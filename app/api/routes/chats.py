from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.concurrency import run_in_threadpool
from typing import TYPE_CHECKING

from app.api.dependencies.auth import get_current_user, get_db
from app.api.schemas.chats import AskRequest, AskResponse, Source, Usage
from app.crud.chats import create_chat, create_message, create_message_source
from app.enums.message_role import MessageRole

if TYPE_CHECKING:
    from app.models.chats import User


router = APIRouter(prefix="/chats", tags=["chats"])


def sources_from_answer(source_dicts: list[dict]) -> list[Source]:
    sources = []
    for source_dict in source_dicts:
        source = Source(
            doc_id=source_dict["doc_id"],
            source_index=source_dict["source_index"],
            chunk_indices=source_dict["chunk_indices"],
            title=source_dict["title"],
            source_path=source_dict["source_path"],
            source_type=source_dict["source_type"],
            doc_type=source_dict["doc_type"],
        )
        sources.append(source)
    return sources


@router.post("/chats", response_model=AskResponse)
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
    query_message = await create_message(db, role=MessageRole.USER, content=ask_request.query, chat=chat)

    try:
        answer = await run_in_threadpool(request.app.state.answer_svc.answer_question, ask_request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate answer")
    
    answer_message = await create_message(db, role=MessageRole.ASSISTANT, content=answer["answer"], chat=chat)
    sources = sources_from_answer(answer["sources"])
    for source in sources:
        await create_message_source(db, message=answer_message, source=source)

    return AskResponse(
        chat_id=chat.chat_id,
        query_message_id=query_message.message_id,
        answer_message_id=answer_message.message_id,
        answer=answer["answer"],
        model=answer["model"],
        finish_reason=answer["finish_reason"],
        usage=Usage(
            completion_tokens=answer["usage"]["completion_tokens"],
            prompt_tokens=answer["usage"]["prompt_tokens"],
            total_tokens=answer["usage"]["total_tokens"],
        ),
        sources=sources,
    )


@router.post("/chats/{chat_id}/messages", response_model=AskResponse)
async def add_message(
    request: Request,
    ask_request: AskRequest,
    chat_id: str,
    user: User = Depends(get_current_user)
) -> AskResponse:
    """
    Look for chat with chat_id in db, raise on not found, add query + response to db, otherwise send chat context + query to RAG llm, return answer
    """
    try:
        answer = await run_in_threadpool(request.app.state.answer_svc.answer_question, ask_request.query)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate answer")
