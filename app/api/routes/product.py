from typing import Annotated

from fastapi import APIRouter, Depends, Security, status

from app.api.dependecies.dependencies import get_current_user, get_product_service
from app.models.users import User
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["product:create"])
    ],
):
    return await service.create_product(product_data)
