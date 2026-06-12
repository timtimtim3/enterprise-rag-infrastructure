import uuid

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import hashlib
import secrets


password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def gen_refresh_token():
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(
    *,
    user_id: str,
    username: str,
    secret_key: str,
    algorithm: str,
    expires_in_seconds: int,
) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=expires_in_seconds)

    payload = {
        "sub": user_id,
        "username": username,
        "exp": expires_at,
        "iat": now,
        "jti": str(uuid.uuid4()),
        "type": "access",
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def verify_access_token(
    access_token: str,
    *,
    secret_key: str,
    algorithm: str,
) -> dict:
    try:
        payload = jwt.decode(
            access_token,
            secret_key,
            algorithms=[algorithm],
        )
    except JWTError as exc:
        raise ValueError("Invalid access token") from exc

    sub = payload.get("sub")
    exp = payload.get("exp")
    iat = payload.get("iat")
    jti = payload.get("jti")

    if not isinstance(sub, str) or not sub:
        raise ValueError("Token subject is missing or invalid")

    if not isinstance(jti, str) or not jti:
        raise ValueError("Token JTI is missing or invalid")

    if not isinstance(exp, int):
        raise ValueError("Token expiration is missing or invalid")

    if not isinstance(iat, int):
        raise ValueError("Token issued-at is missing or invalid")

    if iat > exp:
        raise ValueError("Token issued-at is after expiration")

    return payload
