from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from enum import Enum
from sqlalchemy import Enum as SQLEnum

from app.db.base import Base
from app.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.users import User
    

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Chat(TimestampMixin, Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="chats")
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat")


class Message(TimestampMixin, Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    role: Mapped[MessageRole] = mapped_column(SQLEnum(MessageRole, name="message_role"), nullable=False)
    content: Mapped[str] = mapped_column(String)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    chat_fk: Mapped[int] = mapped_column(ForeignKey("chats.id"))

    message_sources: Mapped[list["MessageSource"]] = relationship("MessageSource", back_populates="message")


class MessageSource(TimestampMixin, Base):
    __tablename__ = "message_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    doc_id: Mapped[str] = mapped_column(String)
    source_index: Mapped[int] = mapped_column(Integer)
    chunk_indices: Mapped[list[int]] = mapped_column(ARRAY(Integer))

    title: Mapped[str] = mapped_column(String)
    source_path: Mapped[str] = mapped_column(String)
    source_type: Mapped[str] = mapped_column(String)
    doc_type: Mapped[str] = mapped_column(String)

    score: Mapped[float] = mapped_column(Float)
    reranker_score: Mapped[float] = mapped_column(Float)

    message: Mapped["Message"] = relationship("Message", back_populates="message_sources")
    message_fk: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    