from __future__ import annotations

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from typing import Literal, TypedDict, TYPE_CHECKING

from app.agents.state import AgentContext
from app.db.crud.employees import get_employees_by_name

if TYPE_CHECKING:
    from app.db.models.employees import Employee


EMPLOYEES = [
    {
        "employee_id": "emp_001",
        "name": "John Smith",
        "role": "Cloud Consultant",
        "skills": ["AWS", "Terraform", "Kubernetes"],
        "current_project": "ACME Cloud Migration",
    },
    {
        "employee_id": "emp_002",
        "name": "John de Vries",
        "role": "Backend Engineer",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "current_project": "Contoso API Platform",
    },
    {
        "employee_id": "emp_003",
        "name": "Alice Jansen",
        "role": "AI Engineer",
        "skills": ["Python", "RAG", "LangGraph", "Qdrant"],
        "current_project": "Globex AI Assistant",
    },
]


class EmployeeDirectoryInfo(TypedDict):
    employee_id: str
    first_name: str
    last_name: str
    job_title: str
    department: str | None


class EmployeeLookupResult(TypedDict):
    status: Literal[
        "found",
        "ambiguous",
        "not_found",
    ]
    matches: list[EmployeeDirectoryInfo]


def employee_to_directory_info(
    employee: Employee,
) -> EmployeeDirectoryInfo:
    return {
        "employee_id": employee.employee_id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "job_title": employee.job_title,
        "department": employee.department,
    }


@tool
async def lookup_employee(
    name: str,
    runtime: ToolRuntime[AgentContext],
) -> EmployeeLookupResult:
    """
    Search the Northstar employee directory by first name, last name,
    or full name.

    Use this to resolve an employee's identity or retrieve basic directory
    information. Multiple employees may have the same first or last name.
    """
    
    async with runtime.context.db_session_factory() as db:
        matches = await get_employees_by_name(
            db=db,
            name=name,
        )

        employees = [
            employee_to_directory_info(employee)
            for employee in matches
        ]

    if not employees:
        status = "not_found"
    elif len(employees) == 1:
        status = "found"
    else:
        status = "ambiguous"

    return {
        "status": status,
        "matches": employees,
    }


@tool
async def find_expert(skill: str) -> dict:
    """
    Find Northstar employees with expertise in a technology or skill.

    Use this when someone needs an internal expert, consultant,
    engineer, or colleague with specific technical experience.
    """

    matches = [
        employee
        for employee in EMPLOYEES
        if any(
            skill.lower() in employee_skill.lower()
            for employee_skill in employee["skills"]
        )
    ]

    return {
        "status": "found" if matches else "not_found",
        "matches": matches,
    }
