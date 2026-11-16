from uuid import UUID

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RegisterUser(BaseModel):
    full_name: str
    email: str
    password: str


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    full_name: str
    email: str
    hashed_password: str
    created_at: datetime
