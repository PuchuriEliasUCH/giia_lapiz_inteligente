from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.sessions.schemas import SessionCreate, SessionEnd, SessionResponse
from app.sessions import service
from app.sessions.buffer import session_buffer
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["sessions"])


@router.post(
    "/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_session(
    data: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.create_session(db, data)


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    session = await service.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return session


@router.get("/children/{child_id}/sessions", response_model=list[SessionResponse])
async def list_sessions(
    child_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.get_sessions_by_child(db, child_id, skip, limit)


@router.patch("/sessions/{session_id}/end", response_model=SessionResponse)
async def end_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    session = await service.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    if session.ended_at is not None:
        raise HTTPException(status_code=400, detail="La sesión ya ha terminado")
    csv_path = await session_buffer.flush_to_csv(session_id)
    metrics = {}
    if csv_path:
        from app.sessions.metrics import calculate_metrics
        metrics = calculate_metrics(csv_path)
    return await service.end_session(db, session, metrics)