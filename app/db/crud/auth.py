from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, timezone

from app.db.models.users import User 
from app.db.models.sessions import Session
from app.core.config import SESSION_EXPIRE_SECONDS


async def create_user(db: AsyncSession, username: str, email: str, password_hash: str) -> User:
    user = User(username=username, email=email, password_hash=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # updates the Python user object
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_session_by_id(db: AsyncSession, session_id: str) -> Session | None:
    result = await db.execute(
        select(Session).options(selectinload(Session.user)).where(Session.session_id == session_id)
    )
    return result.scalar_one_or_none()


async def create_session(db: AsyncSession, session_id: str, user_fk: int) -> Session:
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=SESSION_EXPIRE_SECONDS
    )

    session = Session(
        session_id=session_id,
        user_fk=user_fk,
        expires_at=expires_at,
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def delete_session_by_id(db: AsyncSession, session_id: str) -> bool:
    result = await db.execute(
        select(Session).where(Session.session_id == session_id)
    )
    session = result.scalar_one_or_none()

    if session is None:
        return False
    
    await db.delete(session)
    await db.commit()
    return True


async def delete_session(db: AsyncSession, session: Session) -> bool:
    if session is None:
        return False
    
    await db.delete(session)
    await db.commit()
    return True
