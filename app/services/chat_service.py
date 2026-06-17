from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

from app.api.schemas.chats import AskResponse
from app.api.schemas.mappers import construct_ask_response, sources_from_answer
from app.core.config import ROUTER_HISTORY_TOKEN_BUDGET, ANSWER_HISTORY_TOKEN_BUDGET
from app.db.crud.chats import create_message, create_message_source, get_chat_messages
from app.db.models.chats import Message
from app.domain.enums.llm_route import RetrievalScope
from app.domain.enums.message_role import MessageRole
from app.domain.chats import MessageCreateData
from app.prompts.helpers import estimate_tokens, format_message_dict

if TYPE_CHECKING:
    from app.db.models.chats import Chat
    from app.services.answer_service import AnswerService
    from app.services.query_router import QueryRouter


class AnswerGenerationError(Exception):
    pass


def budget_recent_history_messages(messages: list[Message], max_tokens: int) -> list[dict]:
    budgeted_messages = []
    used = 0
    for message in reversed(messages):
        message_tokens = message.content_tokens or estimate_tokens(message.content)
        if used + message_tokens > max_tokens:
            break
        used += message_tokens
        message_dict = format_message_dict(content=message.content, role=message.role)
        budgeted_messages.append(message_dict)
    return list(reversed(budgeted_messages))


async def answer_chat_message(
    db: AsyncSession,
    query_router: QueryRouter,
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
        content_tokens=estimate_tokens(query),
    )
    query_message = await create_message(db, chat=chat, message_create=message_create)

    # Get chat history
    chat_history_messages = await get_chat_messages(db, chat=chat)

    # Get Router plan (what to do; rag, no rag, tool, ask clarification, etc.)
    router_history_messages = budget_recent_history_messages(chat_history_messages, ROUTER_HISTORY_TOKEN_BUDGET)
    try:
        route_plan = await query_router.route_query(query, history_messages=router_history_messages)
    except Exception as e:
        raise AnswerGenerationError("Failed to generate answer") from e

    # Execute router plan / answer user query
    answer_history_messages = budget_recent_history_messages(chat_history_messages, ANSWER_HISTORY_TOKEN_BUDGET)
    try:
        answer = await answer_svc.answer(
            query=query,
            retrieval_scope=route_plan.retrieval_scope,
            response_mode=route_plan.response_mode,
            reason=route_plan.reason,
            retrieval_query=route_plan.retrieval_query,
            history_messages=answer_history_messages,
        )
    except Exception as e:
        raise AnswerGenerationError("Failed to generate answer") from e

    message_create = MessageCreateData(
        role=MessageRole.ASSISTANT,
        content=answer["answer"],
        content_tokens=estimate_tokens(answer["answer"]),
        model=answer["model"],
        finish_reason=answer["finish_reason"],
        prompt_tokens=answer["usage"]["prompt_tokens"],
        completion_tokens=answer["usage"]["completion_tokens"],
        total_tokens=answer["usage"]["total_tokens"],
    )

    # If RAG was used, add embedding and reranker model and provider names
    if route_plan.retrieval_scope != RetrievalScope.NONE:
        message_create.retrieval_embedding_model = answer_svc.retriever.embedding_svc.model_name
        message_create.retrieval_embedding_provider = answer_svc.retriever.embedding_svc.provider.value
        message_create.retrieval_reranking_model = answer_svc.retriever.reranker.model_name
        message_create.retrieval_reranking_provider = answer_svc.retriever.reranker.provider.value

    answer_message = await create_message(db, chat=chat, message_create=message_create, route_plan=route_plan)

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
