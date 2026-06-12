import pytest

from app.core.security import hash_refresh_token, verify_access_token
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.db.crud.auth import get_refresh_token_by_hash, get_user_by_email


@pytest.mark.asyncio
async def test_signin_jwt_creates_refresh_token_and_returns_access_token(client, db_session, register_payload):
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
        '/auth/signin-jwt',
        json=signin_payload,
    )
    assert response.status_code == 200

    body = response.json()
    access_token =  body.get("access_token")
    token_type = body.get("token_type")
    assert access_token is not None
    assert token_type == "bearer"

    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None

    refresh_token_hash = hash_refresh_token(refresh_token)
    refresh_token_db = await get_refresh_token_by_hash(db_session, refresh_token_hash)

    assert refresh_token_db is not None
    assert refresh_token_db.user_fk == user.id
    assert refresh_token_db.token_hash == refresh_token_hash
    assert refresh_token_db.token_hash != refresh_token
    assert refresh_token_db.revoked_at is None


@pytest.mark.asyncio
async def test_signin_jwt_returns_401_on_non_existing_user(client, register_payload):
    signin_payload = {
        "username": register_payload["username"],
        "password": register_payload["password"],
    }
    response = await client.post(
        '/auth/signin-jwt',
        json=signin_payload,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_signin_jwt_returns_401_on_incorrect_password(client, register_payload):
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
        '/auth/signin-jwt',
        json=signin_payload,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_jwt_returns_current_user(jwt_authenticated_client, register_payload):
    response = await jwt_authenticated_client.get("/auth/me-jwt")
    assert response.status_code == 200

    body = response.json()
    assert body["username"] == register_payload["username"]


@pytest.mark.asyncio
async def test_me_jwt_requires_authentication(client):
    response = await client.get("/auth/me-jwt")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_returns_new_access_token(jwt_authenticated_client):
    response = await jwt_authenticated_client.post(
        '/auth/refresh-jwt',
    )
    assert response.status_code == 200

    body = response.json()

    new_access_token = body.get("access_token")
    token_type = body.get("token_type")
    assert new_access_token is not None
    assert token_type == "bearer"

    jwt_authenticated_client.headers["Authorization"] = (
        f"Bearer {new_access_token}"
    )

    response = await jwt_authenticated_client.get("/auth/me-jwt")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_refresh_requires_refresh_token(client):
    response = await client.post("/auth/refresh-jwt")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_signout_revokes_refresh_token_and_refresh_returns_401(jwt_authenticated_client, db_session):
    refresh_token = jwt_authenticated_client.cookies.get("refresh_token")
    assert refresh_token is not None
    refresh_token_hash = hash_refresh_token(refresh_token)

    response = await jwt_authenticated_client.post('/auth/signout-jwt')
    assert response.status_code == 204

    assert jwt_authenticated_client.cookies.get("refresh_token") is None

    refresh_token_db = await get_refresh_token_by_hash(db_session, refresh_token_hash)
    assert refresh_token_db is not None
    assert refresh_token_db.revoked_at is not None

    response = await jwt_authenticated_client.post('/auth/refresh-jwt')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_signout_revokes_access_token_and_me_returns_401(client, register_payload, fake_redis):
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
        '/auth/signin-jwt',
        json=signin_payload,
    )
    assert signin_response.status_code == 200

    access_token = signin_response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {access_token}",
    })

    response = await client.post('/auth/signout-jwt')
    assert response.status_code == 204

    payload = verify_access_token(access_token, secret_key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    jti = payload["jti"]
    assert await fake_redis.exists(key=f"revoked_access_token:{jti}")

    response = await client.get("/auth/me-jwt")
    assert response.status_code == 401
