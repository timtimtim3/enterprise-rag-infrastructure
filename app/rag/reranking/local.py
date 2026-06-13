from typing import List
from sentence_transformers import CrossEncoder
from fastapi.concurrency import run_in_threadpool

from app.rag.reranking.base import RerankerProvider


class LocalRerankerProvider(RerankerProvider):
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)
        self.model_name = model_name

    async def rerank(self, query: str, chunks: List[str]) -> List[float]:
        query_passage_pairs = self.prepare_input(query, chunks)
        return await run_in_threadpool(self.model.predict, query_passage_pairs)
