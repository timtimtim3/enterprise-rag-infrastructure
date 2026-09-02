from __future__ import annotations

import uuid
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.employee_skills import EmployeeSkill


class Employee(TimestampMixin, Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False, 
                                             default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)

    job_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    employee_skills: Mapped[list["EmployeeSkill"]] = relationship(back_populates="employee", cascade="all, delete-orphan")
