from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from typing import TYPE_CHECKING

from app.api.dependencies.auth import get_current_user, get_db
from app.api.schemas.chats import AskRequest, AskResponse
from app.crud.chats import create_chat, get_user_chat
from app.services.chat_service import answer_chat_message, AnswerGenerationError

if TYPE_CHECKING:
    from app.models.users import User


router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/chats", response_model=AskResponse, status_code=201)
async def chats(
    request: Request,
    ask_request: AskRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AskResponse:
    """
    Creates a new chat in db, add query to db, sends query to RAG llm, add response to db, return answer
    """
    chat = await create_chat(db, title=ask_request.query, user=user)

    try:
        return await answer_chat_message(db, request.app.state.answer_svc, chat, ask_request.query)
    except AnswerGenerationError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer",
        )


@router.post("/chats/{chat_id}/messages", response_model=AskResponse, status_code=201)
async def add_message(
    request: Request,
    ask_request: AskRequest,
    chat_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AskResponse:
    """
    Look for chat with chat_id in db, raise on not found, add query + response to db, 
    otherwise send chat context + query to RAG llm, return answer
    """
    chat = await get_user_chat(db, user, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    try:
        return await answer_chat_message(db, request.app.state.answer_svc, chat, ask_request.query)
    except AnswerGenerationError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer",
        )
