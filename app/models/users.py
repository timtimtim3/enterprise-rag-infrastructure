from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.api.db import Base
from app.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.chats import Chat


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="user")
