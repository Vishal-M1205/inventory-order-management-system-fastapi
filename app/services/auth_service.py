from datetime import datetime, timezone
from uuid import UUID, uuid4

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_jwt_token,
    decode_jwt_token,
    get_token_expiry,
    verify_hashed_password,
)
from app.exceptions.custom_exception import (
    InactiveUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    TokenExpiredException,
)
from app.repositories.implementations.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.auth import Token


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.session = session
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    def _decode_refresh_token(self, refresh_token: str) -> tuple[UUID, UUID]:
        try:
            payload = decode_jwt_token(refresh_token)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException("Refresh token has expired.")
        except jwt.PyJWTError:
            raise InvalidTokenException("Invalid refresh token.")

        if payload.get("type") != "refresh":
            raise InvalidTokenException("Invalid token type.")

        sub = payload.get("sub")
        jti_str = payload.get("jti")
        if not sub or not jti_str:
            raise InvalidTokenException("Malformed refresh token.")

        try:
            return UUID(sub), UUID(jti_str)
        except ValueError:
            raise InvalidTokenException("Malformed refresh token.")

    async def login(self, username: str, password: str) -> Token:
        async with self.session.begin():
            user = await self.user_repository.get_user_by_email(username)
            if not user or not verify_hashed_password(user.hashed_password, password):
                raise InvalidCredentialsException()

            if not user.is_active:
                raise InactiveUserException()

            jti = uuid4()
            family_id = uuid4()
            expires_at = get_token_expiry("refresh")

            await self.refresh_token_repository.create(
                {
                    "user_id": user.id,
                    "jti": jti,
                    "family_id": family_id,
                    "expires_at": expires_at,
                }
            )

            subject = str(user.id)
            return Token(
                access_token=create_jwt_token(subject, "access"),
                refresh_token=create_jwt_token(
                    subject, "refresh", jti=str(jti), expires_at=expires_at
                ),
            )

    async def refresh(self, refresh_token: str) -> Token:
        user_id, jti = self._decode_refresh_token(refresh_token)
        now = datetime.now(timezone.utc)
        reuse_detected = False

        async with self.session.begin():
            token_row = await self.refresh_token_repository.get_by_jti_for_update(jti)
            if not token_row or token_row.user_id != user_id:
                raise InvalidTokenException("Refresh token not recognized.")

            if token_row.is_revoked:
                # Token reuse detected: revoke the entire family and persist it
                await self.refresh_token_repository.revoke_family(
                    token_row.family_id, now
                )
                reuse_detected = True
            else:
                if token_row.expires_at <= now:
                    raise TokenExpiredException("Refresh token has expired.")

                user = await self.user_repository.get_user_by_id(user_id)
                if not user:
                    raise InvalidTokenException("User not found.")
                if not user.is_active:
                    raise InactiveUserException()

                new_jti = uuid4()
                expires_at = get_token_expiry("refresh")

                token_row.is_revoked = True
                token_row.revoked_at = now
                token_row.replaced_by_jti = new_jti

                await self.refresh_token_repository.create(
                    {
                        "user_id": user.id,
                        "jti": new_jti,
                        "family_id": token_row.family_id,
                        "expires_at": expires_at,
                    }
                )

                subject = str(user.id)
                tokens = Token(
                    access_token=create_jwt_token(subject, "access"),
                    refresh_token=create_jwt_token(
                        subject, "refresh", jti=str(new_jti), expires_at=expires_at
                    ),
                )

        if reuse_detected:
            raise InvalidTokenException(
                "Refresh token reuse detected. Session has been revoked."
            )

        return tokens

    async def logout(self, refresh_token: str) -> None:
        user_id, jti = self._decode_refresh_token(refresh_token)
        now = datetime.now(timezone.utc)

        async with self.session.begin():
            token_row = await self.refresh_token_repository.get_by_jti_for_update(jti)
            if token_row and token_row.user_id == user_id:
                await self.refresh_token_repository.revoke_family(
                    token_row.family_id, now
                )
