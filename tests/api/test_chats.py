import pytest

from app.db.crud.chats import create_chat, get_user_chat
from app.api.routes import chats as chats_route
from tests.api.helpers import fake_answer_chat_message, fake_answer_chat_message_gen_fail


@pytest.mark.asyncio
async def test_delete_chat(authenticated_client, authenticated_user, test_chat, db_session):
    response = await authenticated_client.delete(
        f"/chats/{test_chat.chat_id}", 
    )
    assert response.status_code == 204

    chat = await get_user_chat(db_session, authenticated_user, test_chat.chat_id)
    assert chat is None


@pytest.mark.asyncio
async def test_delete_chat_returns_404_on_non_existing_chat(authenticated_client):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client.delete(
        f"/chats/{non_existing_chat_id}", 
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_create_chat_returns_answer(authenticated_client, authenticated_user, db_session, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message,
    )

    response = await authenticated_client.post(
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

    chat = await get_user_chat(db_session, authenticated_user, body["chat_id"])
    assert chat is not None


@pytest.mark.asyncio
async def test_create_chat_returns_500_when_answer_generation_fails(authenticated_client, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message_gen_fail,
    )

    response = await authenticated_client.post(
        "/chats", 
        json={
            "query": "What is Northstar?",
        }
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate answer"


@pytest.mark.asyncio
async def test_list_chats_returns_chats(authenticated_client, authenticated_user, db_session):
    chat1 = await create_chat(db_session, title="Chat1", user=authenticated_user)
    assert chat1 is not None

    chat2 = await create_chat(db_session, title="Chat2", user=authenticated_user)
    assert chat2 is not None

    response = await authenticated_client.get("/chats")
    assert response.status_code == 200

    body = response.json()
    returned_chat_ids = [chat["chat_id"] for chat in body["chats"]]
    expected_chat_ids = [chat1.chat_id, chat2.chat_id]
    assert returned_chat_ids == expected_chat_ids


@pytest.mark.asyncio
async def test_list_chats_returns_empty_list_on_no_chats(authenticated_client):
    response = await authenticated_client.get("/chats")
    assert response.status_code == 200

    body = response.json()
    assert body["chats"] == []


@pytest.mark.asyncio
async def test_get_chat_returns_chat(authenticated_client, test_chat):
    response = await authenticated_client.get(f"/chats/{test_chat.chat_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["chat_id"] == test_chat.chat_id


@pytest.mark.asyncio
async def test_get_chat_returns_404_on_no_such_chat(authenticated_client):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client.get(f"/chats/{non_existing_chat_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"
