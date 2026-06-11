from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, timezone

from app.db.models.users import User 
from app.db.models.sessions import RefreshToken, Session
from app.core.config import REFRESH_TOKEN_EXPIRE_SECONDS, SESSION_EXPIRE_SECONDS


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


async def get_user_by_user_id(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(
        select(User).where(User.user_id == user_id)
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


async def create_refresh_token(db: AsyncSession, token_id: str, token_hash: str, user_fk: int) -> RefreshToken:
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=REFRESH_TOKEN_EXPIRE_SECONDS
    )

    refresh_token = RefreshToken(
        token_id=token_id,
        token_hash=token_hash,
        user_fk=user_fk,
        expires_at=expires_at,
    )
    
    db.add(refresh_token)
    await db.commit()
    await db.refresh(refresh_token)
    return refresh_token


async def delete_refresh_token_by_hash(db: AsyncSession, token_hash: str) -> bool:
    if token_hash is None:
        return False
    
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    )
    refresh_token = result.scalar_one_or_none()
    if refresh_token is None:
        return False
    
    await db.delete(refresh_token)
    await db.commit()
    return True


async def revoke_refresh_token_by_hash(db: AsyncSession, token_hash: str) -> bool:
    if token_hash is None:
        return False
    
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token_hash == token_hash)
    )
    refresh_token = result.scalar_one_or_none()

    if refresh_token is None:
        return False
    
    refresh_token.revoked_at = datetime.now(timezone.utc)
    
    await db.commit()
    return True


async def get_refresh_token_by_hash(db: AsyncSession, token_hash: str) -> RefreshToken | None:
    result = await db.execute(
        select(RefreshToken).options(selectinload(RefreshToken.user)).where(RefreshToken.token_hash == token_hash)
    )
    return result.scalar_one_or_none()
