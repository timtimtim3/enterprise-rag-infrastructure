from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from typing import TYPE_CHECKING

from app.api.dependencies.auth import get_current_user, get_db
from app.api.schemas.chats import AskRequest, AskResponse, ChatInfo, ListChatsResponse, ListMessageSourcesResponse, ListMessagesResponse, MessageInfo, MessageSourceInfo
from app.crud.chats import create_chat as crud_create_chat, delete_chat as crud_delete_chat, get_chat_message, get_chat_messages, get_message_sources, get_user_chat, get_user_chats
from app.services.chat_service import answer_chat_message, AnswerGenerationError

if TYPE_CHECKING:
    from app.models.users import User


router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("", response_model=AskResponse, status_code=201)
async def create_chat(
    request: Request,
    ask_request: AskRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> AskResponse:
    """
    Creates a new chat in db, add query to db, sends query to RAG llm, add response to db, return answer
    """
    chat = await crud_create_chat(db, title=ask_request.query, user=user)

    try:
        return await answer_chat_message(db, request.app.state.answer_svc, chat, ask_request.query)
    except AnswerGenerationError:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer",
        )


@router.post("/{chat_id}/messages", response_model=AskResponse, status_code=201)
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


@router.get("", response_model=ListChatsResponse)
async def list_chats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> ListChatsResponse:
    chats = await get_user_chats(db, user)
    return ListChatsResponse(
        chats=[ChatInfo.model_validate(chat) for chat in chats]
    )


@router.get("/{chat_id}/messages", response_model=ListMessagesResponse)
async def list_messages(
    chat_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ListMessagesResponse:
    chat = await get_user_chat(db, user, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_messages = await get_chat_messages(db, chat)
    return ListMessagesResponse(
        messages=[MessageInfo.model_validate(message) for message in chat_messages]
    )


@router.get("/{chat_id}/messages/{message_id}/sources", response_model=ListMessageSourcesResponse)
async def list_message_sources(
    chat_id: str,
    message_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ListMessageSourcesResponse:
    chat = await get_user_chat(db, user, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_message = await get_chat_message(db, chat, message_id)
    if chat_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    sources = await get_message_sources(db, chat_message)
    return ListMessageSourcesResponse(
        message_sources=[MessageSourceInfo.model_validate(source) for source in sources]
    )


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(chat_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> None:
    chat = await get_user_chat(db, user, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    await crud_delete_chat(db, chat)
