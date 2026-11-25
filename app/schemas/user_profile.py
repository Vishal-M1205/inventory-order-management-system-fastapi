from datetime import date, datetime
import re
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.core.constants import GENDER


class UserProfileCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Age of the user (must be between 18 and 120)",
        examples=[25],
    )
    mobile_number: str = Field(
        ...,
        max_length=13,
        description="Mobile number with optional country code, 10 to 13 digits (e.g. +919876543210)",
        examples=["+919876543210"],
    )
    gender: str = Field(
        ...,
        max_length=10,
        description="Gender of the user (MALE, FEMALE, or OTHER)",
        examples=["MALE"],
    )
    date_of_birth: date = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format",
        examples=["2001-05-20"],
    )
    address: str = Field(
        ...,
        min_length=5,
        max_length=300,
        description="Full residential address (between 5 and 300 characters)",
        examples=["123 Main Street, Springfield"],
    )

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError("Age must be at least 18 years old.")
        if v > 120:
            raise ValueError("Age must be less than or equal to 120.")
        return v

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, v: str) -> str:
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        # Matches optional '+' followed by 10 to 12 digits (total length 10 to 13)
        pattern = r"^\+?[1-9]\d{9,12}$"
        if not re.match(pattern, cleaned):
            raise ValueError(
                "Mobile number must contain 10 to 13 digits, optionally starting with '+' (e.g. +919876543210 or 9876543210)."
            )
        return cleaned

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        normalized = v.strip().upper()
        if normalized not in GENDER:
            raise ValueError(
                f"Invalid gender '{v}'. Allowed values are: {', '.join(GENDER)}."
            )
        return normalized

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: date) -> date:
        today = date.today()
        if v >= today:
            raise ValueError("Date of birth must be a past date.")

        # Minimum age requirement: 18 years
        calculated_age = (
            today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        )
        if calculated_age < 18:
            raise ValueError("User must be at least 18 years old.")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Address cannot be empty or whitespace only.")
        if len(trimmed) < 5:
            raise ValueError("Address must be at least 5 characters long.")
        if len(trimmed) > 300:
            raise ValueError("Address cannot exceed 300 characters.")
        return trimmed

    @model_validator(mode="after")
    def validate_age_matches_dob(self) -> "UserProfileCreate":
        today = date.today()
        dob = self.date_of_birth
        calculated_age = (
            today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        )
        if self.age != calculated_age:
            raise ValueError(
                f"Provided age ({self.age}) does not match date of birth ({dob}). Expected age is {calculated_age}."
            )
        return self


class UserProfileUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    age: Optional[int] = Field(None, ge=18, le=120)
    mobile_number: Optional[str] = Field(
        None,
        max_length=13,
    )
    gender: Optional[str] = Field(None, max_length=10)
    date_of_birth: Optional[date] = None
    address: Optional[str] = Field(None, min_length=5, max_length=300)

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            normalized = v.strip().upper()
            if normalized not in GENDER:
                raise ValueError(
                    f"Invalid gender '{v}'. Allowed values are: {', '.join(GENDER)}."
                )
            return normalized
        return v

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            cleaned = re.sub(r"[\s\-\(\)]", "", v)
            if not re.match(r"^\+?[1-9]\d{9,12}$", cleaned):
                raise ValueError(
                    "Mobile number must contain 10 to 13 digits, optionally starting with '+'."
                )
            return cleaned
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, v: Optional[date]) -> Optional[date]:
        if v is not None:
            today = date.today()
            if v >= today:
                raise ValueError("Date of birth must be a past date.")
            calculated_age = (
                today.year - v.year - ((today.month, today.day) < (v.month, v.day))
            )
            if calculated_age < 18:
                raise ValueError("User must be at least 18 years old.")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            trimmed = v.strip()
            if not trimmed:
                raise ValueError("Address cannot be empty or whitespace only.")
            return trimmed
        return v


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: UUID 
    age: int
    mobile_number: str
    gender: str
    date_of_birth: date | datetime
    address: str
