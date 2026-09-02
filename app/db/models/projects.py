# app/db/models/projects.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.customers import Customer
    from app.db.models.employee_projects import EmployeeProject


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )

    customer_fk: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        index=True,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="projects",
    )

    employee_projects: Mapped[list["EmployeeProject"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    