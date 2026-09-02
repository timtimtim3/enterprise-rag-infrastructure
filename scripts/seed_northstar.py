# scripts/seed_northstar.py

import asyncio
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal

from app.db.models.customers import Customer
from app.db.models.employee_projects import EmployeeProject
from app.db.models.employee_skills import EmployeeSkill
from app.db.models.employees import Employee
from app.db.models.projects import Project
from app.db.models.skills import Skill


# =============================================================================
# Seed data
# =============================================================================

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
    {
        "employee_id": "emp_004",
        "first_name": "Sara",
        "last_name": "Bakker",
        "job_title": "Data Engineer",
        "department": "Data & AI",
        "skills": [
            {
                "name": "Python",
                "proficiency": "advanced",
                "years_experience": 4,
            },
            {
                "name": "Apache Airflow",
                "proficiency": "expert",
                "years_experience": 4,
            },
            {
                "name": "dbt",
                "proficiency": "expert",
                "years_experience": 3,
            },
            {
                "name": "Snowflake",
                "proficiency": "advanced",
                "years_experience": 3,
            },
        ],
    },
    {
        "employee_id": "emp_005",
        "first_name": "Michael",
        "last_name": "Chen",
        "job_title": "DevOps Engineer",
        "department": "Cloud & Platform",
        "skills": [
            {
                "name": "AWS",
                "proficiency": "advanced",
                "years_experience": 5,
            },
            {
                "name": "Kubernetes",
                "proficiency": "expert",
                "years_experience": 5,
            },
            {
                "name": "Terraform",
                "proficiency": "expert",
                "years_experience": 5,
            },
            {
                "name": "GitHub Actions",
                "proficiency": "advanced",
                "years_experience": 3,
            },
        ],
    },
    {
        "employee_id": "emp_006",
        "first_name": "Priya",
        "last_name": "Nair",
        "job_title": "Solution Architect",
        "department": "Architecture",
        "skills": [
            {
                "name": "Azure",
                "proficiency": "expert",
                "years_experience": 8,
            },
            {
                "name": "AWS",
                "proficiency": "advanced",
                "years_experience": 6,
            },
            {
                "name": "Kubernetes",
                "proficiency": "advanced",
                "years_experience": 5,
            },
            {
                "name": "Terraform",
                "proficiency": "advanced",
                "years_experience": 5,
            },
        ],
    },
    {
        "employee_id": "emp_007",
        "first_name": "Lars",
        "last_name": "Visser",
        "job_title": "Technical Project Manager",
        "department": "Delivery",
        "skills": [
            {
                "name": "Scrum",
                "proficiency": "expert",
                "years_experience": 7,
            },
            {
                "name": "Stakeholder Management",
                "proficiency": "expert",
                "years_experience": 8,
            },
            {
                "name": "Cloud Migration",
                "proficiency": "advanced",
                "years_experience": 5,
            },
        ],
    },
]


CUSTOMERS = [
    {
        "customer_id": "cus_001",
        "name": "ACME Bank",
        "industry": "Financial Services",
    },
    {
        "customer_id": "cus_002",
        "name": "Globex Logistics",
        "industry": "Logistics",
    },
    {
        "customer_id": "cus_003",
        "name": "Contoso Retail",
        "industry": "Retail & E-commerce",
    },
    {
        "customer_id": "cus_004",
        "name": "Initech Health",
        "industry": "Healthcare",
    },
]


PROJECTS = [
    {
        "project_id": "proj_001",
        "customer_id": "cus_001",
        "name": "ACME Cloud Migration",
        "status": "active",
    },
    {
        "project_id": "proj_002",
        "customer_id": "cus_001",
        "name": "ACME Data Platform",
        "status": "completed",
    },
    {
        "project_id": "proj_003",
        "customer_id": "cus_002",
        "name": "Globex AI Assistant",
        "status": "active",
    },
    {
        "project_id": "proj_004",
        "customer_id": "cus_002",
        "name": "Globex Logistics Optimization",
        "status": "active",
    },
    {
        "project_id": "proj_005",
        "customer_id": "cus_003",
        "name": "Contoso API Platform",
        "status": "active",
    },
    {
        "project_id": "proj_006",
        "customer_id": "cus_003",
        "name": "Contoso Analytics Modernization",
        "status": "completed",
    },
    {
        "project_id": "proj_007",
        "customer_id": "cus_004",
        "name": "Initech Secure Cloud Foundation",
        "status": "active",
    },
]


