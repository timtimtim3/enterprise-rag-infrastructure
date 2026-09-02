from __future__ import annotations

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from typing import Literal, TypedDict, TYPE_CHECKING

from app.agents.state import AgentContext
from app.db.crud.employees import find_employees_with_skill, get_employee_with_skills, get_employees_by_name, get_projects_for_employee

if TYPE_CHECKING:
    from app.db.models.employees import Employee


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


class EmployeeSkillInfo(TypedDict):
    name: str
    proficiency: str | None
    years_experience: int | None


class EmployeeSkillsResult(TypedDict):
    status: Literal[
        "found",
        "not_found",
        "no_skills",
    ]
    employee_id: str
    skills: list[EmployeeSkillInfo]


class ExpertInfo(TypedDict):
    employee_id: str
    first_name: str
    last_name: str
    job_title: str
    department: str | None
    skill: str
    proficiency: str | None
    years_experience: int | None


class FindExpertResult(TypedDict):
    status: Literal["found", "no_match"]
    matches: list[ExpertInfo]


class EmployeeProjectInfo(TypedDict):
    project_id: str
    project_name: str
    customer_id: str
    customer_name: str
    project_status: str
    role: str | None
    allocation_percentage: int | None
    start_date: str | None
    end_date: str | None


class EmployeeProjectsResult(TypedDict):
    status: Literal[
        "found",
        "no_projects",
        "employee_not_found",
    ]
    employee_id: str
    projects: list[EmployeeProjectInfo]


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
    Search the employee directory by first name, last name,
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
async def get_employee_skills(
    employee_id: str,
    runtime: ToolRuntime[AgentContext],
) -> EmployeeSkillsResult:
    """
    Get the skills associated with a specific employee.

    Use this after resolving the employee's identity with lookup_employee.
    """

    async with runtime.context.db_session_factory() as db:
        employee = await get_employee_with_skills(
            db=db,
            employee_id=employee_id,
        )

        if employee is None:
            return {
                "status": "not_found",
                "employee_id": employee_id,
                "skills": [],
            }

        skills = [
            {
                "name": employee_skill.skill.name,
                "proficiency": employee_skill.proficiency,
                "years_experience": employee_skill.years_experience,
            }
            for employee_skill in employee.employee_skills
        ]

    return {
        "status": "found" if skills else "no_skills",
        "employee_id": employee_id,
        "skills": skills,
    }


@tool
async def find_expert(
    skill: str,
    runtime: ToolRuntime[AgentContext],
) -> FindExpertResult:
    """
    Find employees with expertise in a technology or skill.

    Use this when someone needs an internal expert, consultant,
    engineer, or colleague with specific technical experience.
    """

    async with runtime.context.db_session_factory() as db:
        results = await find_employees_with_skill(
            db=db,
            skill=skill,
        )

        matches = [
            {
                "employee_id": employee.employee_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "job_title": employee.job_title,
                "department": employee.department,
                "skill": db_skill.name,
                "proficiency": employee_skill.proficiency,
                "years_experience": employee_skill.years_experience,
            }
            for employee, employee_skill, db_skill in results
        ]

    return {
        "status": "found" if matches else "no_match",
        "matches": matches,
    }


@tool
async def get_employee_projects(
    employee_id: str,
    runtime: ToolRuntime[AgentContext],
) -> EmployeeProjectsResult:
    """
    Get project assignments for a specific company employee.

    Includes current and historical project assignments. Requires the
    employee's unique employee_id. Use lookup_employee first when only
    the employee's name is known.
    """

    async with runtime.context.db_session_factory() as db:
        employee, assignments = await get_projects_for_employee(
            db=db,
            employee_id=employee_id,
        )

        if employee is None:
            return {
                "status": "employee_not_found",
                "employee_id": employee_id,
                "projects": [],
            }

        projects = [
            {
                "project_id": project.project_id,
                "project_name": project.name,
                "customer_id": customer.customer_id,
                "customer_name": customer.name,
                "project_status": project.status,
                "role": assignment.role,
                "allocation_percentage": assignment.allocation_percentage,
                "start_date": (
                    assignment.start_date.isoformat()
                    if assignment.start_date
                    else None
                ),
                "end_date": (
                    assignment.end_date.isoformat()
                    if assignment.end_date
                    else None
                ),
            }
            for assignment, project, customer in assignments
        ]

    return {
        "status": "found" if projects else "no_projects",
        "employee_id": employee_id,
        "projects": projects,
    }
