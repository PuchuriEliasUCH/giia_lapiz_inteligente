import asyncio
import logging
import threading
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.db.database import AsyncSessionLocal
from app.sessions.model import Session, CloseReason
from app.sessions.buffer import session_buffer
from app.sessions.metrics import calculate_metrics

logger = logging.getLogger(__name__)

SESSION_TIMEOUT_MINUTES = 10

_last_seen: dict[int, datetime] = {}
_lock = threading.Lock()


def update_last_seen(session_id: int) -> None:
    with _lock:
        _last_seen[session_id] = datetime.now(timezone.utc)


async def close_orphan_session(session_id: int) -> None:
    from app.mqtt.simulator import stop_simulation

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Session).where(
                Session.session_id == session_id,
                Session.ended_at == None,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            with _lock:
                _last_seen.pop(session_id, None)
            return

        await stop_simulation(session_id)

        csv_path = await session_buffer.flush_to_csv(session_id)
        metrics = {}
        if csv_path:
            metrics = calculate_metrics(csv_path)

        session.ended_at = datetime.now(timezone.utc)
        session.close_reason = CloseReason.timeout
        for key, value in metrics.items():
            setattr(session, key, value)
        await db.commit()
        logger.warning(
            f"Sesión huérfana cerrada automáticamente: session_id={session_id}"
        )
        with _lock:
            _last_seen.pop(session_id, None)


async def session_watchdog() -> None:
    logger.info("Watchdog de sesiones iniciado")
    while True:
        await asyncio.sleep(60)
        now = datetime.now(timezone.utc)
        timeout = timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        with _lock:
            orphans = [
                sid for sid, ts in list(_last_seen.items()) if (now - ts) > timeout
            ]
        for sid in orphans:
            await close_orphan_session(sid)
