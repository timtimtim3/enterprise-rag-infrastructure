from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING
from langchain_core.messages import AIMessage, HumanMessage

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


def budget_recent_history_messages(
    messages: list[Message],
    max_tokens: int,
) -> list[dict]:
    messages = budget_recent_messages(
        messages,
        max_tokens,
    )

    return [
        format_message_dict(
            content=message.content,
            role=message.role,
        )
        for message in messages
    ]


def budget_recent_messages(
    messages: list[Message],
    max_tokens: int,
) -> list[Message]:
    budgeted_messages = []
    used = 0

    for message in reversed(messages):
        message_tokens = (
            message.content_tokens
            or estimate_tokens(message.content)
        )

        if used + message_tokens > max_tokens:
            break

        used += message_tokens
        budgeted_messages.append(message)

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


def db_history_to_langchain(
    messages: list[Message],
    max_tokens: int,
):
    messages = budget_recent_messages(
        messages,
        max_tokens,
    )

    result = []

    for message in messages:
        if message.role == MessageRole.USER:
            result.append(
                HumanMessage(content=message.content)
            )

        elif message.role == MessageRole.ASSISTANT:
            result.append(
                AIMessage(content=message.content)
            )

    return result


async def answer_chat_message_with_agent(
    db: AsyncSession,
    graph,
    retriever,
    chat,
    query: str,
    user_id: str,
) -> AskResponse:

    # ---------------------------------------------------------
    # 1. Persist user message
    # ---------------------------------------------------------

    query_message = await create_message(
        db,
        chat=chat,
        message_create=MessageCreateData(
            role=MessageRole.USER,
            content=query,
            content_tokens=estimate_tokens(query),
        ),
    )

    # ---------------------------------------------------------
    # 2. Load previous conversation history
    # ---------------------------------------------------------

    chat_messages = await get_chat_messages(
        db,
        chat=chat,
    )

    # We just persisted the current query.
    # Don't include it in history AND append it again below.
    previous_messages = [
        message
        for message in chat_messages
        if message.message_id != query_message.message_id
    ]

    history = db_history_to_langchain(
        messages=previous_messages,
        max_tokens=ANSWER_HISTORY_TOKEN_BUDGET,
    )

    # ---------------------------------------------------------
    # 3. Run LangGraph agent
    # ---------------------------------------------------------

    try:
        result = await graph.ainvoke(
            {
                "messages": [
                    *history,
                    HumanMessage(content=query),
                ],
                "tool_iterations": 0,
                "tool_history": [],
                "source_registry": {},
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "user_id": user_id,
            }
        )

    except Exception as e:
        raise AnswerGenerationError(
            "Failed to generate agent answer"
        ) from e

    final_message = result["messages"][-1]
    answer_text = final_message.content

    # ---------------------------------------------------------
    # 4. Collect sources accumulated across ALL RAG calls
    # ---------------------------------------------------------

    source_registry = result.get(
        "source_registry",
        {},
    )

    answer_sources = sorted(
        source_registry.values(),
        key=lambda source: source["source_index"],
    )

    # ---------------------------------------------------------
    # 5. Create response object, same general shape as before
    # ---------------------------------------------------------

    answer = {
        "answer": answer_text,
        "model": result.get("model"),
        "finish_reason": result.get("finish_reason"),
        "usage": {
            "prompt_tokens": result.get(
                "prompt_tokens",
                0,
            ),
            "completion_tokens": result.get(
                "completion_tokens",
                0,
            ),
            "total_tokens": result.get(
                "total_tokens",
                0,
            ),
        },
        "sources": answer_sources,
    }

    # ---------------------------------------------------------
    # 6. Determine whether RAG was actually used
    # ---------------------------------------------------------

    rag_used = any(
        entry["tool"] == "search_company_knowledge"
        for entry in result.get("tool_history", [])
    )

    # ---------------------------------------------------------
    # 7. Persist assistant message
    # ---------------------------------------------------------

    message_create = MessageCreateData(
        role=MessageRole.ASSISTANT,
        content=answer_text,
        content_tokens=estimate_tokens(answer_text),

        model=answer["model"],
        finish_reason=answer["finish_reason"],

        prompt_tokens=answer["usage"]["prompt_tokens"],
        completion_tokens=answer["usage"]["completion_tokens"],
        total_tokens=answer["usage"]["total_tokens"],
    )

    if rag_used:
        message_create.retrieval_embedding_model = (
            retriever.embedding_svc.model_name
        )
        message_create.retrieval_embedding_provider = (
            retriever.embedding_svc.provider.value
        )
        message_create.retrieval_reranking_model = (
            retriever.reranker.model_name
        )
        message_create.retrieval_reranking_provider = (
            retriever.reranker.provider.value
        )

    answer_message = await create_message(
        db,
        chat=chat,
        message_create=message_create,
    )

    # ---------------------------------------------------------
    # 8. Persist retrieved sources
    # ---------------------------------------------------------

    sources = sources_from_answer(
        answer["sources"]
    )

    for source in sources:
        await create_message_source(
            db,
            message=answer_message,
            source=source,
        )

    # ---------------------------------------------------------
    # 9. API response
    # ---------------------------------------------------------

    return construct_ask_response(
        chat_id=chat.chat_id,
        query_message_id=query_message.message_id,
        answer_message_id=answer_message.message_id,
        answer=answer,
        sources=sources,
    )
