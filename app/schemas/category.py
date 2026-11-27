from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = Field(
        default="No description provided.", min_length=10, max_length=300
    )


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: Optional[str] = Field(default=None, min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, min_length=10, max_length=300)


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str] = None
