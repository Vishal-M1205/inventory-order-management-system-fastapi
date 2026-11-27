from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.scopes import SCOPES
from app.core.security import decode_jwt_token
from app.database.database import get_db_session
from app.exceptions.custom_exception import (
    ForbiddenException,
    InactiveUserException,
    InvalidTokenException,
    TokenExpiredException,
)
from app.models.users import User
from app.repositories.implementations.category_repository import CategoryRepository
from app.repositories.implementations.product_repository import ProductRepository
from app.repositories.implementations.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.implementations.role_repository import RoleRepository
from app.repositories.implementations.user_profile_repository import (
    UserProfileRepository,
)
from app.repositories.implementations.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.category_service import CategoryService
from app.services.product_service import ProductService
from app.services.user_profile_service import UserProfileService
from app.services.user_service import UserService

DB_SESSION = Annotated[AsyncSession, Depends(get_db_session)]
o_auth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_user_repository(session: DB_SESSION) -> UserRepository:
    return UserRepository(session=session)


def get_role_repository(session: DB_SESSION) -> RoleRepository:
    return RoleRepository(session=session)


def get_user_profile_repository(session: DB_SESSION) -> UserProfileRepository:
    return UserProfileRepository(session=session)


def get_refresh_token_repository(session: DB_SESSION) -> RefreshTokenRepository:
    return RefreshTokenRepository(session=session)


def get_category_repository(session: DB_SESSION) -> CategoryRepository:
    return CategoryRepository(session=session)


def get_product_repository(session: DB_SESSION) -> ProductRepository:
    return ProductRepository(session=session)


def get_auth_service(
    session: DB_SESSION,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    refresh_token_repository: Annotated[
        RefreshTokenRepository, Depends(get_refresh_token_repository)
    ],
) -> AuthService:
    return AuthService(
        session=session,
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


def get_user_service(
    session: DB_SESSION,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
) -> UserService:
    return UserService(
        session=session,
        user_repository=user_repository,
        role_repository=role_repository,
    )


def get_user_profile_service(
    session: DB_SESSION,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    profile_repository: Annotated[
        UserProfileRepository, Depends(get_user_profile_repository)
    ],
) -> UserProfileService:
    return UserProfileService(
        session=session,
        user_repository=user_repository,
        profile_repository=profile_repository,
    )


def get_category_service(
    session: DB_SESSION,
    category_repository: Annotated[
        CategoryRepository, Depends(get_category_repository)
    ],
) -> CategoryService:
    return CategoryService(
        session=session,
        category_repository=category_repository,
    )


def get_product_service(
    session: DB_SESSION,
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    category_repository: Annotated[
        CategoryRepository, Depends(get_category_repository)
    ],
) -> ProductService:
    return ProductService(
        session=session,
        product_repository=product_repository,
        category_repository=category_repository,
    )


async def get_current_user(
    token: Annotated[str, Depends(o_auth2_scheme)],
    security_scopes: SecurityScopes,
    session: DB_SESSION,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    try:
        payload = decode_jwt_token(token)
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except jwt.PyJWTError:
        raise InvalidTokenException()

    if payload.get("type") != "access":
        raise InvalidTokenException("Invalid token type.")

    sub = payload.get("sub")
    if not sub:
        raise InvalidTokenException()

    try:
        user_id = UUID(sub)
    except ValueError:
        raise InvalidTokenException()

    user = await user_repository.get_user_by_id(user_id)
    if user:
        _ = user.role
        session.expunge_all()
    # Close SQLAlchemy's autobegin read transaction so services can call session.begin()
    await session.rollback()

    if not user:
        raise InvalidTokenException("User not found.")

    if not user.is_active:
        raise InactiveUserException()

    role_name = user.role.role if user.role else None
    allowed_scopes = SCOPES.get(role_name, [])

    for scope in security_scopes.scopes:
        if scope not in allowed_scopes:
            raise ForbiddenException(
                f"Not enough permissions. Missing scope: {scope}"
            )

    return user
