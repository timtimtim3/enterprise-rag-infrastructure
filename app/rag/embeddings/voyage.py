import voyageai
from typing import List

from app.rag.embeddings.base import EmbeddingProvider


class VoyageEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str):
        self.vo = voyageai.AsyncClient(api_key=api_key)
        self.model = model

    async def embed_documents(self, chunk_texts: List[str]) -> List[List[float]]:
        result = await self.vo.embed(chunk_texts, model=self.model, input_type="document")
        return result.embeddings
    
    async def embed_query(self, text: str) -> List[float]:
        result = await self.vo.embed([text], model=self.model, input_type="query")
        return result.embeddings[0]
    