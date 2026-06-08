from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.sessions.model import Session
from app.sessions.schemas import SessionCreate
from app.children.model import Child


async def create_session(
    db: AsyncSession, data: SessionCreate, user_id: int
) -> Session:
    child = await db.execute(
        select(Child).where(Child.child_id == data.child_id, Child.user_id == user_id)
    )
    if not child.scalar_one_or_none():
        return None
    session = Session(child_id=data.child_id, exercise_id=data.exercise_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_session_by_id(
    db: AsyncSession, session_id: int, user_id: int
) -> Session | None:
    result = await db.execute(
        select(Session)
        .join(Child, Session.child_id == Child.child_id)
        .where(Session.session_id == session_id, Child.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_sessions_by_child(
    db: AsyncSession, child_id: int, user_id: int, skip: int = 0, limit: int = 50
) -> list[Session]:
    result = await db.execute(
        select(Session)
        .join(Child, Session.child_id == Child.child_id)
        .where(Session.child_id == child_id, Child.user_id == user_id)
        .order_by(Session.started_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def end_session(db, session, metrics: dict, close_reason: str = "manual"):
    session.ended_at = datetime.now(timezone.utc)
    for key, value in metrics.items():
        setattr(session, key, value)
    session.close_reason = close_reason
    await db.commit()
    await db.refresh(session)
    return session
