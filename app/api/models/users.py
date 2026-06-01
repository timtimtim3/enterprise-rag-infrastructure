from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import TYPE_CHECKING

from app.api.db import Base

if TYPE_CHECKING:
    from app.api.models.chats import Chat


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="user")
