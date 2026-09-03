# app/db/crud/support_tickets.py

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

from app.db.models.support_tickets import SupportTicket
from app.domain.support import SupportTicketPriority

if TYPE_CHECKING:
    from app.db.models.users import User


async def create_support_ticket(
    db: AsyncSession,
    *,
    title: str,
    description: str,
    priority: SupportTicketPriority,
    requester: User,
) -> SupportTicket:
    ticket = SupportTicket(
        title=title,
        description=description,
        priority=priority,
        status="open",
        requester=requester,
    )

    db.add(ticket)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(ticket)

    return ticket
