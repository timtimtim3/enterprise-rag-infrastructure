import pytest

from app.db.crud.auth import get_user_by_username
from app.db.crud.chats import create_chat, get_user_chat


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
