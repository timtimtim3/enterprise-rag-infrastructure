from __future__ import annotations

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.db.session import get_db
from app.db.crud.auth import get_session_by_id, delete_session

if TYPE_CHECKING:
    from app.db.models import User


async def get_current_user(
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = await get_session_by_id(
        db,
        session_id,
    )

    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if session.expires_at < datetime.now(timezone.utc):
        await delete_session(db, session)
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user
