# app/db/models/employee_projects.py

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.employees import Employee
    from app.db.models.projects import Project


class EmployeeProject(TimestampMixin, Base):
    __tablename__ = "employee_projects"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        primary_key=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        primary_key=True,
    )

    role: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    allocation_percentage: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="employee_projects",
    )

    project: Mapped["Project"] = relationship(
        back_populates="employee_projects",
    )
    