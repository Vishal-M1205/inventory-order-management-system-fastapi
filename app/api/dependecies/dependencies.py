from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.scopes import SCOPES
from app.core.security import decode_jwt_token
from app.database.database import get_db_session
from app.exceptions.custom_exception import (
    ForbiddenException,
    InvalidTokenException,
    NotFoundException,
)
from app.repositories.implementations.role_repository import RoleRepository
from app.repositories.implementations.user_repository import UserRepository
from app.repositories.implementations.user_role_repository import UserRoleRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

DB_SESSION = Annotated[AsyncSession, Depends(get_db_session)]
o_auth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_user_repository(session: DB_SESSION):
    return UserRepository(session=session)


def get_role_repository(session: DB_SESSION):
    return RoleRepository(session)


def get_user_role_repository(sesssion: DB_SESSION):
    return UserRoleRepository(sesssion)


def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(user_repository=user_repository)


def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
    user_role_repository: Annotated[
        UserRoleRepository, Depends(get_user_role_repository)
    ],
    session: DB_SESSION,
):
    return UserService(
        session=session,
        user_repository=user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository,
    )


async def get_current_user(
    token: Annotated[str, Depends(o_auth2_scheme)],
    security_scopes: SecurityScopes,
    session: DB_SESSION,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    token_data = decode_jwt_token(token)

    if not token_data.get("sub", None):
        raise InvalidTokenException()

    user = await user_repository.get_user_by_email(token_data.get("sub"))
    await session.commit()

    if not user:
        raise NotFoundException("User not found")

    role = token_data.get("role", None)

    if role:
        if user.role.role != role:
            raise InvalidTokenException()

        allowed_scopes = SCOPES[role]

        for scope in security_scopes.scopes:
            if not scope in allowed_scopes:
                raise ForbiddenException()

    return user
