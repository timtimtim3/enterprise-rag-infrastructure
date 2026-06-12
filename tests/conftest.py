# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import TEST_DATABASE_URL
from app.core.redis import get_redis
from app.db.base import Base
from app.db.session import get_db
from app.db.crud.auth import get_user_by_username
from app.db.crud.chats import create_chat
from app.main import app


test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)


class FakeRedis:
    def __init__(self):
        self.store = {}

    async def exists(self, key: str) -> int:
        return int(key in self.store)

    async def setex(self, key: str, ttl: int, value: str) -> None:
        self.store[key] = value

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)


@pytest.fixture(scope="session")
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
async def db_session(setup_test_db):
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()


@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
async def client(db_session, fake_redis):
    async def override_get_db():
        yield db_session

    async def override_get_redis():
        yield fake_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


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
async def session_authenticated_client(client, register_payload):
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
async def jwt_authenticated_client(client, register_payload):
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

    return client


@pytest.fixture
async def authenticated_client(jwt_authenticated_client):
    return jwt_authenticated_client


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