EMPLOYEE_PROJECTS = [
    {
        "employee_id": "emp_001",
        "project_id": "proj_001",
        "role": "Cloud Consultant",
        "allocation_percentage": 80,
        "start_date": date(2026, 1, 12),
        "end_date": None,
    },
    {
        "employee_id": "emp_001",
        "project_id": "proj_007",
        "role": "Cloud Advisor",
        "allocation_percentage": 20,
        "start_date": date(2026, 6, 1),
        "end_date": None,
    },
    {
        "employee_id": "emp_002",
        "project_id": "proj_005",
        "role": "Lead Backend Engineer",
        "allocation_percentage": 70,
        "start_date": date(2026, 2, 2),
        "end_date": None,
    },
    {
        "employee_id": "emp_002",
        "project_id": "proj_003",
        "role": "Backend Integration Engineer",
        "allocation_percentage": 30,
        "start_date": date(2026, 5, 4),
        "end_date": None,
    },
    {
        "employee_id": "emp_003",
        "project_id": "proj_003",
        "role": "AI Engineer",
        "allocation_percentage": 80,
        "start_date": date(2026, 3, 2),
        "end_date": None,
    },
    {
        "employee_id": "emp_003",
        "project_id": "proj_002",
        "role": "AI & Retrieval Consultant",
        "allocation_percentage": 20,
        "start_date": date(2025, 8, 1),
        "end_date": date(2026, 2, 27),
    },
    {
        "employee_id": "emp_004",
        "project_id": "proj_002",
        "role": "Data Engineer",
        "allocation_percentage": 100,
        "start_date": date(2025, 5, 1),
        "end_date": date(2026, 2, 27),
    },
    {
        "employee_id": "emp_004",
        "project_id": "proj_004",
        "role": "Senior Data Engineer",
        "allocation_percentage": 100,
        "start_date": date(2026, 3, 2),
        "end_date": None,
    },
    {
        "employee_id": "emp_005",
        "project_id": "proj_001",
        "role": "DevOps Engineer",
        "allocation_percentage": 60,
        "start_date": date(2026, 1, 12),
        "end_date": None,
    },
    {
        "employee_id": "emp_005",
        "project_id": "proj_007",
        "role": "Platform Engineer",
        "allocation_percentage": 40,
        "start_date": date(2026, 6, 1),
        "end_date": None,
    },
    {
        "employee_id": "emp_006",
        "project_id": "proj_001",
        "role": "Solution Architect",
        "allocation_percentage": 30,
        "start_date": date(2026, 1, 5),
        "end_date": None,
    },
    {
        "employee_id": "emp_006",
        "project_id": "proj_007",
        "role": "Lead Solution Architect",
        "allocation_percentage": 70,
        "start_date": date(2026, 5, 18),
        "end_date": None,
    },
    {
        "employee_id": "emp_007",
        "project_id": "proj_004",
        "role": "Technical Project Manager",
        "allocation_percentage": 50,
        "start_date": date(2026, 2, 16),
        "end_date": None,
    },
    {
        "employee_id": "emp_007",
        "project_id": "proj_005",
        "role": "Technical Project Manager",
        "allocation_percentage": 50,
        "start_date": date(2026, 2, 2),
        "end_date": None,
    },
]


# =============================================================================
# Skills / employees
# =============================================================================

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

        db.add(
            EmployeeSkill(
                employee_id=employee.id,
                skill_id=skill.id,
                proficiency=skill_data["proficiency"],
                years_experience=skill_data["years_experience"],
            )
        )

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


