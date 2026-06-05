from typing import List
from sentence_transformers import CrossEncoder
from fastapi.concurrency import run_in_threadpool


class Reranker:
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)
        self.model_name = model_name

    async def rerank_scores(self, query_passage_pairs: List[List[str]]) -> List[float]:
        return await run_in_threadpool(self.model.predict, query_passage_pairs)
    
    def prepare_input(self, query: str, passages: List[str]):
        return [[query, passage] for passage in passages]
