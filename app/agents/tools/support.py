import uuid

from langchain_core.tools import tool


@tool
async def create_support_ticket(
    title: str,
    description: str,
    priority: str = "normal",
) -> dict:
    """
    Create an internal Northstar IT support ticket.

    Only use this when the user explicitly asks to create/open/file
    a support ticket. Do not call it merely because the user describes
    a technical problem.

    Required information must be sufficiently clear before creating the ticket.
    """

    # Fake implementation initially.
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "created",
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
    }
