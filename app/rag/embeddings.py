from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name

    def embed(self, chunk_texts: List[str]) -> List[List[float]]:
        return self.model.encode(chunk_texts, normalize_embeddings=True, batch_size=32)
    