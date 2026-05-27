from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.mysql import INTEGER

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        INTEGER(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(80),
        nullable=False
    )

    lastname = Column(
        String(80),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False,
        unique=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    phone = Column(
        String(9),
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
        nullable=True,
        server_default=func.now(),
        onupdate=func.now()
    )