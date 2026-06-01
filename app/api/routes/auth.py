from fastapi import APIRouter, HTTPException

from app.crud.auth import create_user


router = APIRouter(prefix="auth", tags=["auth"])



@router.post("sing_up")
async def sign_up(username: str, email: str, password: str):
    try:
        create_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail="")


@router.post("sing_in")
async def sign_in():
    pass
