from typing import Optional
from datetime import datetime
from sqlalchemy import Text, DateTime, Float, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    child_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("children.child_id")
    )
    exercise_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("exercises.exercise_id")
    )
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    avg_pressure: Mapped[Optional[float]] = mapped_column(Float)
    max_pressure: Mapped[Optional[float]] = mapped_column(Float)
    pressure_stability: Mapped[Optional[float]] = mapped_column(Float)
    movement_stability: Mapped[Optional[float]] = mapped_column(Float)
    tremor_level: Mapped[Optional[float]] = mapped_column(Float)
    posture_score: Mapped[Optional[float]] = mapped_column(Float)
    total_errors: Mapped[Optional[int]] = mapped_column(
        SMALLINT(unsigned=True), default=0
    )
    feedback_count: Mapped[Optional[int]] = mapped_column(
        SMALLINT(unsigned=True), default=0
    )
    ai_score: Mapped[Optional[float]] = mapped_column(Float)
    result_summary: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
