import pytest


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

    return {
        "client": client,
        "user": register_payload,
    }
