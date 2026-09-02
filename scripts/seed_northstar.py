# scripts/seed_northstar.py

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal
from app.db.models.employee_skills import EmployeeSkill
from app.db.models.employees import Employee
from app.db.models.skills import Skill


EMPLOYEES = [
    {
        "employee_id": "emp_001",
        "first_name": "John",
        "last_name": "Smith",
        "job_title": "Cloud Consultant",
        "department": "Cloud & Platform",
        "skills": [
            {
                "name": "AWS",
                "proficiency": "expert",
                "years_experience": 6,
            },
            {
                "name": "Terraform",
                "proficiency": "advanced",
                "years_experience": 4,
            },
            {
                "name": "Kubernetes",
                "proficiency": "advanced",
                "years_experience": 3,
            },
        ],
    },
    {
        "employee_id": "emp_002",
        "first_name": "John",
        "last_name": "de Vries",
        "job_title": "Backend Engineer",
        "department": "Software Engineering",
        "skills": [
            {
                "name": "Python",
                "proficiency": "expert",
                "years_experience": 6,
            },
            {
                "name": "FastAPI",
                "proficiency": "expert",
                "years_experience": 4,
            },
            {
                "name": "PostgreSQL",
                "proficiency": "advanced",
                "years_experience": 5,
            },
        ],
    },
    {
        "employee_id": "emp_003",
        "first_name": "Alice",
        "last_name": "Jansen",
        "job_title": "AI Engineer",
        "department": "Data & AI",
        "skills": [
            {
                "name": "Python",
                "proficiency": "expert",
                "years_experience": 5,
            },
            {
                "name": "RAG",
                "proficiency": "expert",
                "years_experience": 3,
            },
            {
                "name": "LangGraph",
                "proficiency": "advanced",
                "years_experience": 2,
            },
            {
                "name": "Qdrant",
                "proficiency": "advanced",
                "years_experience": 2,
            },
        ],
    },
]


def normalize_skill_name(name: str) -> str:
    return " ".join(name.strip().split())


async def get_or_create_skill(
    db: AsyncSession,
    name: str,
) -> Skill:
    normalized_name = normalize_skill_name(name)

    result = await db.execute(
        select(Skill).where(
            Skill.name.ilike(normalized_name)
        )
    )

    skill = result.scalar_one_or_none()

    if skill is not None:
        return skill

    skill = Skill(
        name=normalized_name,
    )

    db.add(skill)
    await db.flush()

    return skill


async def get_employee_by_employee_id(
    db: AsyncSession,
    employee_id: str,
) -> Employee | None:
    result = await db.execute(
        select(Employee).where(
            Employee.employee_id == employee_id
        )
    )

    return result.scalar_one_or_none()


async def employee_skill_exists(
    db: AsyncSession,
    employee_id: int,
    skill_id: int,
) -> bool:
    result = await db.execute(
        select(EmployeeSkill).where(
            EmployeeSkill.employee_id == employee_id,
            EmployeeSkill.skill_id == skill_id,
        )
    )

    return result.scalar_one_or_none() is not None


async def seed_employee(
    db: AsyncSession,
    data: dict,
) -> None:
    employee = await get_employee_by_employee_id(
        db=db,
        employee_id=data["employee_id"],
    )

    if employee is None:
        employee = Employee(
            employee_id=data["employee_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            job_title=data["job_title"],
            department=data["department"],
        )

        db.add(employee)
        await db.flush()

        print(
            f"Added employee: "
            f"{employee.first_name} {employee.last_name}"
        )
    else:
        print(
            f"Employee already exists: "
            f"{employee.first_name} {employee.last_name}"
        )

    for skill_data in data["skills"]:
        skill = await get_or_create_skill(
            db=db,
            name=skill_data["name"],
        )

        exists = await employee_skill_exists(
            db=db,
            employee_id=employee.id,
            skill_id=skill.id,
        )

        if exists:
            print(
                f"  Skill already assigned: {skill.name}"
            )
            continue

        employee_skill = EmployeeSkill(
            employee_id=employee.id,
            skill_id=skill.id,
            proficiency=skill_data["proficiency"],
            years_experience=skill_data["years_experience"],
        )

        db.add(employee_skill)

        print(
            f"  Added skill: {skill.name}"
        )


async def seed_employees(
    db: AsyncSession,
) -> None:
    for employee_data in EMPLOYEES:
        await seed_employee(
            db=db,
            data=employee_data,
        )


async def main():
    async with SessionLocal() as db:
        try:
            await seed_employees(db)

            await db.commit()

            print()
            print("Northstar seed completed successfully.")

        except Exception:
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
