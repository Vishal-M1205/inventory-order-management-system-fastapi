from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, user_email: str) -> Optional[User]:
        stmnt = select(User).where(
            and_(User.email == user_email, User.is_active == True)
        )

        data = await self.session.execute(stmnt)

        return data.scalar_one_or_none()

    async def insert_user(
        self,
        user_data: dict,
    ) -> User:
        user = User(**user_data)

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

        return user
