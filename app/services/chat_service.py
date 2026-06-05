from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.concurrency import run_in_threadpool
from typing import TYPE_CHECKING

from app.api.schemas.chats import AskResponse
from app.api.schemas.mappers import construct_ask_response, sources_from_answer
from app.db.crud.chats import create_message, create_message_source
from app.domain.enums.message_role import MessageRole
from app.domain.chats import MessageCreateData

if TYPE_CHECKING:
    from app.db.models.chats import Chat
    from app.services.answer_service import AnswerService


class AnswerGenerationError(Exception):
    pass


async def answer_chat_message(
    db: AsyncSession,
    answer_svc: AnswerService,
    chat: Chat,
    query: str,
) -> AskResponse:
    """
    Add query to db, sends query to RAG llm, add response to db, then sources, return answer
    """
    message_create = MessageCreateData(
        role=MessageRole.USER,
        content=query,
    )
    query_message = await create_message(db, chat=chat, message_create=message_create)

    try:
        answer = await answer_svc.answer_question(query)
    except Exception as e:
        raise AnswerGenerationError("Failed to generate answer") from e

    message_create = MessageCreateData(
        role=MessageRole.ASSISTANT,
        content=answer["answer"],
        model=answer["model"],
        route=answer["route"],
        finish_reason=answer["finish_reason"],
        prompt_tokens=answer["usage"]["prompt_tokens"],
        completion_tokens=answer["usage"]["completion_tokens"],
        total_tokens=answer["usage"]["total_tokens"],
    )

    # RAG-based, for now we always do RAG
    if True:
        # Rag-only fields
        message_create.retrieval_embedding_model = answer_svc.retriever.embedding_svc.model_name
        message_create.retrieval_reranking_model = answer_svc.retriever.reranker.model_name

    answer_message = await create_message(db, chat=chat, message_create=message_create)

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
