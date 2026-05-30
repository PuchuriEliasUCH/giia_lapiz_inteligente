from sqlalchemy import Column, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT
from sqlalchemy.sql import func
from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    child_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("children.child_id"),
        nullable=False
    )

    exercise_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("exercises.exercise_id"),
        nullable=False
    )

    started_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    ended_at = Column(
        DateTime,
        nullable=True
    )

    avg_pressure = Column(Float, nullable=True)
    max_pressure = Column(Float, nullable=True)
    pressure_stability = Column(Float, nullable=True)
    movement_stability = Column(Float, nullable=True)
    tremor_level = Column(Float, nullable=True)
    posture_score = Column(Float, nullable=True)

    total_errors = Column(
        SMALLINT(unsigned=True),
        nullable=True,
        default=0
    )

    feedback_count = Column(
        SMALLINT(unsigned=True),
        nullable=True,
        default=0
    )

    ai_score = Column(Float, nullable=True)

    result_summary = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )