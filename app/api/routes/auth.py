from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependecies.dependencies import get_user_service
from app.schemas.user import RegisterResponse, RegisterUser
from app.services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register/employee", response_model=RegisterResponse)
async def register_employee(
    employee_data: RegisterUser,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.register_employee(employee_data)
