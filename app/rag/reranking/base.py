from typing import List
from abc import ABC, abstractmethod

from app.rag.reranking.providers import RerankerProviders


class RerankerProvider(ABC):
    provider: RerankerProviders
    model_name: str

    @abstractmethod
    def __init__(self, model_name: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def rerank(self, query: str, chunks: List[str], *args, **kwargs) -> List[float]:
        pass

    def prepare_input(self, query: str, chunks: List[str]):
        return [[query, chunk] for chunk in chunks]
