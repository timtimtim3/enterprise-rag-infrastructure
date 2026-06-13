from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING, Set

from app.core.config import (
    COLLECTION_NAME_PREFIX, 
    FINAL_TOP_K, 
    INITIAL_TOP_K, 
    MIN_REQUIRED, 
    REL_SCORE_THRESH, 
    EXPAND_WINDOW_BEFORE,
    EXPAND_WINDOW_AFTER,
    KEEP_ENTIRE_DOC_CHUNK_THRESH
)
from app.rag.vectorstores.qdrant_store import get_all_qdrant_points_by_doc_id

if TYPE_CHECKING:
    from qdrant_client import AsyncQdrantClient
    from app.rag.embeddings.local import LocalEmbeddingProvider
    from app.rag.reranking.local import LocalRerankerProvider


class Retriever:
    def __init__(
        self, 
        embedding_svc: LocalEmbeddingProvider,
        reranker: LocalRerankerProvider,
        qdrant_client: AsyncQdrantClient,
        collection_name: str = COLLECTION_NAME_PREFIX,
        initial_top_k: int = INITIAL_TOP_K,
        min_required: int = MIN_REQUIRED,
        final_top_k: int = FINAL_TOP_K,
        relative_threshold: float = REL_SCORE_THRESH,
        expand_window_before: int = EXPAND_WINDOW_BEFORE,
        expand_window_after: int = EXPAND_WINDOW_AFTER,
        keep_entire_doc_chunk_thresh: int = KEEP_ENTIRE_DOC_CHUNK_THRESH
    ) -> None:
        self.embedding_svc = embedding_svc
        self.reranker = reranker
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name

        self.initial_top_k = initial_top_k
        self.min_required = min_required
        self.final_top_k = final_top_k
        self.relative_threshold = relative_threshold

        self.expand_window_before = expand_window_before
        self.expand_window_after = expand_window_after
        self.keep_entire_doc_chunk_thresh = keep_entire_doc_chunk_thresh

    async def retrieve_context(
        self,
        query: str,
        initial_top_k: Optional[int] = None,
        min_required: Optional[int] = None,
        final_top_k: Optional[int] = None,
        relative_threshold: Optional[float] = None,
        cutoff: bool = True,
        expand: bool = True
    ) -> List[dict]:
        if initial_top_k is None:
            initial_top_k = self.initial_top_k    
        if min_required is None:
            min_required = self.min_required    
        if final_top_k is None:
            final_top_k = self.final_top_k   
        if relative_threshold is None:
            relative_threshold = self.relative_threshold   

        query_embedding = await self.embedding_svc.embed_query(query)
        resp = await self.qdrant_client.query_points(collection_name=self.collection_name, query=query_embedding, limit=initial_top_k)
        points = resp.points

        context_dicts = [self._to_context_dict(point) for point in points]
        if len(context_dicts) == 0:
            return context_dicts

        # Rerank
        context_dicts = await self.rerank_context_dicts(query, context_dicts)

        # Cutoff / filter
        to_keep = None
        if not cutoff:
            to_keep = context_dicts
        else:
            relative_threshold_score = context_dicts[0]["reranker_score"] * relative_threshold

            # Always keep min_required if available
            if len(context_dicts) <= min_required:
                to_keep = context_dicts
            else:
                # Then keep up to final_top_k but only if score is high enough
                for i in range(min_required, min(len(context_dicts), final_top_k)):
                    if context_dicts[i]["reranker_score"] < relative_threshold_score:
                        to_keep = context_dicts[:i]
                        break

            if i == min(len(context_dicts), final_top_k) - 1:
                to_keep = context_dicts[:final_top_k]

        # Do neighbor chunk / parent doc context expansion
        if expand:
            expanded_doc_dicts: dict[str, List[dict]] = {}
            doc_id_to_included_chunk_idcs: dict[str, Set[int]]= {}

            for context_dict in to_keep:
                doc_id = context_dict["doc_id"]
                all_doc_chunks = await get_all_qdrant_points_by_doc_id(self.qdrant_client, doc_id)
                doc_chunk_count = len(all_doc_chunks)

                if context_dict["source_type"] == "internal" and doc_chunk_count <= self.keep_entire_doc_chunk_thresh:
                    # Keep all chunks from the doc if it's internal and only has a couple of chunks
                    chunks_to_keep = [self._to_context_dict(chunk) for chunk in all_doc_chunks]
                else:
                    # Otherwise take neighboring chunks
                    chunk_index = context_dict["chunk_index"]
                    chunks_before_start_idx = max(0, chunk_index - self.expand_window_before)
                    chunks_after_end_idx = min(doc_chunk_count - 1, chunk_index + self.expand_window_after)
                    chunk_indices = set(range(chunks_before_start_idx, chunks_after_end_idx + 1))

                    chunks_to_keep = []
                    for chunk in all_doc_chunks:
                        chunk_dict = self._to_context_dict(chunk)
                        if chunk_dict["chunk_index"] in chunk_indices:
                            chunks_to_keep.append(chunk_dict)
                
                if len(chunks_to_keep) == 0:
                    continue

                # Deduplicate
                deduplicate_chunks_to_keep = []
                chunks_to_keep.sort(key=lambda x: x["chunk_index"])
                starting_idx = chunks_to_keep[0]["chunk_index"]
                ending_idx = starting_idx if len(chunks_to_keep) == 1 else chunks_to_keep[-1]["chunk_index"]
                if doc_id not in doc_id_to_included_chunk_idcs:
                    # Nothing to deduplicate yet since this is the first expanded chunk set for this doc we are encountering
                    doc_id_to_included_chunk_idcs[doc_id] = set(range(starting_idx, ending_idx + 1))
                    deduplicate_chunks_to_keep = chunks_to_keep
                else:
                    # We've already seen an expanded chunk set and thus must deduplicate the current one to only add chunks we
                    # don't have yet
                    for i, chunk_index in enumerate(range(starting_idx, ending_idx + 1)):
                        if chunk_index not in doc_id_to_included_chunk_idcs[doc_id]:
                            deduplicate_chunks_to_keep.append(chunks_to_keep[i])
                            doc_id_to_included_chunk_idcs[doc_id].add(chunk_index)

                if len(deduplicate_chunks_to_keep) == 0:
                    continue

                if doc_id not in expanded_doc_dicts:
                    expanded_doc_dicts[doc_id] = [deduplicate_chunks_to_keep]
                else:
                    expanded_doc_dicts[doc_id].append(deduplicate_chunks_to_keep)

            # Sort inner lists in expanded_doc_dicts and combine into one large list
            big_lst = []
            for doc_id, list_of_doc_lists in expanded_doc_dicts.items():
                list_of_doc_lists.sort(key=lambda lst: lst[0]["chunk_index"])
                for lst in list_of_doc_lists:
                    big_lst.extend(lst)
            return big_lst
        return to_keep
    
    async def rerank_context_dicts(self, query: str, context_dicts: List[dict]) -> List[dict]:
        chunks = [context_dict['text'] for context_dict in context_dicts]
        scores = await self.reranker.rerank(query, chunks)
        for i, score in enumerate(scores):
            context_dicts[i]["reranker_score"] = float(score)
        sorted_context_dicts = sorted(context_dicts, key=lambda x: x["reranker_score"], reverse=True)
        return sorted_context_dicts
    
    def _to_context_dict(self, point) -> dict:
        payload = point.payload or {}

        return {
            # retrieval
            "id": str(point.id),
            "score": None if not hasattr(point, "score") else point.score,

            # document identity
            "doc_id": payload.get("doc_id"),
            "chunk_id": payload.get("chunk_id"),
            "chunk_index": payload.get("chunk_index"),

            # document metadata
            "title": payload.get("title"),
            "source_path": payload.get("source_path"),
            "source_type": payload.get("source_type"),
            "classification": payload.get("classification"),
            "visibility": payload.get("visibility"),
            "organization": payload.get("organization"),
            "vendor": payload.get("vendor"),
            "url": payload.get("url"),
            "doc_type": payload.get("doc_type"),
            "status": payload.get("status"),
            "authority": payload.get("authority"),
            "category": payload.get("category"),
            "tags": payload.get("tags"),

            # structure
            "h1": payload.get("h1"),
            "h2": payload.get("h2"),
            "h3": payload.get("h3"),

            # chunk content
            "text": payload.get("text", ""),
            "chunk_char_count": payload.get("chunk_char_count"),
        }
        