import pytest

from app.db.crud.auth import get_user_by_username
from app.db.crud.chats import create_chat, create_message, create_message_source, get_user_chat
from app.api.schemas.chats import AskResponse, UsageInfo
from app.api.routes import chats as chats_route
from app.domain.chats import MessageCreateData, SourceCreateData
from app.services.chat_service import AnswerGenerationError


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


async def fake_answer_chat_message_gen_fail(**kwargs):
    raise AnswerGenerationError()


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


@pytest.mark.asyncio
async def test_delete_chat_raises_404_on_non_existing_chat(authenticated_client):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client["client"].delete(
        f"/chats/{non_existing_chat_id}", 
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"
    

@pytest.mark.asyncio
async def test_create_chat_returns_answer(authenticated_client, db_session, monkeypatch, app_state):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

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

    chat = await get_user_chat(db_session, user, body["chat_id"])
    assert chat is not None


@pytest.mark.asyncio
async def test_create_chat_raises_500_when_answer_generation_fails(authenticated_client, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message_gen_fail,
    )

    response = await authenticated_client["client"].post(
        "/chats", 
        json={
            "query": "What is Northstar?",
        }
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate answer"


@pytest.mark.asyncio
async def test_add_message_returns_answer(authenticated_client, db_session, monkeypatch, app_state):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="What is Northstar?", user=user)
    assert chat is not None

    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message,
    )

    response = await authenticated_client["client"].post(
        f"/chats/{chat.chat_id}/messages",
        json={
            "query": "Thanks for answering my question!",
        }
    )
    assert response.status_code == 201

    body = response.json()
    assert body["answer"] == "Fake answer"
    assert body["chat_id"] == chat.chat_id


@pytest.mark.asyncio
async def test_add_message_raises_404_on_non_existing_chat(authenticated_client, monkeypatch, app_state):
    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message,
    )

    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client["client"].post(
        f"/chats/{non_existing_chat_id}/messages",
        json={
            "query": "Thanks for answering my question!",
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_add_message_raises_500_when_answer_generation_fails(authenticated_client, db_session, monkeypatch, app_state):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="What is Northstar?", user=user)
    assert chat is not None

    monkeypatch.setattr(
        chats_route,
        "answer_chat_message",
        fake_answer_chat_message_gen_fail,
    )

    response = await authenticated_client["client"].post(
        f"/chats/{chat.chat_id}/messages",
        json={
            "query": "Thanks for answering my question!",
        }
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to generate answer"


@pytest.mark.asyncio
async def test_list_chats_returns_chats(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat1 = await create_chat(db_session, title="Chat1", user=user)
    assert chat1 is not None

    chat2 = await create_chat(db_session, title="Chat2", user=user)
    assert chat2 is not None

    response = await authenticated_client["client"].get("/chats")
    assert response.status_code == 200

    body = response.json()
    returned_chat_ids = [chat["chat_id"] for chat in body["chats"]]
    expected_chat_ids = [chat1.chat_id, chat2.chat_id]
    assert returned_chat_ids == expected_chat_ids


@pytest.mark.asyncio
async def test_list_chats_returns_empty_list_on_no_chats(authenticated_client):
    response = await authenticated_client["client"].get("/chats")
    assert response.status_code == 200

    body = response.json()
    assert body["chats"] == []


@pytest.mark.asyncio
async def test_get_chat_returns_chat(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="Chat1", user=user)
    assert chat is not None

    response = await authenticated_client["client"].get(f"/chats/{chat.chat_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["chat_id"] == chat.chat_id


@pytest.mark.asyncio
async def test_get_chat_raises_404_on_no_such_chat(authenticated_client):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client["client"].get(f"/chats/{non_existing_chat_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_list_messages_returns_messages(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="Chat1", user=user)
    assert chat is not None

    message_create1 = MessageCreateData(
        role="user",
        content="What is Northstar?",    
        content_tokens=3,
    )
    message1 = await create_message(db_session, chat, message_create1)

    message_create2 = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message2 = await create_message(db_session, chat, message_create2)

    response = await authenticated_client["client"].get(f"/chats/{chat.chat_id}/messages")
    assert response.status_code == 200

    body = response.json()
    returned_message_ids = [message["message_id"] for message in body["messages"]]
    expected_message_ids = [message1.message_id, message2.message_id]
    assert returned_message_ids == expected_message_ids


@pytest.mark.asyncio
async def test_list_messages_raises_404_on_no_such_chat(authenticated_client):
    non_existing_chat_id = "some-non-existing-chatid"
    response = await authenticated_client["client"].get(f"/chats/{non_existing_chat_id}/messages")
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_list_message_sources_returns_message_sources(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="Chat", user=user)
    assert chat is not None

    message_create = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message = await create_message(db_session, chat, message_create)

    source_create = SourceCreateData(
        doc_id="some-docid",
        source_index=0,
        title="This is an interesting doc",
        source_path="data/curated/internal/interesting-doc.md",
        source_type="internal",
        doc_type="standard",
        chunk_indices=[1, 2, 3],
    )
    source = await create_message_source(db_session, message, source_create)

    response = await authenticated_client["client"].get(f"/chats/{chat.chat_id}/messages/{message.message_id}/sources")
    assert response.status_code == 200

    body = response.json()
    returned_doc_ids = [message_source["doc_id"] for message_source in body["message_sources"]]
    expected_doc_ids = [source.doc_id]
    assert returned_doc_ids == expected_doc_ids


@pytest.mark.asyncio
async def test_list_message_sources_raises_404_on_no_such_chat(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="Chat", user=user)
    assert chat is not None

    non_existing_chat_id = "some-non-existing-chatid"

    message_create = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message = await create_message(db_session, chat, message_create)

    source_create = SourceCreateData(
        doc_id="some-docid",
        source_index=0,
        title="This is an interesting doc",
        source_path="data/curated/internal/interesting-doc.md",
        source_type="internal",
        doc_type="standard",
        chunk_indices=[1, 2, 3],
    )
    await create_message_source(db_session, message, source_create)

    response = await authenticated_client["client"].get(f"/chats/{non_existing_chat_id}/messages/{message.message_id}/sources")
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_list_message_sources_raises_404_on_no_such_message(authenticated_client, db_session):
    user = await get_user_by_username(db_session, authenticated_client["user"]["username"])
    assert user is not None

    chat = await create_chat(db_session, title="Chat", user=user)
    assert chat is not None

    message_create = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message = await create_message(db_session, chat, message_create)
    non_existing_message_id = "some-non-existing-messageid"

    source_create = SourceCreateData(
        doc_id="some-docid",
        source_index=0,
        title="This is an interesting doc",
        source_path="data/curated/internal/interesting-doc.md",
        source_type="internal",
        doc_type="standard",
        chunk_indices=[1, 2, 3],
    )
    await create_message_source(db_session, message, source_create)

    response = await authenticated_client["client"].get(f"/chats/{chat.chat_id}/messages/{non_existing_message_id}/sources")
    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"
