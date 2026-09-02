from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.employees import Employee
from app.db.models.employee_skills import EmployeeSkill
from app.db.models.skills import Skill
from app.db.models.customers import Customer
from app.db.models.employee_projects import EmployeeProject
from app.db.models.projects import Project



async def get_employees_by_name(
    db: AsyncSession,
    name: str,
) -> list[Employee]:
    name = " ".join(name.strip().split())

    full_name = func.concat_ws(
        " ",
        Employee.first_name,
        Employee.last_name,
    )

    stmt = (
        select(Employee)
        .where(
            or_(
                Employee.first_name.ilike(name),
                Employee.last_name.ilike(name),
                full_name.ilike(name),
            )
        )
        .order_by(
            Employee.last_name,
            Employee.first_name,
        )
    )

    result = await db.execute(stmt)

    return list(result.scalars().all())


async def get_employee_with_skills(
    db: AsyncSession,
    employee_id: str,
) -> Employee | None:
    stmt = (
        select(Employee)
        .where(Employee.employee_id == employee_id)
        .options(
            selectinload(Employee.employee_skills)
            .selectinload(EmployeeSkill.skill)
        )
    )

    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def find_employees_with_skill(
    db: AsyncSession,
    skill: str,
) -> list[tuple[Employee, EmployeeSkill]]:
    skill = " ".join(skill.strip().split())

    stmt = (
        select(Employee, EmployeeSkill, Skill)
        .join(
            EmployeeSkill,
            EmployeeSkill.employee_id == Employee.id,
        )
        .join(
            Skill,
            Skill.id == EmployeeSkill.skill_id,
        )
        .where(
            Skill.name.ilike(skill)
        )
        .order_by(
            EmployeeSkill.years_experience.desc().nullslast()
        )
    )

    result = await db.execute(stmt)

    return list(result.all())


async def get_projects_for_employee(
    db: AsyncSession,
    employee_id: str,
) -> tuple[
    Employee | None,
    list[tuple[EmployeeProject, Project, Customer]],
]:
    employee_result = await db.execute(
        select(Employee).where(
            Employee.employee_id == employee_id
        )
    )

    employee = employee_result.scalar_one_or_none()

    if employee is None:
        return None, []

    stmt = (
        select(
            EmployeeProject,
            Project,
            Customer,
        )
        .join(
            Project,
            Project.id == EmployeeProject.project_id,
        )
        .join(
            Customer,
            Customer.id == Project.customer_fk,
        )
        .where(
            EmployeeProject.employee_id == employee.id
        )
        .order_by(
            EmployeeProject.start_date.desc().nullslast()
        )
    )

    result = await db.execute(stmt)

    return employee, list(result.all())
