from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.mixins import TimestampMixin


class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    code: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    company_name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    contact_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    contact_number: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    gst_number: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, unique=True
    )
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
