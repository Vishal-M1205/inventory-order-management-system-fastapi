from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions.custom_exception import ConflictException, NotFoundException
from app.models.roles import RoleEnum
from app.models.users import User
from app.repositories.implementations.role_repository import RoleRepository
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.user import RegisterUser


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        self.session = session
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def _register(self, user_data: RegisterUser, role: RoleEnum) -> User:
        async with self.session.begin():
            existing_user = await self.user_repository.get_user_by_email(
                user_data.email
            )
            if existing_user:
                raise ConflictException("User with this email already exists.")

            role_id = await self.role_repository.get_role_id_by_role(role)
            if not role_id:
                raise NotFoundException(f"Role '{role}' not found.")

            payload = user_data.model_dump(exclude={"password"})
            payload["hashed_password"] = hash_password(user_data.password)
            payload["role_id"] = role_id

            try:
                return await self.user_repository.insert_user(payload)
            except IntegrityError:
                raise ConflictException("User with this email already exists.")

    async def register_customer(self, customer_data: RegisterUser) -> User:
        return await self._register(customer_data, RoleEnum.CUSTOMER)

    async def register_employee(self, employee_data: RegisterUser) -> User:
        return await self._register(employee_data, RoleEnum.EMPLOYEE)

    async def register_manager(self, manager_data: RegisterUser) -> User:
        return await self._register(manager_data, RoleEnum.MANAGER)
