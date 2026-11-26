from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import (
    ConflictException,
    ForbiddenException,
    NotFoundException,
)
from app.models.roles import RoleEnum
from app.models.user_profile import UserProfile
from app.models.users import User
from app.repositories.implementations.user_profile_repository import (
    UserProfileRepository,
)
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate


class UserProfileService:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        profile_repository: UserProfileRepository,
    ):
        self.session = session
        self.user_repository = user_repository
        self.profile_repository = profile_repository

    async def _validate_admin_target(
        self, actor: User, target_user_id: UUID
    ) -> User:
        if target_user_id == actor.id:
            raise ForbiddenException("Use /me to access or update your own profile.")

        target_user = await self.user_repository.get_user_by_id(target_user_id)
        if not target_user:
            raise NotFoundException("Target user not found.")

        if target_user.role and target_user.role.role == RoleEnum.ADMIN:
            raise ForbiddenException("Cannot access or modify an admin's profile.")

        return target_user

    async def get_my_profile(self, current_user: User) -> UserProfile:
        async with self.session.begin():
            profile = await self.profile_repository.get_by_user_id(current_user.id)
            if not profile:
                raise NotFoundException("Profile not found.")
            return profile

    async def create_my_profile(
        self, current_user: User, data: UserProfileCreate
    ) -> UserProfile:
        async with self.session.begin():
            existing = await self.profile_repository.get_by_user_id(current_user.id)
            if existing:
                raise ConflictException("Profile already exists for this user.")

            payload = data.model_dump()
            payload["user_id"] = current_user.id
            payload["updated_by"] = current_user.id

            try:
                return await self.profile_repository.create(payload)
            except IntegrityError:
                raise ConflictException(
                    "Profile already exists or mobile number is already in use."
                )

    async def update_my_profile(
        self, current_user: User, data: UserProfileUpdate
    ) -> UserProfile:
        async with self.session.begin():
            profile = await self.profile_repository.get_by_user_id(current_user.id)
            if not profile:
                raise NotFoundException("Profile not found.")

            update_data = data.model_dump(exclude_unset=True)
            update_data["updated_by"] = current_user.id

            try:
                return await self.profile_repository.update(profile, update_data)
            except IntegrityError:
                raise ConflictException("Mobile number is already in use.")

    async def get_user_profile(
        self, current_user: User, target_user_id: UUID
    ) -> UserProfile:
        async with self.session.begin():
            await self._validate_admin_target(current_user, target_user_id)
            profile = await self.profile_repository.get_by_user_id(target_user_id)
            if not profile:
                raise NotFoundException("Profile not found.")
            return profile

    async def update_user_profile(
        self, current_user: User, target_user_id: UUID, data: UserProfileUpdate
    ) -> UserProfile:
        async with self.session.begin():
            await self._validate_admin_target(current_user, target_user_id)
            profile = await self.profile_repository.get_by_user_id(target_user_id)
            if not profile:
                raise NotFoundException("Profile not found.")

            update_data = data.model_dump(exclude_unset=True)
            update_data["updated_by"] = current_user.id

            try:
                return await self.profile_repository.update(profile, update_data)
            except IntegrityError:
                raise ConflictException("Mobile number is already in use.")
