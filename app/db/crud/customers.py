# app/db/crud/customers.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.customers import Customer
from app.db.models.projects import Project


def normalize_customer_name(name: str) -> str:
    return " ".join(name.strip().split())


async def get_customers_by_name(
    db: AsyncSession,
    name: str,
) -> list[Customer]:
    name = normalize_customer_name(name)

    stmt = (
        select(Customer)
        .where(
            Customer.name.ilike(f"%{name}%")
        )
        .order_by(Customer.name)
    )

    result = await db.execute(stmt)

    return list(result.scalars().all())


async def get_projects_by_customer_id(
    db: AsyncSession,
    customer_id: str,
) -> tuple[Customer | None, list[Project]]:
    customer_result = await db.execute(
        select(Customer).where(
            Customer.customer_id == customer_id
        )
    )

    customer = customer_result.scalar_one_or_none()

    if customer is None:
        return None, []

    project_result = await db.execute(
        select(Project)
        .where(
            Project.customer_fk == customer.id
        )
        .order_by(Project.name)
    )

    return customer, list(project_result.scalars().all())
