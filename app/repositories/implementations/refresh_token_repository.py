from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, token_data: dict) -> RefreshToken:
        token = RefreshToken(**token_data)
        self.session.add(token)
        await self.session.flush()
        await self.session.refresh(token)
        return token

    async def get_by_jti_for_update(self, jti: UUID) -> Optional[RefreshToken]:
        stmnt = (
            select(RefreshToken)
            .where(RefreshToken.jti == jti)
            .with_for_update()
        )
        result = await self.session.execute(stmnt)
        return result.scalar_one_or_none()

    async def revoke_family(self, family_id: UUID, revoked_at: datetime) -> None:
        stmnt = (
            update(RefreshToken)
            .where(
                RefreshToken.family_id == family_id,
                RefreshToken.is_revoked.is_(False),
            )
            .values(is_revoked=True, revoked_at=revoked_at)
        )
        await self.session.execute(stmnt)

    async def revoke_all_for_user(self, user_id: UUID, revoked_at: datetime) -> None:
        stmnt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked.is_(False),
            )
            .values(is_revoked=True, revoked_at=revoked_at)
        )
        await self.session.execute(stmnt)
