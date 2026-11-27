from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.models.category import Category
from app.repositories.implementations.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, session: AsyncSession, category_repository: CategoryRepository):
        self.session = session
        self.category_repository = category_repository

    async def create_category(self, payload: CategoryCreate) -> Category:
        async with self.session.begin():
            try:
                return await self.category_repository.insert_category(
                    payload.model_dump()
                )
            except IntegrityError:
                raise ConflictException(
                    detail="Category with this name already exists."
                )

    async def update_category(
        self, category_id: UUID, category_data: CategoryUpdate
    ) -> Category:
        async with self.session.begin():
            payload = category_data.model_dump(exclude_unset=True)

            if not payload:
                raise BadRequestException(detail="No fields provided to update.")

            if "name" in payload and payload["name"] is None:
                raise BadRequestException(detail="Category name cannot be null.")

            try:
                updated_category = await self.category_repository.update_category(
                    category_id, payload
                )
            except IntegrityError:
                raise ConflictException(
                    detail="Category with this name already exists."
                )

            if not updated_category:
                raise NotFoundException("Category not found.")

            return updated_category
