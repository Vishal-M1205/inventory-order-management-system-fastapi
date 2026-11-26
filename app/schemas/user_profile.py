from datetime import date, datetime
import re
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)

from app.core.constants import GENDER


def _validate_mobile(v: str) -> str:
    cleaned = re.sub(r"[\s\-\(\)]", "", v)
    if not re.match(r"^\+?[1-9]\d{9,12}$", cleaned):
        raise ValueError(
            "Mobile number must contain 10 to 13 digits, optionally starting with '+'."
        )
    return cleaned


def _validate_gender(v: str) -> str:
    normalized = v.strip().upper()
    if normalized not in GENDER:
        raise ValueError(
            f"Invalid gender '{v}'. Allowed values are: {', '.join(GENDER)}."
        )
    return normalized


def _validate_dob(v: date) -> date:
    today = date.today()
    if v >= today:
        raise ValueError("Date of birth must be a past date.")
    age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
    if age < 18:
        raise ValueError("User must be at least 18 years old.")
    return v


def _validate_address(v: str) -> str:
    trimmed = v.strip()
    if len(trimmed) < 5:
        raise ValueError("Address must be at least 5 characters long.")
    if len(trimmed) > 300:
        raise ValueError("Address cannot exceed 300 characters.")
    return trimmed


class UserProfileCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    mobile_number: str = Field(..., max_length=13, examples=["+919876543210"])
    gender: str = Field(..., max_length=10, examples=["MALE"])
    date_of_birth: date = Field(..., examples=["2001-05-20"])
    address: str = Field(..., min_length=5, max_length=300, examples=["123 Main St"])

    @field_validator("mobile_number")
    @classmethod
    def check_mobile(cls, v: str) -> str:
        return _validate_mobile(v)

    @field_validator("gender")
    @classmethod
    def check_gender(cls, v: str) -> str:
        return _validate_gender(v)

    @field_validator("date_of_birth")
    @classmethod
    def check_dob(cls, v: date) -> date:
        return _validate_dob(v)

    @field_validator("address")
    @classmethod
    def check_address(cls, v: str) -> str:
        return _validate_address(v)


class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    mobile_number: Optional[str] = Field(None, max_length=13)
    gender: Optional[str] = Field(None, max_length=10)
    date_of_birth: Optional[date] = None
    address: Optional[str] = Field(None, min_length=5, max_length=300)

    @field_validator("mobile_number")
    @classmethod
    def check_mobile(cls, v: Optional[str]) -> Optional[str]:
        return _validate_mobile(v) if v is not None else v

    @field_validator("gender")
    @classmethod
    def check_gender(cls, v: Optional[str]) -> Optional[str]:
        return _validate_gender(v) if v is not None else v

    @field_validator("date_of_birth")
    @classmethod
    def check_dob(cls, v: Optional[date]) -> Optional[date]:
        return _validate_dob(v) if v is not None else v

    @field_validator("address")
    @classmethod
    def check_address(cls, v: Optional[str]) -> Optional[str]:
        return _validate_address(v) if v is not None else v


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: UUID
    mobile_number: str
    gender: str
    date_of_birth: date
    address: str
    updated_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
