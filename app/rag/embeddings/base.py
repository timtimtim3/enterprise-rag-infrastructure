from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    @abstractmethod
    def __init__(self, model_name: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def embed_documents(self, chunk_texts: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
        pass
    