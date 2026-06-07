from typing import Optional
from datetime import date, datetime
from sqlalchemy import String, Text, Date, Enum, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Child(Base):
    __tablename__ = "children"

    child_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True), ForeignKey("users.user_id")
    )
    name: Mapped[str] = mapped_column(String(80))
    birth_date: Mapped[Optional[date]] = mapped_column(Date)
    dominant_hand: Mapped[str] = mapped_column(
        Enum("derecha", "izquierda", "ambidiestro"), default="derecha"
    )
    school_grade: Mapped[Optional[str]] = mapped_column(String(30))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
