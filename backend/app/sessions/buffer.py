import csv
import os
import threading
from collections import defaultdict
from typing import Any

RAW_DIR = "/raw_sessions"

FIELDS = ["ts", "ax", "ay", "az", "gx", "gy", "gz", "fsr"]


class SessionBuffer:
    def __init__(self):
        self._data: dict[int, list[dict[str, Any]]] = defaultdict(list)
        self._lock = threading.Lock()

    def append(self, session_id: int, reading: dict[str, Any]) -> None:
        with self._lock:
            self._data[session_id].append(reading)

    def flush(self, session_id: int) -> list[dict[str, Any]]:
        with self._lock:
            return self._data.pop(session_id, [])

    async def flush_to_csv(self, session_id: int) -> str | None:
        readings = self.flush(session_id)
        if not readings:
            return None
        os.makedirs(RAW_DIR, exist_ok=True)
        path = os.path.join(RAW_DIR, f"session_{session_id}.csv")
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(readings)
        return path


session_buffer = SessionBuffer()
