from __future__ import annotations

from typing import List, TYPE_CHECKING

from app.core.config import COLLECTION_NAME

if TYPE_CHECKING:
    from qdrant_client import QdrantClient
    from app.embeddings.service import EmbeddingService


class Retriever:
    def __init__(
        self, 
        embedding_svc: EmbeddingService,
        qdrant_client: QdrantClient,
        collection_name: str = COLLECTION_NAME
    ) -> List[dict]:
        self.embedding_svc = embedding_svc
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name

    def retrieve_context(self, query: str, limit: int = 20) -> List[dict]:
        query_embedding = self.embedding_svc.embed(query)
        resp = self.qdrant_client.query_points(collection_name=self.collection_name, query=query_embedding, limit=limit)
        points = resp.points

        context_dcts = []
        for point in points:
            point_dct = self._to_context_dict(point)
            context_dcts.append(point_dct)
        return context_dcts
    
    def _to_context_dict(self, point) -> dict:
        payload = point.payload or {}

        return {
            "id": str(point.id),
            "score": point.score,

            "doc_id": payload.get("doc_id"),
            "chunk_id": payload.get("chunk_id"),
            "chunk_index": payload.get("chunk_index"),

            "title": payload.get("title"),
            "source_path": payload.get("source_path"),
            "source_type": payload.get("source_type"),
            "vendor": payload.get("vendor"),

            "doc_type": payload.get("doc_type"),
            "status": payload.get("status"),
            "authority": payload.get("authority"),
            "category": payload.get("category"),

            "h1": payload.get("h1"),
            "h2": payload.get("h2"),
            "h3": payload.get("h3"),

            "text": payload.get("text", ""),
            "chunk_char_count": payload.get("chunk_char_count"),
        }
        