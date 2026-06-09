import pytest

from app.db.crud.auth import get_session_by_id, get_user_by_email


@pytest.mark.asyncio
async def test_signup_creates_user(client, db_session, register_payload):
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert response.status_code == 201

    user = await get_user_by_email(db_session, register_payload["email"])

    assert user is not None
    assert user.email == register_payload["email"]
    assert user.username == register_payload["username"]


@pytest.mark.asyncio
async def test_signup_fails_on_existing_email(client, register_payload):
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert response.status_code == 201

    register_payload["username"] = "testuser2"
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_signup_fails_on_existing_username(client, register_payload):
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert response.status_code == 201

    register_payload["email"] = "test2@example.com"
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"username": "", "email": "test@test.com", "password": "pass"},
        {"username": "user", "email": "", "password": "pass"},
        {"username": "user", "email": "invalid", "password": "pass"},
    ],
)
async def test_signup_rejects_invalid_input(client, payload):
    response = await client.post(
        "/auth/signup",
        json=payload,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_signin_creates_session(client, db_session, register_payload):
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert response.status_code == 201

    email = register_payload["email"]
    user = await get_user_by_email(db_session, email)
    assert user is not None

    signin_payload = {
        "username": register_payload["username"],
        "password": register_payload["password"],
    }
    response = await client.post(
        '/auth/signin',
        json=signin_payload,
    )
    assert response.status_code == 200

    session_cookie = response.cookies.get("session_id")
    assert session_cookie is not None

    session = await get_session_by_id(db_session, session_cookie)
    assert session is not None
    assert session.user_fk == user.id


@pytest.mark.asyncio
async def test_signin_fails_on_non_existing_user(client, register_payload):
    signin_payload = {
        "username": register_payload["username"],
        "password": register_payload["password"],
    }
    response = await client.post(
        '/auth/signin',
        json=signin_payload,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_signin_fails_on_incorrect_password(client, register_payload):
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert response.status_code == 201

    signin_payload = {
        "username": register_payload["username"],
        "password": register_payload["password"] + "passwordmutation",
    }
    response = await client.post(
        '/auth/signin',
        json=signin_payload,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_returns_current_user(authenticated_client):
    response = await authenticated_client["client"].get("/auth/me")
    assert response.status_code == 200

    body = response.json()
    assert body["username"] == authenticated_client["user"]["username"]


@pytest.mark.asyncio
async def test_get_me_requires_authentication(client):
    response = await client.get("/auth/me")

    assert response.status_code == 401
