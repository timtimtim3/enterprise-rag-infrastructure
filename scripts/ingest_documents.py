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
import asyncio
import frontmatter
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct

from app.rag.embeddings.factory import embedding_provider_factory
from scripts.helpers import content_hash
from app.rag.vectorstores.qdrant_store import delete_qdrant_points_by_doc_id, get_provider_model_name_identifier, init_qdrant, name_qdrant_collection, update_qdrant_points_metadata
from app.core.config import (
    DOC_EXTENSIONS,
    DATA_DIR_PATH,
    COLLECTION_NAME_PREFIX,
    EMBEDDING_PROVIDER,
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


async def main() -> None:
    embedding_provider = embedding_provider_factory(EMBEDDING_PROVIDER)
    provider_model_name_identifier = get_provider_model_name_identifier(EMBEDDING_PROVIDER, embedding_provider.model_name)
    ingestion_file = INGESTION_STATE_PATH / f"ingestion-state_{provider_model_name_identifier}.json"
    qdrant_collection_name = name_qdrant_collection(COLLECTION_NAME_PREFIX, EMBEDDING_PROVIDER, embedding_provider.model_name)

    try:
        # Init qdrant_client here when the collection already exists and we need it to re-embed / re-store / update meta
        # early for when content has changed 
        qdrant_client = await init_qdrant(qdrant_collection_name)
    except Exception:
        # If collection doesn't exist yet, we assume we don't call qdrant_client yet since we don't have an ingestion_state yet
        qdrant_client = None

    # Read ingestion state
    ingestion_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(ingestion_file, 'r') as file:
            ingestion_state = json.load(file)
    except FileNotFoundError as e:
        ingestion_state = {}
    pending_ingestion_state = ingestion_state.copy() # For skipping next time the already embedded docs, only embed on doc content change or model change
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    # Decide which docs to ingest
    files = [path for path in DATA_DIR_PATH.rglob("*") if path.is_file() and path.suffix in DOC_EXTENSIONS]
    metadata, docs = [], []
    norm_docs_hashes, meta_hashes = [], []
    for path in files:
        meta, doc = load_doc(path)
        norm_doc = normalize_markdown(doc)
        norm_content_hash = content_hash(norm_doc)
        meta_str = json.dumps(
            meta,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        meta_hash = content_hash(meta_str)

        # Check for doc changes and metadata changes in ingestion_state
        doc_id = meta["doc_id"]
        if doc_id in ingestion_state:
            # Doc was ingested before
            state = ingestion_state[doc_id]

            if norm_content_hash != state["normalized_content_hash"]:
                # Content changed, requires deleting (then re-embedding and re-storing)
                await delete_qdrant_points_by_doc_id(qdrant_client, doc_id, qdrant_collection_name)
            elif "meta_hash" not in state or meta_hash != state["meta_hash"]:
                # Requires meta update only
                await update_qdrant_points_metadata(qdrant_client, meta, doc_id, qdrant_collection_name)
                pending_ingestion_state[doc_id]["meta_hash"] = meta_hash
                pending_ingestion_state[doc_id]["last_metadata_updated_at"] = now
                continue
            else:
                # No update required
                continue

        # We will embed these and store these
        metadata.append(meta)
        docs.append(norm_doc)
        norm_docs_hashes.append(norm_content_hash)
        meta_hashes.append(meta_hash)

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
            "meta_hash": meta_hashes[doc_index],
            "last_ingested_at": now,
            "last_metadata_updated_at": now,
            "chunk_count": len(chunks),
            "chunk_hashes": [chunk["payload"]["chunk_hash"] for chunk in doc_chunks],
            "embedding_model": embedding_provider.model_name,
            "embedding_provider": EMBEDDING_PROVIDER.value,
            "collection_name": qdrant_collection_name,
            "status": "indexed",
        }
	
    if len(chunk_texts) > 0:
        # Embed chunks
        chunk_embeddings = await embedding_provider.embed_documents(chunk_texts)
        for chunk_obj, embedding in zip(all_chunks, chunk_embeddings):
            chunk_obj["vector"] = embedding
        EMBEDDING_DIM = len(chunk_embeddings[0])
        # We need to call this again here in case this is the first time running this script
        # and we don't have the collection initialized yet
        qdrant_client = await init_qdrant(qdrant_collection_name, EMBEDDING_DIM)

        # Store each chunk_obj (and its embedding) in Qdrant
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
            await qdrant_client.upsert(
                collection_name=qdrant_collection_name,
                points=batch,
                wait=True,
            )
            print(f"Uploaded batch {i // BATCH_SIZE + 1}")

    # Once sucessfully stored, write the ingestion state, for now keep local simple store file, later write to postgresql db service
    ingestion_file.write_text(
        json.dumps(pending_ingestion_state, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    asyncio.run(main())
