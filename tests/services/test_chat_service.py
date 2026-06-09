import pytest
from unittest.mock import AsyncMock

from app.db.crud.chats import get_chat_messages
from app.domain.enums.message_role import MessageRole
from app.domain.routing import RoutePlan, SearchHints
from app.services.chat_service import answer_chat_message, budget_recent_history_messages, AnswerGenerationError
from app.domain.enums.llm_route import IntentRoute, RetrievalScope, ToolAction, ResponseMode


@pytest.mark.asyncio
async def test_answer_chat_message(db_session, test_chat):
    query = "What is Northstar?"
    answer = "Northstar is a company"

    mock_query_router = AsyncMock()
    route_plan = RoutePlan(
        intent=IntentRoute.ANSWER,
        retrieval_scope=RetrievalScope.NONE,
        tool_action=ToolAction.NONE,
        response_mode=ResponseMode.DIRECT_ANSWER,
        retrieval_query=query,
        confidence=1.0,
        reason="The user wants to know what Northstar is, which is a question I can answer directly",
        search_hints=SearchHints(
            internal=False,
            public=False,
            vendors=[],
            keywords=[]
        )
    )
    mock_query_router.route_query.return_value = route_plan

    mock_answer_svc = AsyncMock()
    mock_answer_svc.answer.return_value = {
        "answer": answer,
        "model": "llm-model",
        "finish_reason": "done",
        "usage": {
            "completion_tokens": 5,
            "prompt_tokens": 3,
            "total_tokens": 8,
        },
        "sources": [],
    }

    response = await answer_chat_message(
        db=db_session,
        query_router=mock_query_router,
        answer_svc=mock_answer_svc,
        chat=test_chat,
        query=query,
    )

    assert response.answer == answer
    assert response.chat_id == test_chat.chat_id

    # Assert calling behavior and args/kwargs
    mock_query_router.route_query.assert_awaited_once()
    router_call = mock_query_router.route_query.await_args
    assert router_call.args[0] == query
    assert "history_messages" in router_call.kwargs

    mock_answer_svc.answer.assert_awaited_once()
    answer_call = mock_answer_svc.answer.await_args
    answer_kwargs = answer_call.kwargs
    assert answer_kwargs["query"] == query
    assert answer_kwargs["retrieval_scope"] == route_plan.retrieval_scope
    assert answer_kwargs["response_mode"] == route_plan.response_mode
    assert answer_kwargs["reason"] == route_plan.reason
    assert answer_kwargs["retrieval_query"] == route_plan.retrieval_query
    assert "history_messages" in answer_kwargs

    # Assert message creation
    messages = await get_chat_messages(db_session, test_chat)
    assert len(messages) == 2

    user_message = messages[0]
    assistant_message = messages[1]

    # Assert db message fields
    assert user_message.role == MessageRole.USER
    assert user_message.content == query

    assert assistant_message.role == MessageRole.ASSISTANT
    assert assistant_message.content == "Northstar is a company"
    assert assistant_message.model == "llm-model"
    assert assistant_message.finish_reason == "done"
    assert assistant_message.prompt_tokens == 3
    assert assistant_message.completion_tokens == 5
    assert assistant_message.total_tokens == 8

    # Assert return obj fields
    assert response.query_message_id == user_message.message_id
    assert response.answer_message_id == assistant_message.message_id
    assert response.model == "llm-model"
    assert response.finish_reason == "done"

    assert response.usage.prompt_tokens == 3
    assert response.usage.completion_tokens == 5
    assert response.usage.total_tokens == 8

    assert response.sources == []
