from typing import Literal, TypedDict, cast

from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from app.agents.state import AgentContext
from app.db.crud.auth import get_user_by_user_id
from app.db.crud.support import create_support_ticket_record
from app.domain.support import SupportTicketPriority


class SupportTicketResult(TypedDict):
    status: Literal["created", "user_not_found"]
    ticket_id: str | None
    title: str
    priority: SupportTicketPriority


@tool
async def create_support_ticket(
    title: str,
    description: str,
    runtime: ToolRuntime[AgentContext],
    priority: SupportTicketPriority = "normal",
) -> SupportTicketResult:
    """
    Create an internal company IT support ticket.

    Only use this when the user explicitly asks to create, open, or file
    a support ticket. Do not call it merely because the user describes
    a technical problem.

    Required information must be sufficiently clear before creating the ticket.
    """

    async with runtime.context.db_session_factory() as db:
        user = await get_user_by_user_id(
            db=db,
            user_id=runtime.context.user_id,
        )

        if user is None:
            return {
                "status": "user_not_found",
                "ticket_id": None,
                "title": title,
                "priority": priority,
            }

        ticket = await create_support_ticket_record(
            db=db,
            title=title,
            description=description,
            priority=priority,
            requester=user,
        )

    return {
        "status": "created",
        "ticket_id": ticket.ticket_id,
        "title": ticket.title,
        "priority": cast(SupportTicketPriority, ticket.priority),
    }
