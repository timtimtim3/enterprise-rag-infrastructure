from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from app.core.config import COLLECTION_NAME, FINAL_TOP_K, INITIAL_TOP_K, MIN_REQUIRED, REL_SCORE_THRESH

if TYPE_CHECKING:
    from qdrant_client import QdrantClient
    from app.models.models import EmbeddingService, Reranker


class Retriever:
    def __init__(
        self, 
        embedding_svc: EmbeddingService,
        reranker: Reranker,
        qdrant_client: QdrantClient,
        collection_name: str = COLLECTION_NAME,
        initial_top_k: int = INITIAL_TOP_K,
        min_required: int = MIN_REQUIRED,
        final_top_k: int = FINAL_TOP_K,
        relative_threshold: float = REL_SCORE_THRESH
    ) -> None:
        self.embedding_svc = embedding_svc
        self.reranker = reranker
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name

        self.initial_top_k = initial_top_k
        self.min_required = min_required
        self.final_top_k = final_top_k
        self.relative_threshold = relative_threshold

    def retrieve_context(
        self,
        query: str,
        initial_top_k: Optional[int] = None,
        min_required: Optional[int] = None,
        final_top_k: Optional[int] = None,
        relative_threshold: Optional[float] = None,
        cutoff: bool = True,
    ) -> List[dict]:
        if initial_top_k is None:
            initial_top_k = self.initial_top_k    
        if min_required is None:
            min_required = self.min_required    
        if final_top_k is None:
            final_top_k = self.final_top_k   
        if relative_threshold is None:
            relative_threshold = self.relative_threshold   

        query_embedding = self.embedding_svc.embed([query])[0]
        resp = self.qdrant_client.query_points(collection_name=self.collection_name, query=query_embedding, limit=initial_top_k)
        points = resp.points

        context_dicts = []
        for point in points:
            point_dct = self._to_context_dict(point)
            context_dicts.append(point_dct)

        if len(context_dicts) == 0:
            return context_dicts

        # Rerank
        context_dicts = self.rerank_context_dicts(query, context_dicts)
        if not cutoff:
            return context_dicts

        # Cutoff / filter
        relative_threshold_score = context_dicts[0]["reranker_score"] * relative_threshold

        # Always keep min_required if available
        if len(context_dicts) <= min_required:
            return context_dicts
        
        # Then keep up to final_top_k but only if score is high enough
        for i in range(min_required, min(len(context_dicts), final_top_k)):
            if context_dicts[i]["reranker_score"] < relative_threshold_score:
                return context_dicts[:i]
        return context_dicts[:final_top_k]
    
    def rerank_context_dicts(self, query: str, context_dicts: List[dict]) -> List[dict]:
        batch_input = [[query, context_dict['text']] for context_dict in context_dicts]
        scores = self.reranker.rerank_scores(batch_input)
        for i, score in enumerate(scores):
            context_dicts[i]["reranker_score"] = float(score)
        sorted_context_dicts = sorted(context_dicts, key=lambda x: x["reranker_score"], reverse=True)
        return sorted_context_dicts
    
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
        