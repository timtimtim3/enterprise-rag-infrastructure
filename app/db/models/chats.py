from __future__ import annotations

import uuid
from sqlalchemy import JSON, Integer, String, ForeignKey, Float, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Enum as SQLEnum

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin
from app.domain.enums.message_role import MessageRole
from app.domain.enums.llm_route import IntentRoute, RetrievalScope, ToolAction, ResponseMode

if TYPE_CHECKING:
    from app.db.models.users import User
    

class Chat(TimestampMixin, Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="chats")
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class Message(TimestampMixin, Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    role: Mapped[MessageRole] = mapped_column(SQLEnum(MessageRole, name="message_role"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Assistant-only fields
    model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    finish_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    route_intent: Mapped[Optional[IntentRoute]] = mapped_column(SQLEnum(IntentRoute, name="route_intent"), nullable=True)
    route_retrieval_scope: Mapped[Optional[RetrievalScope]] = mapped_column(SQLEnum(RetrievalScope, name="route_retrieval_scope"), 
                                                                            nullable=True)
    route_tool_action: Mapped[Optional[ToolAction]] = mapped_column(SQLEnum(ToolAction, name="route_tool_action"), nullable=True)
    route_response_mode: Mapped[Optional[ResponseMode]] = mapped_column(SQLEnum(ResponseMode, name="route_response_mode"), 
                                                                        nullable=True)
    route_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    route_plan: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Rag-only fields
    retrieval_embedding_model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    retrieval_reranking_model: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    chat_fk: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)

    message_sources: Mapped[list["MessageSource"]] = relationship("MessageSource", back_populates="message", cascade="all, delete-orphan")


class MessageSource(TimestampMixin, Base):
    __tablename__ = "message_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    doc_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_indices: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_type: Mapped[str] = mapped_column(String(255), nullable=False)
    doc_type: Mapped[str] = mapped_column(String(255), nullable=False)

    score: Mapped[float] = mapped_column(Float, nullable=True)
    reranker_score: Mapped[float] = mapped_column(Float, nullable=True)

    message: Mapped["Message"] = relationship("Message", back_populates="message_sources")
    message_fk: Mapped[int] = mapped_column(ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    