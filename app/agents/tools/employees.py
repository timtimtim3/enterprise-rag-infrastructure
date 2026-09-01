from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from app.agents.state import AgentContext
from app.db.crud.employees import get_employees_by_name


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


@tool
async def lookup_employee(name: str, runtime: ToolRuntime[AgentContext]) -> dict:
    """
    Search the Northstar employee directory by first name, last name,
    or full name.

    Multiple employees may have the same first or last name.
    """

    async with runtime.context.db_session_factory() as db:
        matches = await get_employees_by_name(
            db=db,
            name=name
        )

    if not matches:
        return {
            "status": "not_found",
            "matches": [],
        }

    employees = [
        {
            "employee_id": employee.employee_id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
        }
        for employee in matches
    ]

    if len(employees) > 1:
        return {
            "status": "ambiguous",
            "matches": employees,
        }

    return {
        "status": "found",
        "employee": employees[0],
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
