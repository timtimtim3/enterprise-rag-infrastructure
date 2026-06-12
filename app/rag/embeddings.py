from abc import ABC, abstractmethod
from typing import List
from sentence_transformers import SentenceTransformer
from fastapi.concurrency import run_in_threadpool


class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, chunk_texts: List[str]) -> List[List[float]]:
        pass


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    async def embed(self, chunk_texts: List[str]) -> List[List[float]]:
        return await run_in_threadpool(self.model.encode, chunk_texts, normalize_embeddings=True, batch_size=32)
    