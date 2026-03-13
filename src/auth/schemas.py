from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


def datetime_to_gmt_str(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
        from_attributes=True
    )


class UserCreate(BaseSchema):
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=72, description="Password (max 72 characters due to bcrypt limitation)")


class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(BaseSchema):
    id: UUID
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseSchema):
    username: str
    password: str = Field(max_length=72, description="Password (max 72 characters)")


class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    user_id: UUID
    username: str