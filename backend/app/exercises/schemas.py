from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StrokeTypeResponse(BaseModel):
    stroke_type_id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    stroke_type_id: int


class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    stroke_type_id: Optional[int] = None
    is_active: Optional[bool] = None


class ExerciseResponse(BaseModel):
    exercise_id: int
    name: str
    description: Optional[str] = None
    stroke_type_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
