from sqlalchemy import Column, String, Text, Date, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func
from app.db.base import Base


class Child(Base):
    __tablename__ = "children"

    child_id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        INTEGER(unsigned=True),
        ForeignKey("users.user_id"),
        nullable=False
    )

    name = Column(
        String(80),
        nullable=False
    )

    birth_date = Column(
        Date,
        nullable=True
    )

    dominant_hand = Column(
        Enum("derecha", "izquierda", "ambidiestro"),
        nullable=False,
        default="derecha"
    )

    school_grade = Column(
        String(30),
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
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