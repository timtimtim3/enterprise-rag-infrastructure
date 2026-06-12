from typing import List
from abc import ABC, abstractmethod


class RerankerProvider(ABC):
    @abstractmethod
    async def rerank(self, query_passage_pairs: List[List[str]]) -> List[float]:
        pass

    def prepare_input(self, query: str, passages: List[str]):
        return [[query, passage] for passage in passages]
