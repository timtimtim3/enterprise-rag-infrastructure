import pytest

from app.db.crud.auth import get_user_by_username
from app.db.crud.chats import create_chat, get_user_chat
from app.api.schemas.chats import AskResponse, UsageInfo
from app.api.routes import chats as chats_route
from app.services.chat_service import AnswerGenerationError


@pytest.mark.asyncio
async def test_delete_chat(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, "Some chat title", user)
    assert chat is not None

    chat_id = chat.chat_id

    response = await authenticated_client["client"].delete(
        f"/chats/{chat.chat_id}", 
    )
    assert response.status_code == 204

    chat = await get_user_chat(db_session, user, chat_id)
    assert chat is None


async def fake_answer_chat_message(**kwargs):
    return AskResponse(
        chat_id=kwargs["chat"].chat_id,
        query_message_id="query-msg-1",
        answer_message_id="answer-msg-1",
        answer="Fake answer",
        model="fake-model",
        finish_reason="stop",
        usage=UsageInfo(
            completion_tokens=10,
            prompt_tokens=20,
            total_tokens=30,
        ),
        sources=[],
    )


@pytest.mark.asyncio
async def test_create_chat_returns_answer(authenticated_client, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message,
    )

    response = await authenticated_client["client"].post(
        "/chats",
        json={
            "query": "What is Northstar?",
        }
    )
    assert response.status_code == 201

    body = response.json()
    assert body["answer"] == "Fake answer"
    assert body["model"] == "fake-model"
    assert body["sources"] == []


@pytest.mark.asyncio
async def test_create_chat_returns_500_when_answer_generation_fails(authenticated_client, monkeypatch, app_state):
    async def fake_answer_chat_message(**kwargs):
        raise AnswerGenerationError()

    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message,
    )

    response = await authenticated_client["client"].post(
        "/chats", 
        json={
            "query": "What is Northstar?",
        }
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate answer"
