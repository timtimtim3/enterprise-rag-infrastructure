from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from app.domain.chats import SourceBase, MessageBase


class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=20_000)


class SourceInfo(SourceBase):
    pass


class UsageInfo(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class AskResponse(BaseModel):
    chat_id: str
    query_message_id: str
    answer_message_id: str
    answer: str
    model: Optional[str]
    finish_reason: Optional[str]
    usage: UsageInfo
    sources: List[SourceInfo]


class ChatInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: str
    title: Optional[str]


class ListChatsResponse(BaseModel):
    chats: List[ChatInfo]


class MessageInfo(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    message_id: str


class ListMessagesResponse(BaseModel):
    messages: List[MessageInfo]


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


class ListMessageSourcesResponse(BaseModel):
    message_sources: List[MessageSourceInfo]
