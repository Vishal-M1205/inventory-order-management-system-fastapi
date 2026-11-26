from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Security, status

from app.api.dependecies.dependencies import (
    get_current_user,
    get_user_profile_service,
)
from app.models.users import User
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileResponse,
    UserProfileUpdate,
)
from app.services.user_profile_service import UserProfileService

router = APIRouter(prefix="/api/profiles", tags=["User Profiles"])


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["profile:read:self"])
    ],
):
    return await service.get_my_profile(current_user)


@router.post(
    "/me",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_profile(
    profile_data: UserProfileCreate,
    service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["profile:update:self"])
    ],
):
    return await service.create_my_profile(current_user, profile_data)


@router.patch("/me", response_model=UserProfileResponse)
async def update_my_profile(
    profile_data: UserProfileUpdate,
    service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["profile:update:self"])
    ],
):
    return await service.update_my_profile(current_user, profile_data)


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: UUID,
    service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["profile:read:any"])
    ],
):
    return await service.get_user_profile(current_user, user_id)


@router.patch("/{user_id}", response_model=UserProfileResponse)
async def update_user_profile(
    user_id: UUID,
    profile_data: UserProfileUpdate,
    service: Annotated[UserProfileService, Depends(get_user_profile_service)],
    current_user: Annotated[
        User, Security(get_current_user, scopes=["profile:update:any"])
    ],
):
    return await service.update_user_profile(current_user, user_id, profile_data)
