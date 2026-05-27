# scans data/curated/
#   → parses frontmatter
#   → gett body text
#   → normalizes lightly
#   → chunks body text
#   → embeds chunks
#   → stores chunks in Qdrant
#   → stores ingestion state separately
import re
import uuid
import json
import datetime
from pathlib import Path
from typing import Tuple, Dict, List

import frontmatter
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from scripts.helpers import content_hash
from app.embeddings.service import EmbeddingService
from app.core.config import (
    DOC_EXTENSIONS,
    DATA_DIR_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    QDRANT_URL,
    QDRANT_API_KEY,
    INGESTION_STATE_PATH
)


def load_doc(path: Path) -> Tuple[Dict, str]:
    text = path.read_text(encoding="utf-8")
    metadata, content = frontmatter.parse(text)
    return metadata, content


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()


def get_qdrant_uuid(chunk_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_id))


def main() -> None:
    files = [path for path in DATA_DIR_PATH.rglob("*") if path.is_file() and path.suffix in DOC_EXTENSIONS]
    metadata, docs = [], []
    norm_docs_hashes = []
    for path in files:
        meta, doc = load_doc(path)
        norm_doc = normalize_markdown(doc)
        norm_content_hash = content_hash(norm_doc)
        metadata.append(meta)
        docs.append(norm_doc)
        norm_docs_hashes.append(norm_content_hash)

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
    )

    all_chunks: List[Dict] = [] # For storing actual objects in vectorstore like Qdrant
    chunk_texts: List[str] = [] # For embedding all at once (batched)
    pending_ingestion_state = {} # For skipping next time the already embedded docs, only embed on doc content change or model change
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    for doc_index, doc in enumerate(docs):
        chunks = markdown_splitter.split_text(doc)
        chunks = recursive_splitter.split_documents(chunks)
        doc_meta = metadata[doc_index]
        doc_id = doc_meta["doc_id"]
	
        doc_chunks = []
        for chunk_index, chunk in enumerate(chunks):
            text = chunk.page_content
            chunk_hash = content_hash(text)
            chunk_id = f"{doc_id}::{chunk_hash}::{chunk_index}"
            qdrant_chunk_uuid = get_qdrant_uuid(chunk_id)
            chunk_payload = {
                **doc_meta,
                **chunk.metadata,
                "chunk_id": chunk_id,
                "chunk_index": chunk_index,
                "chunk_hash": chunk_hash,
                "chunk_char_count": len(chunk.page_content),
                "text": text,
            }

            chunk_obj = {
                "id": qdrant_chunk_uuid,
                "vector": None,
                "payload": chunk_payload
            }
            all_chunks.append(chunk_obj)
            chunk_texts.append(text)
            doc_chunks.append(chunk_obj)

        # Store ingestion state
        pending_ingestion_state[doc_id] = {
            "source_path": doc_meta.get("source_path"),
            "source_content_hash": doc_meta.get("content_hash"),
            "normalized_content_hash": norm_docs_hashes[doc_index],
            "last_ingested_at": now,
            "chunk_count": len(chunks),
            "chunk_hashes": [chunk["payload"]["chunk_hash"] for chunk in doc_chunks],
            "embedding_model": EMBEDDING_MODEL,
            "collection_name": COLLECTION_NAME,
            "status": "indexed",
        }
		
    # Embed chunks
    embedding_svc = EmbeddingService(EMBEDDING_MODEL)
    chunk_embeddings = embedding_svc.embed(chunk_texts)
    for chunk_obj, embedding in zip(all_chunks, chunk_embeddings):
        chunk_obj["vector"] = embedding
    EMBEDDING_DIM = len(chunk_embeddings[0])

    # Store each chunk_obj (and its embedding) in Qdrant
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )

    points = [
        PointStruct(
            id=chunk["id"], 
            vector=chunk["vector"],
            payload=chunk["payload"]
        )
        for chunk in all_chunks
    ]      

    BATCH_SIZE = 64
    for i in range(0, len(points), BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch,
            wait=True,
        )
        print(f"Uploaded batch {i // BATCH_SIZE + 1}")

    # Once sucessfully stored, write the ingestion state, for now keep local simple store file, later write to postgresql db service
    INGESTION_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    INGESTION_STATE_PATH.write_text(
        json.dumps(pending_ingestion_state, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