# =============================================================================
# Customers
# =============================================================================

async def get_customer_by_customer_id(
    db: AsyncSession,
    customer_id: str,
) -> Customer | None:
    result = await db.execute(
        select(Customer).where(
            Customer.customer_id == customer_id
        )
    )

    return result.scalar_one_or_none()


async def seed_customers(
    db: AsyncSession,
) -> None:
    for data in CUSTOMERS:
        customer = await get_customer_by_customer_id(
            db=db,
            customer_id=data["customer_id"],
        )

        if customer is not None:
            print(
                f"Customer already exists: {customer.name}"
            )
            continue

        customer = Customer(
            customer_id=data["customer_id"],
            name=data["name"],
            industry=data["industry"],
        )

        db.add(customer)
        await db.flush()

        print(
            f"Added customer: {customer.name}"
        )


# =============================================================================
# Projects
# =============================================================================

async def get_project_by_project_id(
    db: AsyncSession,
    project_id: str,
) -> Project | None:
    result = await db.execute(
        select(Project).where(
            Project.project_id == project_id
        )
    )

    return result.scalar_one_or_none()


async def seed_projects(
    db: AsyncSession,
) -> None:
    for data in PROJECTS:
        project = await get_project_by_project_id(
            db=db,
            project_id=data["project_id"],
        )

        if project is not None:
            print(
                f"Project already exists: {project.name}"
            )
            continue

        customer = await get_customer_by_customer_id(
            db=db,
            customer_id=data["customer_id"],
        )

        if customer is None:
            raise RuntimeError(
                f"Customer {data['customer_id']} does not exist "
                f"for project {data['project_id']}"
            )

        project = Project(
            project_id=data["project_id"],
            customer_fk=customer.id,
            name=data["name"],
            status=data["status"],
        )

        db.add(project)
        await db.flush()

        print(
            f"Added project: {project.name}"
        )


# =============================================================================
# Employee ↔ Project assignments
# =============================================================================

async def employee_project_exists(
    db: AsyncSession,
    employee_id: int,
    project_id: int,
) -> bool:
    result = await db.execute(
        select(EmployeeProject).where(
            EmployeeProject.employee_id == employee_id,
            EmployeeProject.project_id == project_id,
        )
    )

    return result.scalar_one_or_none() is not None


async def seed_employee_projects(
    db: AsyncSession,
) -> None:
    for data in EMPLOYEE_PROJECTS:
        employee = await get_employee_by_employee_id(
            db=db,
            employee_id=data["employee_id"],
        )

        if employee is None:
            raise RuntimeError(
                f"Employee {data['employee_id']} does not exist"
            )

        project = await get_project_by_project_id(
            db=db,
            project_id=data["project_id"],
        )

        if project is None:
            raise RuntimeError(
                f"Project {data['project_id']} does not exist"
            )

        exists = await employee_project_exists(
            db=db,
            employee_id=employee.id,
            project_id=project.id,
        )

        if exists:
            print(
                f"Project assignment already exists: "
                f"{employee.first_name} {employee.last_name} "
                f"→ {project.name}"
            )
            continue

        assignment = EmployeeProject(
            employee_id=employee.id,
            project_id=project.id,
            role=data["role"],
            allocation_percentage=data["allocation_percentage"],
            start_date=data["start_date"],
            end_date=data["end_date"],
        )

        db.add(assignment)

        print(
            f"Added project assignment: "
            f"{employee.first_name} {employee.last_name} "
            f"→ {project.name}"
        )


# =============================================================================
# Main
# =============================================================================

async def main():
    async with SessionLocal() as db:
        try:
            # Order matters because later entities reference earlier ones.
            await seed_employees(db)
            await seed_customers(db)
            await seed_projects(db)
            await seed_employee_projects(db)

            await db.commit()

            print()
            print("Northstar seed completed successfully.")

        except Exception:
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
    