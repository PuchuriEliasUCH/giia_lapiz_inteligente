from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum


class DominantHand(str, Enum):
    derecha = "derecha"
    izquierda = "izquierda"
    ambidiestro = "ambidiestro"


class ChildCreate(BaseModel):
    name: str
    birth_date: Optional[date] = None
    dominant_hand: DominantHand = DominantHand.derecha
    school_grade: Optional[str] = None
    notes: Optional[str] = None


class ChildUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    dominant_hand: Optional[DominantHand] = None
    school_grade: Optional[str] = None
    notes: Optional[str] = None


class ChildResponse(BaseModel):
    child_id: int
    user_id: int
    name: str
    birth_date: Optional[date] = None
    dominant_hand: DominantHand
    school_grade: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
