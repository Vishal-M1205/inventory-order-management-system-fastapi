from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.database import get_db_session
from app.repositories.implementations.user_repository import UserRepository
from app.services.user_service import UserService

DB_SESSION = Annotated[AsyncSession, Depends(get_db_session)]


def get_user_repository(session: DB_SESSION):
    return UserRepository(session=session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    session: DB_SESSION,
):
    return UserService(session=session, repository=repository)
