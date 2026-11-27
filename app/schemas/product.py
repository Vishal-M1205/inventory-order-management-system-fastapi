from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    category_id: UUID
    name: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = Field(
        default="No description provided.", min_length=10, max_length=300
    )
    selling_price: Decimal = Field(..., decimal_places=2, max_digits=13, ge=0)
    net_weight_kilogram: Decimal = Field(..., decimal_places=2, max_digits=5, ge=0)


class ProductUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    category_id: Optional[UUID] = None
    name: Optional[str] = Field(default=None, min_length=5, max_length=100)
    description: Optional[str] = Field(default=None, min_length=10, max_length=300)
    selling_price: Optional[Decimal] = Field(
        default=None, decimal_places=2, max_digits=13, ge=0
    )
    net_weight_kilogram: Optional[Decimal] = Field(
        default=None, decimal_places=2, max_digits=5, ge=0
    )
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    category_id: UUID
    name: str
    sku: str
    description: Optional[str] = None
    selling_price: Decimal
    net_weight_kilogram: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime
