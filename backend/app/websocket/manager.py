import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self._connections: dict[int, WebSocket] = {}

    async def connect(self, session_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self._connections[session_id] = ws
        logger.info(f"WebSocket conectado: session_id={session_id}")

    def disconnect(self, session_id: int) -> None:
        self._connections.pop(session_id, None)
        logger.info(f"WebSocket desconectado: session_id={session_id}")

    async def send(self, session_id: int, data: dict) -> None:
        ws = self._connections.get(session_id)
        if ws is None:
            return
        try:
            await ws.send_json(data)
        except Exception as e:
            logger.warning(f"Error enviando WebSocket a session_id={session_id}: {e}")
            self.disconnect(session_id)

    def is_connected(self, session_id: int) -> bool:
        return session_id in self._connections


manager = ConnectionManager()
