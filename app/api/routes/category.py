from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Security, status

from app.api.dependecies.dependencies import get_category_service, get_current_user
from app.models.users import User
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_data: CategoryCreate,
    service: Annotated[CategoryService, Depends(get_category_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["category:create"])
    ],
):
    return await service.create_category(category_data)


@router.patch(
    "/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK
)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    service: Annotated[CategoryService, Depends(get_category_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["category:update"])
    ],
):
    return await service.update_category(category_id, category_data)
