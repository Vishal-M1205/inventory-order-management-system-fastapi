from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        stmnt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmnt)
        return result.scalar_one_or_none()

    async def get_user_by_email(
        self, user_email: str, active_only: bool = False
    ) -> Optional[User]:
        stmnt = select(User).where(User.email == user_email)
        if active_only:
            stmnt = stmnt.where(User.is_active.is_(True))
        result = await self.session.execute(stmnt)
        return result.scalar_one_or_none()

    async def insert_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
