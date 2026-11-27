from typing import Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        return await self.session.get(Category, category_id)

    async def insert_category(self, category_data: dict) -> Category:
        category = Category(**category_data)
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def update_category(
        self, category_id: UUID, category_data: dict
    ) -> Optional[Category]:
        stmnt = (
            update(Category)
            .where(Category.id == category_id)
            .values(**category_data)
            .returning(Category)
        )
        result = await self.session.execute(stmnt)
        return result.scalar_one_or_none()
