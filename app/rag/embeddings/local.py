from typing import List
from sentence_transformers import SentenceTransformer
from fastapi.concurrency import run_in_threadpool

from app.rag.embeddings.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    async def embed_documents(self, chunk_texts: List[str]) -> List[List[float]]:
        embeddings = await run_in_threadpool(
            self.model.encode,
            chunk_texts,
            normalize_embeddings=True,
            batch_size=32,
        )
        return embeddings.tolist()
        
    async def embed_query(self, text: str) -> List[float]:
        embeddings = await run_in_threadpool(
            self.model.encode,
            [text],
            normalize_embeddings=True,
            batch_size=32,
        )
        return embeddings[0].tolist()
    