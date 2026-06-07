import pytest
from app.sessions.buffer import SessionBuffer


class TestSessionBuffer:
    async def test_append_and_flush(self):
        buf = SessionBuffer()
        await buf.append(1, {"ax": 0.1, "ay": 0.2})
        await buf.append(1, {"ax": 0.3, "ay": 0.4})
        data = await buf.flush(1)
        assert len(data) == 2
        assert data[0]["ax"] == 0.1
        assert data[1]["ax"] == 0.3

    async def test_flush_clears_data(self):
        buf = SessionBuffer()
        await buf.append(1, {"ax": 0.1})
        await buf.flush(1)
        data = await buf.flush(1)
        assert data == []

    async def test_flush_nonexistent_session(self):
        buf = SessionBuffer()
        data = await buf.flush(999)
        assert data == []

    async def test_multiple_sessions_independent(self):
        buf = SessionBuffer()
        await buf.append(1, {"val": "a"})
        await buf.append(2, {"val": "b"})
        data1 = await buf.flush(1)
        data2 = await buf.flush(2)
        assert len(data1) == 1
        assert len(data2) == 1
        assert data1[0]["val"] == "a"
        assert data2[0]["val"] == "b"
