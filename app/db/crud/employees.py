from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.employees import Employee


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
