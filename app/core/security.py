import jwt
from pwdlib import PasswordHash
from app.core.config import config
from datetime import datetime, timedelta, timezone

from app.core.scopes import SCOPES

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_hashed_password(hashed_password: str, password: str) -> bool:
    return password_hasher.verify(password, hashed_password)


def create_jwt_token(token_data: dict, type: str = "access") -> str:
    encoded_data = token_data.copy()

    if type == "access":
        expire_minutes = datetime.now(timezone.utc) + timedelta(
            minutes=config.jwt_access_token_expiration_minute
        )

    elif type == "refresh":
        expire_minutes = datetime.now(timezone.utc) + timedelta(
            minutes=config.jwt_refresh_token_expiration_minute
        )

    encoded_data["exp"] = expire_minutes
    role = encoded_data.get("role", None)

    if role and type == "access":
        encoded_data["scopes"] = SCOPES[role]

    encoded_data["type"] = "access"

    return jwt.encode(
        encoded_data, key=config.jwt_secret_key, algorithm=config.jwt_hashing_algorithm
    )


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(
        jwt=token, key=config.jwt_secret_key, algorithms=[config.jwt_hashing_algorithm]
    )
