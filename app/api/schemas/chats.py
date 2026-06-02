from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from app.enums.message_role import MessageRole


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


class ChatInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: str
    title: Optional[str]


class MessageInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message_id: str
    role: MessageRole
    content: str


class MessageSourceInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doc_id: str
    source_index: int
    chunk_indices: list[int]
    title: str
    source_path: str
    source_type: str
    doc_type: str
    score: Optional[float] = None
    reranker_score: Optional[float] = None


class ListChatsResponse(BaseModel):
    chats: List[ChatInfo]


class ListMessagesResponse(BaseModel):
    messages: List[MessageInfo]


class ListMessageSourcesResponse(BaseModel):
    message_sources: List[MessageSourceInfo]
