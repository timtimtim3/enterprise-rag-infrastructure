from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, FieldCondition, Filter, FilterSelector, MatchValue, VectorParams, PayloadSchemaType

from app.core.config import COLLECTION_NAME, QDRANT_API_KEY, QDRANT_URL


def ensure_payload_index(
    qdrant_client,
    collection_name: str,
    collection_info,
    field_name: str,
    field_schema,
) -> None:
    if field_name in collection_info.payload_schema:
        return

    qdrant_client.create_payload_index(
        collection_name=collection_name,
        field_name=field_name,
        field_schema=field_schema,
    )


def init_qdrant(embedding_dim: Optional[int] = None):
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    if not qdrant_client.collection_exists(COLLECTION_NAME):
        if embedding_dim is None:
            raise ValueError(
                "embedding_dim must be provided when creating a new Qdrant collection"
            )
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
        )

    collection_info = qdrant_client.get_collection(COLLECTION_NAME)
    
    ensure_payload_index(qdrant_client, COLLECTION_NAME, collection_info, "doc_id", PayloadSchemaType.KEYWORD)
    ensure_payload_index(qdrant_client, COLLECTION_NAME, collection_info, "chunk_index", PayloadSchemaType.INTEGER)
    return qdrant_client


def update_qdrant_points_metadata(qdrant_client, new_doc_metadata_fields: dict, doc_id: str, collection_name: str = COLLECTION_NAME):
    # This merges the existing payload with this one, overriding fields with the same key, and adding new ones (this doesn't handle removal of fiellds)
    qdrant_client.set_payload(
        collection_name=collection_name,
        payload=new_doc_metadata_fields,
        points=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    )
                ]
            )
        ),
    )


def delete_qdrant_points_by_doc_id(
    qdrant_client,
    doc_id: str,
    collection_name: str = COLLECTION_NAME,
) -> None:
    qdrant_client.delete(
        collection_name=collection_name,
        points_selector=FilterSelector(
            filter=Filter(
                must=[
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    )
                ]
            )
        ),
    )


def get_all_qdrant_points_by_doc_id(qdrant_client, doc_id: str, collection_name: str = COLLECTION_NAME, limit: int = 100) -> List:
    all_doc_chunks = []
    offset = None

    while True:
        points, offset = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="doc_id",
                        match=MatchValue(value=doc_id),
                    )
                ]
            ),
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        all_doc_chunks.extend(points)

        if offset is None:
            break
    return all_doc_chunks
