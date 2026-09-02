# app/agents/tools/customers.py

from __future__ import annotations

from typing import Literal, TypedDict

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from app.agents.state import AgentContext
from app.db.crud.customers import (
    get_customers_by_name,
    get_projects_by_customer_id,
)


class CustomerInfo(TypedDict):
    customer_id: str
    name: str
    industry: str | None


class CustomerLookupResult(TypedDict):
    status: Literal[
        "found",
        "ambiguous",
        "not_found",
    ]
    matches: list[CustomerInfo]


class CustomerProjectInfo(TypedDict):
    project_id: str
    name: str
    status: str


class CustomerProjectsResult(TypedDict):
    status: Literal[
        "found",
        "no_projects",
        "customer_not_found",
    ]
    customer_id: str
    projects: list[CustomerProjectInfo]


@tool
async def lookup_customer(
    name: str,
    runtime: ToolRuntime[AgentContext],
) -> CustomerLookupResult:
    """
    Search the company's customer directory by customer name.

    Use this when the user asks about a customer, account, client,
    or customer-specific information.
    """

    async with runtime.context.db_session_factory() as db:
        customers = await get_customers_by_name(
            db=db,
            name=name,
        )

        matches = [
            {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "industry": customer.industry,
            }
            for customer in customers
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
async def get_customer_projects(
    customer_id: str,
    runtime: ToolRuntime[AgentContext],
) -> CustomerProjectsResult:
    """
    Get projects belonging to a specific company customer.

    Requires the customer's unique customer_id. Use lookup_customer
    first when only the customer name is known.
    """

    async with runtime.context.db_session_factory() as db:
        customer, projects = await get_projects_by_customer_id(
            db=db,
            customer_id=customer_id,
        )

        if customer is None:
            return {
                "status": "customer_not_found",
                "customer_id": customer_id,
                "projects": [],
            }

        project_infos = [
            {
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status,
            }
            for project in projects
        ]

    return {
        "status": "found" if project_infos else "no_projects",
        "customer_id": customer_id,
        "projects": project_infos,
    }
