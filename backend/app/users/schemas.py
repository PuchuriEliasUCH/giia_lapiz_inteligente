from pydantic import BaseModel
from datetime import datetime


class UserProfile(BaseModel):
    user_id: int
    name: str
    lastname: str
    email: str
    phone: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
