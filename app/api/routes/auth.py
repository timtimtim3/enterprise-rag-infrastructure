from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

from app.api.dependencies.auth import get_current_user, get_current_user_jwt, get_current_user_refresh
from app.db.session import get_db
from app.api.schemas.auth import LoginJWTResponse, RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, UserInfo
from app.db.crud.auth import create_refresh_token, create_user, delete_session_by_id, get_user_by_email, get_user_by_username, create_session, revoke_refresh_token_by_hash
from app.core.security import create_access_token, gen_refresh_token, hash_password, hash_refresh_token, verify_password
from app.core.config import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    DUMMY_PASSWORD_HASH,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_SECONDS,
    SESSION_EXPIRE_SECONDS,
)

if TYPE_CHECKING:
    from app.db.models.users import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=RegisterResponse, status_code=201)
async def sign_up(register_request: RegisterRequest, db: AsyncSession = Depends(get_db)) -> RegisterResponse:
    hashed_password = hash_password(register_request.password)

    existing_user = await get_user_by_email(
        db,
        register_request.email,
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Could not register with details",
        )

    existing_user = await get_user_by_username(
        db,
        register_request.username,
    )
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Could not register with details",
        )

    user = await create_user(db, register_request.username, register_request.email, hashed_password)
    return RegisterResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
    )


@router.post("/signin", response_model=LoginResponse)
async def sign_in(response: Response, login_request: LoginRequest, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    existing_user = await get_user_by_username(
        db,
        login_request.username,
    )

    if not existing_user:
        verify_password(login_request.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    verified = verify_password(login_request.password, existing_user.password_hash)
    if not verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )
    
    session_id = str(uuid.uuid4())
    await create_session(db, session_id, existing_user.id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=SESSION_EXPIRE_SECONDS,
    )
    
    return LoginResponse(
        user_id=existing_user.user_id,
        username=existing_user.username
    )


@router.get("/me", response_model=UserInfo)
async def get_me(user: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo.model_validate(user)


@router.post("/signout", status_code=204)
async def sign_out(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> None:
    session_id = request.cookies.get("session_id")
    if session_id is not None:
        await delete_session_by_id(db, session_id)

    response.delete_cookie(
        key="session_id",
        httponly=True,
        secure=False,
        samesite="lax",
    )


@router.post("/signin-jwt", response_model=LoginJWTResponse)
async def sign_in_jwt(response: Response, login_request: LoginRequest, db: AsyncSession = Depends(get_db)) -> LoginJWTResponse:
    existing_user = await get_user_by_username(
        db,
        login_request.username,
    )

    if not existing_user:
        verify_password(login_request.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    verified = verify_password(login_request.password, existing_user.password_hash)
    if not verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )
    
    refresh_token = gen_refresh_token()
    refresh_token_hash = hash_refresh_token(refresh_token)
    refresh_token_id = str(uuid.uuid4())
    await create_refresh_token(db, refresh_token_id, refresh_token_hash, existing_user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_SECONDS,
        path="/auth",
    )

    access_token = create_access_token(
        user_id=str(existing_user.user_id),
        username=existing_user.username,
        secret_key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
        expires_in_seconds=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
    
    return LoginJWTResponse(
        user_id=existing_user.user_id,
        username=existing_user.username,
        access_token=access_token,
    )


@router.get("/me-jwt", response_model=UserInfo)
async def get_me_jwt(user: User = Depends(get_current_user_jwt)) -> UserInfo:
    return UserInfo.model_validate(user)


@router.post("/signout-jwt", status_code=204)
async def sign_out_jwt(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> None:
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is not None:
        refresh_token_hash = hash_refresh_token(refresh_token)
        await revoke_refresh_token_by_hash(db, refresh_token_hash)

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=False,
        samesite="lax",
        path="/auth",
    )


@router.post("/refresh-jwt", response_model=LoginJWTResponse)
async def refresh_jwt(user: User = Depends(get_current_user_refresh)) -> LoginJWTResponse:
    access_token = create_access_token(
        user_id=str(user.user_id),
        username=user.username,
        secret_key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
        expires_in_seconds=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
    
    return LoginJWTResponse(
        user_id=user.user_id,
        username=user.username,
        access_token=access_token,
    )
