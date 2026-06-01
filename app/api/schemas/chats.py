from pydantic import BaseModel
from typing import List, Optional


class AskRequest(BaseModel):
    query: str


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Source(BaseModel):
    source_index: int
    title: str
    source_path: str
    doc_id: str
    chunk_indices: List[int]


class AskResponse(BaseModel):
    answer: str
    model: Optional[str]
    finish_reason: Optional[str]
    usage: Usage
    sources: List[Source]
