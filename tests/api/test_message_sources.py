import pytest

from app.db.crud.chats import create_message, create_message_source
from app.domain.chats import MessageCreateData, SourceCreateData


@pytest.mark.asyncio
async def test_list_message_sources_returns_message_sources(authenticated_client, test_chat, db_session):
    message_create = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message = await create_message(db_session, test_chat, message_create)

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

    response = await authenticated_client.get(f"/chats/{test_chat.chat_id}/messages/{message.message_id}/sources")
    assert response.status_code == 200

    body = response.json()
    returned_doc_ids = [message_source["doc_id"] for message_source in body["message_sources"]]
    expected_doc_ids = [source.doc_id]
    assert returned_doc_ids == expected_doc_ids


@pytest.mark.asyncio
async def test_list_message_sources_returns_404_on_no_such_chat(authenticated_client, test_chat, db_session):
    non_existing_chat_id = "some-non-existing-chatid"
    message_create = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message = await create_message(db_session, test_chat, message_create)

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

    response = await authenticated_client.get(f"/chats/{non_existing_chat_id}/messages/{message.message_id}/sources")
    assert response.status_code == 404
    assert response.json()["detail"] == "Chat not found"


@pytest.mark.asyncio
async def test_list_message_sources_returns_404_on_no_such_message(authenticated_client, test_chat, db_session):
    message_create = MessageCreateData(
        role="system",
        content="Northstar is a company.",  
        content_tokens=4,
    )
    message = await create_message(db_session, test_chat, message_create)
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

    response = await authenticated_client.get(f"/chats/{test_chat.chat_id}/messages/{non_existing_message_id}/sources")
    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"
