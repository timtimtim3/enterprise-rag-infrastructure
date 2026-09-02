from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.employee_projects import EmployeeProject
from app.db.models.employees import Employee
from app.db.models.projects import Project
from app.db.models.customers import Customer


def normalize_project_name(name: str) -> str:
    return " ".join(name.strip().split())


async def get_projects_by_name(
    db: AsyncSession,
    name: str,
) -> list[tuple[Project, Customer]]:
    name = normalize_project_name(name)

    stmt = (
        select(Project, Customer)
        .join(
            Customer,
            Customer.id == Project.customer_fk,
        )
        .where(
            Project.name.ilike(f"%{name}%")
        )
        .order_by(
            Customer.name,
            Project.name,
        )
    )

    result = await db.execute(stmt)

    return list(result.all())


async def get_team_for_project(
    db: AsyncSession,
    project_id: str,
) -> tuple[
    Project | None,
    list[tuple[EmployeeProject, Employee]],
]:
    project_result = await db.execute(
        select(Project).where(
            Project.project_id == project_id
        )
    )

    project = project_result.scalar_one_or_none()

    if project is None:
        return None, []

    stmt = (
        select(
            EmployeeProject,
            Employee,
        )
        .join(
            Employee,
            Employee.id == EmployeeProject.employee_id,
        )
        .where(
            EmployeeProject.project_id == project.id
        )
        .order_by(
            Employee.last_name,
            Employee.first_name,
        )
    )

    result = await db.execute(stmt)

    return project, list(result.all())
