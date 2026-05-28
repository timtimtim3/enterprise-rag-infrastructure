from typing import List
from sentence_transformers import SentenceTransformer, CrossEncoder


class EmbeddingService:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, chunk_texts: List[str]) -> List[List[float]]:
        return self.model.encode(chunk_texts, normalize_embeddings=True, batch_size=32)
    

class Reranker:
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)

    def rerank_scores(self, query_passage_pairs: List[List[str]]) -> List[float]:
        return self.model.predict(query_passage_pairs)
    
    def prepare_input(self, query: str, passages: List[str]):
        return [[query, passage] for passage in passages]
