from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_validator, constr

class Link(BaseModel):
    link: HttpUrl
    shortned_link: str
    created_date: datetime
    clicked: int = 0 
    user_id: Optional[str] = None

    @field_validator('link')
    def validate_link_length(cls, value):
        if len(str(value)) > 500:
            raise ValueError('Link must be at most 500 characters long')
        return value
