from app.agents.tools.customers import (
    get_customer_projects,
    lookup_customer,
)
from app.agents.tools.employees import (
    find_expert,
    lookup_employee,
)
from app.agents.tools.knowledge import build_knowledge_tools
from app.agents.tools.support import create_support_ticket


def build_agent_tools(retriever):
    knowledge_tools = build_knowledge_tools(retriever)

    return [
        *knowledge_tools,
        lookup_employee,
        find_expert,
        lookup_customer,
        get_customer_projects,
        create_support_ticket,
    ]