from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.concurrency import run_in_threadpool
from typing import TYPE_CHECKING

from app.api.schemas.chats import AskResponse
from app.api.schemas.mappers import construct_ask_response, sources_from_answer
from app.crud.chats import create_message, create_message_source
from app.enums.message_role import MessageRole

if TYPE_CHECKING:
    from app.models.chats import Chat


class AnswerGenerationError(Exception):
    pass


async def answer_chat_message(
    db: AsyncSession,
    answer_svc,
    chat: Chat,
    query: str,
) -> AskResponse:
    """
    Add query to db, sends query to RAG llm, add response to db, then sources, return answer
    """
    query_message = await create_message(db, role=MessageRole.USER, content=query, chat=chat)

    try:
        answer = await run_in_threadpool(answer_svc.answer_question, query)
    except Exception as e:
        raise AnswerGenerationError("Failed to generate answer") from e

    answer_message = await create_message(db, role=MessageRole.ASSISTANT, content=answer["answer"], chat=chat)

    sources = sources_from_answer(answer["sources"])
    for source in sources:
        await create_message_source(db, message=answer_message, source=source)

    return construct_ask_response(
        chat_id=chat.chat_id,
        query_message_id=query_message.message_id,
        answer_message_id=answer_message.message_id,
        answer=answer,
        sources=sources,
    )
