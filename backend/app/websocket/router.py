from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from app.websocket.manager import manager
from app.core.security import decode_access_token

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/sessions/{session_id}")
async def session_ws(
    session_id: int,
    ws: WebSocket,
    token: str = Query(...),
):
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(session_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(session_id)
