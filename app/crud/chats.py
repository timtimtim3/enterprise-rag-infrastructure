from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING, Optional

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


async def get_user_chat(db: AsyncSession, user: User, chat_id: str) -> Optional[Chat]:
    result = await db.execute(
        select(Chat).where(Chat.user_fk == user.id, Chat.chat_id == chat_id)
    )
    return result.scalar_one_or_none()
