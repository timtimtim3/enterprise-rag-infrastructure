from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


async def create_user(db: AsyncSession, name: str, email: str, password_hash: str):
    user = User(username=name, email=email, password_hash=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # updates the Python user object
    return user
