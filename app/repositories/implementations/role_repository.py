from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roles import Role, RoleEnum


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role_by_name(self, role: RoleEnum | str) -> Optional[Role]:
        stmnt = select(Role).where(Role.role == str(role))
        result = await self.session.execute(stmnt)
        return result.scalar_one_or_none()

    async def get_role_id_by_role(self, role: RoleEnum | str) -> Optional[UUID]:
        role_obj = await self.get_role_by_name(role)
        return role_obj.id if role_obj else None
