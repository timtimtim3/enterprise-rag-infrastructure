from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.employees import Employee
    from app.db.models.skills import Skill


class EmployeeSkill(TimestampMixin, Base):
    __tablename__ = "employee_skills"

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        primary_key=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True,
    )

    proficiency: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    years_experience: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="employee_skills",
    )

    skill: Mapped["Skill"] = relationship(
        back_populates="employee_skills",
    )
