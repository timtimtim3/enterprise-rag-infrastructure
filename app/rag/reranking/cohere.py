from typing import List

from app.rag.reranking.base import RerankerProvider


class CohereRerankerProvider(RerankerProvider):
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name

    async def rerank(self, query_passage_pairs: List[List[str]]) -> List[float]:
        return [0.0]
