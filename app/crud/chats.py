from __future__ import annotations
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING, Optional

from app.models.chats import Chat, Message, MessageSource

if TYPE_CHECKING:
    from app.models.users import User
    from app.api.schemas.chats import SourceCreate, MessageCreate


async def create_chat(db: AsyncSession, title: str, user: User) -> Chat:
    chat = Chat(title=title, user=user)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


async def create_message(db: AsyncSession, chat: Chat, message_create: MessageCreate) -> Message:
    message = Message(
        chat=chat,
        **message_create.model_dump(),
    )
    db.add(message)
    chat.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(message)
    await db.refresh(chat)
    return message


async def create_message_source(
    db: AsyncSession,
    message: Message,
    source: SourceCreate,
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


async def get_user_chats(db: AsyncSession, user: User) -> list[Chat]:
    result = await db.execute(
        select(Chat).where(Chat.user_fk == user.id).order_by(Chat.updated_at.desc())
    )
    return result.scalars().all()


async def get_chat_messages(db: AsyncSession, chat: Chat) -> list[Message]:
    result = await db.execute(
        select(Message).where(Message.chat_fk == chat.id).order_by(Message.created_at.asc())
    )
    return result.scalars().all()


async def get_chat_message(db: AsyncSession, chat: Chat, message_id: str) -> Optional[Message]:
    result = await db.execute(
        select(Message).where(Message.chat_fk == chat.id, Message.message_id == message_id)
    )
    return result.scalar_one_or_none()


async def get_message_sources(db: AsyncSession, message: Message) -> list[MessageSource]:
    result = await db.execute(
        select(MessageSource).where(MessageSource.message_fk == message.id).order_by(MessageSource.source_index.asc())
    )
    return result.scalars().all()


async def delete_chat(db: AsyncSession, chat: Chat) -> bool:
    if chat is None:
        return False
    
    await db.delete(chat)
    await db.commit()
    return True


async def touch_chat(db: AsyncSession, chat: Chat) -> None:
    chat.updated_at = datetime.now(timezone.utc)
    await db.commit()
    