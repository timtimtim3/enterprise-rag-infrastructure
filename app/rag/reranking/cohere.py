import cohere
from typing import List

from app.rag.reranking.base import RerankerProvider
from app.rag.reranking.providers import RerankerProviders


class CohereRerankerProvider(RerankerProvider):
    def __init__(self, model_name: str, api_key: str):
        self.provider = RerankerProviders.COHERE
        self.model_name = model_name
        self.co = cohere.AsyncClientV2(api_key=api_key)

    async def rerank(self, query: str, chunks: List[str]) -> List[float]:
        result = await self.co.rerank(model=self.model_name, query=query, documents=chunks, top_n=len(chunks))

        scores = [0.0] * len(chunks)

        for item in result.results:
            scores[item.index] = item.relevance_score

        return scores
