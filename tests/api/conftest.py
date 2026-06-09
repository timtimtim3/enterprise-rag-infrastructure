import pytest

from app.db.crud.auth import get_user_by_username
from app.db.crud.chats import create_chat
from app.main import app


@pytest.fixture
def app_state(monkeypatch):
    monkeypatch.setattr(app.state, "query_router", object(), raising=False)
    monkeypatch.setattr(app.state, "answer_svc", object(), raising=False)


@pytest.fixture
def register_payload():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password",
    }


@pytest.fixture
async def authenticated_client(client, register_payload):
    signup_response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert signup_response.status_code == 201

    signin_payload = {
        "username": register_payload["username"],
        "password": register_payload["password"],
    }
    signin_response = await client.post(
        '/auth/signin',
        json=signin_payload,
    )
    assert signin_response.status_code == 200

    return client


@pytest.fixture
async def authenticated_user(authenticated_client, register_payload, db_session):
    user = await get_user_by_username(db_session, register_payload["username"])
    assert user is not None
    return user


@pytest.fixture
async def test_chat(db_session, authenticated_user):
    chat = await create_chat(db_session, title="Chat", user=authenticated_user)
    assert chat is not None
    return chat
