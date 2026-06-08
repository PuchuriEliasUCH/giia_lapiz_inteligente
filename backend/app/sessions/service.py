from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.sessions.model import Session
from app.sessions.schemas import SessionCreate


async def create_session(db: AsyncSession, data: SessionCreate) -> Session:
    session = Session(child_id=data.child_id, exercise_id=data.exercise_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_session_by_id(db: AsyncSession, session_id: int) -> Session | None:
    result = await db.execute(select(Session).where(Session.session_id == session_id))
    return result.scalar_one_or_none()


async def get_sessions_by_child(
    db: AsyncSession, child_id: int, skip: int = 0, limit: int = 50
) -> list[Session]:
    result = await db.execute(
        select(Session)
        .where(Session.child_id == child_id)
        .order_by(Session.started_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def end_session(db, session, metrics: dict):
    session.ended_at = datetime.now(timezone.utc)
    for key, value in metrics.items():
        setattr(session, key, value)
    await db.commit()
    await db.refresh(session)
    return session
