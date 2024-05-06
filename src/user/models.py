from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    email: EmailStr
    salt:Optional[str] = None
    hashed_password: str
    created_date: Optional[datetime] = None

    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('Email cannot be empty')
        return value

