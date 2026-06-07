from collections import defaultdict
import asyncio
from typing import Any


class SessionBuffer:
    def __init__(self):
        self._data: dict[int, list[dict[str, Any]]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def append(self, session_id: int, reading: dict[str, Any]) -> None:
        async with self._lock:
            self._data[session_id].append(reading)

    async def flush(self, session_id: int) -> list[dict[str, Any]]:
        async with self._lock:
            return self._data.pop(session_id, [])


session_buffer = SessionBuffer()
