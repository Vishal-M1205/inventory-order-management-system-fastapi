import re
import secrets

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import ConflictException, NotFoundException
from app.models.product import Product
from app.repositories.implementations.category_repository import CategoryRepository
from app.repositories.implementations.product_repository import ProductRepository
from app.schemas.product import ProductCreate


def _generate_sku(category_name: str, product_name: str) -> str:
    cat_clean = re.sub(r"[^A-Za-z0-9]", "", category_name).upper()
    prod_clean = re.sub(r"[^A-Za-z0-9]", "", product_name).upper()

    cat_prefix = (cat_clean[:3] or "CAT").ljust(3, "X")
    prod_prefix = (prod_clean[:4] or "PROD").ljust(4, "X")
    rand_suffix = secrets.token_hex(3).upper()

    return f"{cat_prefix}-{prod_prefix}-{rand_suffix}"


class ProductService:
    def __init__(
        self,
        session: AsyncSession,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
    ):
        self.session = session
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def create_product(self, product_data: ProductCreate) -> Product:
        async with self.session.begin():
            existing_category = await self.category_repository.get_category_by_id(
                product_data.category_id
            )
            if not existing_category:
                raise NotFoundException(detail="Category not found.")

            payload = product_data.model_dump()
            payload["sku"] = _generate_sku(existing_category.name, product_data.name)
            payload["is_active"] = True

            try:
                return await self.product_repository.insert_product(payload)
            except IntegrityError:
                raise ConflictException(detail="Product with this SKU already exists.")
