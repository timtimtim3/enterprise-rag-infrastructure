import asyncio

import voyageai
from typing import List

from app.rag.embeddings.base import EmbeddingProvider
from app.rag.embeddings.providers import EmbeddingProviders


class VoyageEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        batch_size: int = 8,
        sleep_seconds: float = 25,
    ):
        self.provider = EmbeddingProviders.VOYAGE
        self.vo = voyageai.AsyncClient(api_key=api_key)
        self.model_name = model_name
        self.batch_size = batch_size
        self.sleep_seconds = sleep_seconds

    async def embed_documents(self, chunk_texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []

        for i in range(0, len(chunk_texts), self.batch_size):
            batch = chunk_texts[i : i + self.batch_size]

            result = await self.vo.embed(
                batch,
                model=self.model_name,
                input_type="document",
            )
            embeddings.extend(result.embeddings)

            if i + self.batch_size < len(chunk_texts):
                await asyncio.sleep(self.sleep_seconds)

        return embeddings
    
    async def embed_query(self, text: str) -> List[float]:
        result = await self.vo.embed([text], model=self.model_name, input_type="query")
        return result.embeddings[0]
    