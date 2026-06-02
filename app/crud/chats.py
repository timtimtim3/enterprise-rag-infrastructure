from __future__ import annotations

from sqlalchemy import select, func, Row
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence
from typing import Any, TYPE_CHECKING

from app.models.chats import Chat, Message, MessageSource

if TYPE_CHECKING:
    from app.models.users import User
    from app.enums.message_role import MessageRole
    from app.api.schemas.chats import Source


async def create_chat(db: AsyncSession, title: str, user: User) -> Chat:
    chat = Chat(title=title, user=user)

    db.add(chat)
    await db.commit()
    await db.refresh(chat)

    return chat


async def create_message(db: AsyncSession, role: MessageRole, content: str, chat: Chat) -> Message:
    message = Message(role=role, content=content, chat=chat)

    db.add(message)
    await db.commit()
    await db.refresh(message)

    return message


async def create_message_source(
    db: AsyncSession,
    message: Message,
    source: Source,
) -> MessageSource:
    message_source = MessageSource(
        message=message,
        **source.model_dump(),
    )

    db.add(message_source)
    await db.commit()
    await db.refresh(message_source)

    return message_source
