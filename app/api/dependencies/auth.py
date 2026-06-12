from __future__ import annotations

from fastapi import Cookie, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from app.core.config import JWT_ALGORITHM, JWT_SECRET_KEY
from app.core.redis import get_redis
from app.core.security import hash_refresh_token, verify_access_token
from app.db.session import get_db
from app.db.crud.auth import get_refresh_token_by_hash, get_session_by_id, delete_session, get_user_by_user_id

if TYPE_CHECKING:
    from app.db.models import User


bearer_scheme = HTTPBearer(auto_error=False)


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
    
    if session.expires_at <= datetime.now(timezone.utc):
        await delete_session(db, session)
        raise HTTPException(status_code=401, detail="Session expired")

    return session.user


async def get_current_user_jwt(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Verify type, sub, jti, exp, iat
        payload = verify_access_token(credentials.credentials, secret_key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except ValueError:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    jti = payload["jti"]
    if await redis.exists(f"revoked_access_token:{jti}"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = payload["sub"]
    user = await get_user_by_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user


async def get_current_user_refresh(
    refresh_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    refresh_token_hash = hash_refresh_token(refresh_token)
    refresh_token_db = await get_refresh_token_by_hash(db, refresh_token_hash)
    
    if not refresh_token_db:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if refresh_token_db.revoked_at is not None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if refresh_token_db.expires_at <= datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Not authenticated")

    return refresh_token_db.user
