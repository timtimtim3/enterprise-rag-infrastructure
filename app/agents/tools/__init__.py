from app.agents.tools.customers import (
    get_customer_projects,
    lookup_customer,
)
from app.agents.tools.employees import (
    find_expert,
    get_employee_projects,
    get_employee_skills,
    lookup_employee,
)
from app.agents.tools.knowledge import build_knowledge_tools
from app.agents.tools.projects import get_project_team, lookup_project
from app.agents.tools.support import create_support_ticket


def build_agent_tools(retriever):
    knowledge_tools = build_knowledge_tools(retriever)

    return [
        *knowledge_tools,
        lookup_employee,
        get_employee_skills,
        find_expert,
        get_employee_projects,
        lookup_customer,
        get_customer_projects,
        lookup_project,
        get_project_team,
        create_support_ticket,
    ]