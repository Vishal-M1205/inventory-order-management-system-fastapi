from app.core.security import create_jwt_token, verify_hashed_password
from app.exceptions.custom_exception import (
    InvalidCredentialsException,
    NotFoundException,
)
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.auth import Token


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def login(self, username: str, password: str) -> Token:
        user = await self.user_repository.get_user_by_email(username)
        if not user:
            raise NotFoundException(detail="User not found")

        if not verify_hashed_password(user.hashed_password, password):
            raise InvalidCredentialsException()
        token_data = {"sub": user.email, "role": user.role.role}
        token = create_jwt_token(token_data)

        return Token(access_token=token)
