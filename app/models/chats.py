from __future__ import annotations

import uuid
from sqlalchemy import Integer, String, ForeignKey, Float, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLEnum

from app.db.base import Base
from app.models.timestamp import TimestampMixin
from app.enums.message_role import MessageRole

if TYPE_CHECKING:
    from app.models.users import User
    

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
    