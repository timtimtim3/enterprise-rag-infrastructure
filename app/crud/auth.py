import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


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
    return result.scalars.first()


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalars.first()
