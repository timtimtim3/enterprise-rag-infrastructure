from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from app.db.base import Base
from app.db.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.employee_skills import EmployeeSkill


class Skill(TimestampMixin, Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    employee_skills: Mapped[list["EmployeeSkill"]] = relationship(back_populates="skill", cascade="all, delete-orphan")
    