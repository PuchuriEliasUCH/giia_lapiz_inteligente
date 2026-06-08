from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SessionCreate(BaseModel):
    child_id: int
    exercise_id: int


class SessionEndRequest(BaseModel):
    close_reason: str = "manual"


class SessionResponse(BaseModel):
    session_id: int
    child_id: int
    exercise_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    close_reason: Optional[str] = None
    avg_pressure: Optional[float] = None
    max_pressure: Optional[float] = None
    pressure_stability: Optional[float] = None
    movement_stability: Optional[float] = None
    tremor_level: Optional[float] = None
    posture_score: Optional[float] = None
    total_errors: Optional[int] = None
    feedback_count: Optional[int] = None
    ai_score: Optional[float] = None
    result_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
