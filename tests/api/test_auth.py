import pytest

from app.db.crud.auth import get_user_by_email


@pytest.mark.asyncio
async def test_signup_creates_user(client, db_session):
    email = "test@example.com"
    username = "testuser"
    register_payload = {
        "username": username,
        "email": email,
        "password": "password",
    }
    response = await client.post(
        '/auth/signup',
        json=register_payload,
    )
    assert response.status_code == 201

    user = await get_user_by_email(db_session, email)

    assert user is not None
    assert user.email == email
    assert user.username == username


@pytest.mark.asyncio
async def test_signup_fails_on_existing_email(client, db_session):
    register_payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password",
    }
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
async def test_signup_fails_on_existing_username(client, db_session):
    register_payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password",
    }
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
