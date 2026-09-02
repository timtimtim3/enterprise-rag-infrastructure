# app/agents/tools/projects.py

from typing import Literal, TypedDict

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from app.agents.state import AgentContext
from app.db.crud.projects import get_team_for_project, get_projects_by_name


class ProjectInfo(TypedDict):
    project_id: str
    name: str
    status: str
    customer_id: str
    customer_name: str


class ProjectLookupResult(TypedDict):
    status: Literal[
        "found",
        "ambiguous",
        "not_found",
    ]
    matches: list[ProjectInfo]


class ProjectTeamMember(TypedDict):
    employee_id: str
    first_name: str
    last_name: str
    job_title: str
    department: str | None
    project_role: str | None
    allocation_percentage: int | None
    start_date: str | None
    end_date: str | None


class ProjectTeamResult(TypedDict):
    status: Literal[
        "found",
        "no_team",
        "project_not_found",
    ]
    project_id: str
    members: list[ProjectTeamMember]


@tool
async def lookup_project(
    name: str,
    runtime: ToolRuntime[AgentContext],
) -> ProjectLookupResult:
    """
    Search company projects by project name.

    Use this to resolve a project's identity when the user refers to
    a project by name rather than by project_id.

    Multiple projects may have similar names, so customer information
    is returned to help disambiguate matches.
    """

    async with runtime.context.db_session_factory() as db:
        results = await get_projects_by_name(
            db=db,
            name=name,
        )

        matches = [
            {
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status,
                "customer_id": customer.customer_id,
                "customer_name": customer.name,
            }
            for project, customer in results
        ]

    if not matches:
        status = "not_found"
    elif len(matches) == 1:
        status = "found"
    else:
        status = "ambiguous"

    return {
        "status": status,
        "matches": matches,
    }


@tool
async def get_project_team(
    project_id: str,
    runtime: ToolRuntime[AgentContext],
) -> ProjectTeamResult:
    """
    Get employees assigned to a specific company project.

    Requires the project's unique project_id.
    """

    async with runtime.context.db_session_factory() as db:
        project, assignments = await get_team_for_project(
            db=db,
            project_id=project_id,
        )

        if project is None:
            return {
                "status": "project_not_found",
                "project_id": project_id,
                "members": [],
            }

        members = [
            {
                "employee_id": employee.employee_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "job_title": employee.job_title,
                "department": employee.department,
                "project_role": assignment.role,
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
            for assignment, employee in assignments
        ]

    return {
        "status": "found" if members else "no_team",
        "project_id": project_id,
        "members": members,
    }
