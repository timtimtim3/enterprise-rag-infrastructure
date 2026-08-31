import pytest

from app.db.crud.chats import create_message
from app.api.routes import chats as chats_route
from app.domain.chats import MessageCreateData
from tests.api.helpers import fake_answer_chat_message, fake_answer_chat_message_gen_fail


@pytest.mark.asyncio
async def test_add_message_returns_answer(authenticated_client, test_chat, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message_with_agent",
        fake_answer_chat_message,
    )

    response = await authenticated_client.post(
        f"/chats/{test_chat.chat_id}/messages",
        json={
            "query": "Thanks for answering my question!",
        }
    )
    assert response.status_code == 201

    body = response.json()
    assert body["answer"] == "Fake answer"
    assert body["chat_id"] == test_chat.chat_id


@pytest.mark.asyncio
async def test_add_message_returns_404_on_non_existing_chat(authenticated_client, monkeypatch, app_state):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client.post(
        f"/chats/{non_existing_chat_id}/messages",
        json={
            "query": "Thanks for answering my question!",
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_add_message_returns_500_when_answer_generation_fails(authenticated_client, test_chat, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message_with_agent",
        fake_answer_chat_message_gen_fail,
    )

    response = await authenticated_client.post(
        f"/chats/{test_chat.chat_id}/messages",
        json={
            "query": "Thanks for answering my question!",
        }
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate answer"


@pytest.mark.asyncio
async def test_list_messages_returns_messages(authenticated_client, test_chat, db_session):
    message_create1 = MessageCreateData(
        role="user",
        content="What is Northstar?",    
        content_tokens=3,
    )
    message1 = await create_message(db_session, test_chat, message_create1)

    message_create2 = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message2 = await create_message(db_session, test_chat, message_create2)

    response = await authenticated_client.get(f"/chats/{test_chat.chat_id}/messages")
    assert response.status_code == 200

    body = response.json()
    returned_message_ids = [message["message_id"] for message in body["messages"]]
    expected_message_ids = [message1.message_id, message2.message_id]
    assert returned_message_ids == expected_message_ids


@pytest.mark.asyncio
async def test_list_messages_returns_404_on_no_such_chat(authenticated_client):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client.get(f"/chats/{non_existing_chat_id}/messages")
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"
