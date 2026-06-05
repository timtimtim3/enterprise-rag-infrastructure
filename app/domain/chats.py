from typing import Optional

from pydantic import BaseModel

from app.domain.enums.llm_route import IntentRoute, ResponseMode, RetrievalScope, ToolAction
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
    content_tokens: Optional[int]

    # Assistant-only fields
    model: Optional[str] = None
    finish_reason: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    route_intent: Optional[IntentRoute] = None
    route_retrieval_scope: Optional[RetrievalScope] = None
    route_tool_action: Optional[ToolAction] = None
    route_response_mode: Optional[ResponseMode] = None
    route_confidence: Optional[float] = None
    route_plan: Optional[dict] = None

    # Rag-only fields
    retrieval_embedding_model: Optional[str] = None
    retrieval_reranking_model: Optional[str] = None


class MessageCreateData(MessageBase):
    pass
