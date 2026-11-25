from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roles import Role


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role_id_by_role(self, role: str) -> Role:
        stmnt = select(Role).where(Role.role == role)

        data = await self.session.execute(stmnt)

        data = data.scalar_one_or_none()

        if data:
            return data.id
