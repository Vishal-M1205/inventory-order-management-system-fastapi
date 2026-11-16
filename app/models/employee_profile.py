from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Uuid
from typing import TYPE_CHECKING
from app.core.constants import GENDER
from datetime import datetime
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:

    from app.models.users import User


class EmployeeProfile(Base):
    __tablename__ = "employee_profile"

    __table_args__ = (
        CheckConstraint("age >= 18", name="employee_profile_age_check"),
        CheckConstraint(f"gender IN {GENDER}"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), unique=True, index=True, nullable=False
    )
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    mobile_numner: Mapped[str] = mapped_column(String(13), nullable=False, index=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    address: Mapped[str] = mapped_column(String(300), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="profile")
