from __future__ import annotations

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.concurrency import run_in_threadpool
from typing import TYPE_CHECKING

from app.api.dependencies.auth import get_current_user
from app.api.schemas.chats import AskRequest, AskResponse

if TYPE_CHECKING:
    from app.models.chats import User


router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/chats", response_model=AskResponse)
async def chats(request: Request, ask_request: AskRequest, user: User = Depends(get_current_user)) -> AskResponse:
    """
    Creates a new chat in db, add query to db, sends query to RAG llm, add response to db, return answer
    """
    try:
        answer = await run_in_threadpool(request.app.state.answer_svc.answer_question, ask_request.query)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate answer")


@router.post("/chats/{chat_id}/messages", response_model=AskResponse)
async def add_message(request: Request, ask_request: AskRequest, chat_id: str, user: User = Depends(get_current_user)) -> AskResponse:
    """
    Look for chat with chat_id in db, raise on not found, add query + response to db, otherwise send chat context + query to RAG llm, return answer
    """
    try:
        answer = await run_in_threadpool(request.app.state.answer_svc.answer_question, ask_request.query)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate answer")
