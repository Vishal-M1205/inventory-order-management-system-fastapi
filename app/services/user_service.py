from typing import Optional
from app.core.security import hash_password
from app.exceptions.custom_exception import ConflictException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.repositories.implementations.user_repository import UserRepository
from app.schemas.user import RegisterUser


class UserService:
    def __init__(self, session: AsyncSession, user_repository: UserRepository):
        self.session = session
        self.user_repository = user_repository

    async def register_employee(self, employee_data: RegisterUser) -> Optional[User]:
        async with self.session.begin():

            existing_user = await self.repository.get_user_by_email(employee_data.email)

            if existing_user:
                raise ConflictException("User with this email already found.")

            hashed_password = hash_password(employee_data.password)

            employee_data = employee_data.model_dump(exclude={"password"})
            employee_data["hashed_password"] = hashed_password

            user = await self.repository.insert_user(employee_data)

            return user
