from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Security, status

from app.api.dependecies.dependencies import (
    get_auth_service,
    get_current_user,
    get_user_service,
)
from app.schemas.auth import Token
from app.schemas.user import RegisterResponse, RegisterUser
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    service: Annotated[AuthService, Depends(get_auth_service)],
    login_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return await service.login(login_credentials.username, login_credentials.password)


@router.post("/register/employee", response_model=RegisterResponse)
async def register_employee(
    employee_data: RegisterUser,
    service: Annotated[UserService, Depends(get_user_service)],
    current_user=Security(get_current_user, scopes=["user:create"]),
):
    return await service.register_employee(employee_data)


@router.post("/register/customer", response_model=RegisterResponse)
async def register_customer(
    customer_data: RegisterUser,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.register_customer(customer_data)


@router.post("/register/manager", response_model=RegisterResponse)
async def register_manager(
    manager_data: RegisterUser,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.register_manager(manager_data)
