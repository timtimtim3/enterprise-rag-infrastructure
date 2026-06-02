from pydantic import BaseModel, Field
from typing import List, Optional


class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=20_000)


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class Source(BaseModel):
    doc_id: str
    source_index: int
    title: str
    source_path: str
    source_type: str
    doc_type: str
    chunk_indices: List[int]


class AskResponse(BaseModel):
    chat_id: str
    query_message_id: str
    answer_message_id: str
    answer: str
    model: Optional[str]
    finish_reason: Optional[str]
    usage: Usage
    sources: List[Source]
