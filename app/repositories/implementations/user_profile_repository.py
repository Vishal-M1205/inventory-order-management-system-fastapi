from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_profile import UserProfile


class UserProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserProfile]:
        stmnt = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.session.execute(stmnt)
        return result.scalar_one_or_none()

    async def create(self, profile_data: dict) -> UserProfile:
        profile = UserProfile(**profile_data)
        self.session.add(profile)
        await self.session.flush()
        await self.session.refresh(profile)
        return profile

    async def update(self, profile: UserProfile, update_data: dict) -> UserProfile:
        for key, value in update_data.items():
            setattr(profile, key, value)
        await self.session.flush()
        await self.session.refresh(profile)
        return profile
