from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from identity_service.DB.enums import UserGender


class UserBass(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    first_name: str
    last_name: str
    gender: Optional[UserGender] = None
    email: str


class UserCreate(UserBass):
    # Note: max_digits is not valid for strings.
    # Use max_length instead, and optionally min_length or pattern.
    password: str = Field(..., max_length=10)


class UserRead(UserBass):
    user_id: UUID
    created_at: datetime


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
