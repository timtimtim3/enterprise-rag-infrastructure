from typing import Optional

from pydantic import BaseModel

from app.domain.enums.llm_route import LLMRoute
from app.domain.enums.message_role import MessageRole


class SourceBase(BaseModel):
    doc_id: str
    source_index: int
    title: str
    source_path: str
    source_type: str
    doc_type: str
    chunk_indices: list[int]


class SourceCreateData(SourceBase):
    pass


class MessageBase(BaseModel):
    role: MessageRole
    content: str

    # Assistant-only fields
    model: Optional[str] = None
    route: Optional[LLMRoute] = None
    finish_reason: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    # Rag-only fields
    retrieval_embedding_model: Optional[str] = None
    retrieval_reranking_model: Optional[str] = None


class MessageCreateData(MessageBase):
    pass
