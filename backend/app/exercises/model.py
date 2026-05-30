from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func
from app.db.base import Base


class StrokeType(Base):
    __tablename__ = "stroke_types"

    stroke_type_id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(50),
        nullable=False,
        unique=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(50),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    stroke_type_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("stroke_types.stroke_type_id"),
        nullable=False
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )