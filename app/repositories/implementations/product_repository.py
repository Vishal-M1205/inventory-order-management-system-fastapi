from app.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_product(self, product_data: dict) -> Product:
        product = Product(**product_data)

        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)

        return product
