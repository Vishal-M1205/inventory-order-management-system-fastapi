from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

import jwt
from pwdlib import PasswordHash

from app.core.config import config

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_hashed_password(hashed_password: str, password: str) -> bool:
    return password_hasher.verify(password, hashed_password)


def get_token_expiry(token_type: Literal["access", "refresh"]) -> datetime:
    minutes = (
        config.jwt_access_token_expiration_minute
        if token_type == "access"
        else config.jwt_refresh_token_expiration_minute
    )
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


def create_jwt_token(
    subject: str,
    token_type: Literal["access", "refresh"] = "access",
    jti: Optional[str] = None,
    expires_at: Optional[datetime] = None,
) -> str:
    """Create a JWT containing identity (sub), token type, expiration, and optional jti."""
    expire_at = expires_at or get_token_expiry(token_type)

    payload = {
        "sub": subject,
        "type": token_type,
        "exp": expire_at,
    }
    if jti is not None:
        payload["jti"] = jti

    return jwt.encode(
        payload, key=config.jwt_secret_key, algorithm=config.jwt_hashing_algorithm
    )


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(
        jwt=token,
        key=config.jwt_secret_key,
        algorithms=[config.jwt_hashing_algorithm],
    )
