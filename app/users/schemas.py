from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, strip_whitespace=True)
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
