# app/db/models/customers.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.projects import Project


class Customer(TimestampMixin, Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String(150),
        index=True,
        nullable=False,
    )

    industry: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    