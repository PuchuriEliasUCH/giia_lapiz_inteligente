import pytest
from app.sessions.buffer import SessionBuffer


class TestSessionBuffer:
    def test_append_and_flush(self):
        buf = SessionBuffer()
        buf.append(1, {"ax": 0.1, "ay": 0.2})
        buf.append(1, {"ax": 0.3, "ay": 0.4})
        data = buf.flush(1)
        assert len(data) == 2
        assert data[0]["ax"] == 0.1
        assert data[1]["ax"] == 0.3

    def test_flush_clears_data(self):
        buf = SessionBuffer()
        buf.append(1, {"ax": 0.1})
        buf.flush(1)
        data = buf.flush(1)
        assert data == []

    def test_flush_nonexistent_session(self):
        buf = SessionBuffer()
        data = buf.flush(999)
        assert data == []

    def test_multiple_sessions_independent(self):
        buf = SessionBuffer()
        buf.append(1, {"val": "a"})
        buf.append(2, {"val": "b"})
        data1 = buf.flush(1)
        data2 = buf.flush(2)
        assert len(data1) == 1
        assert len(data2) == 1
        assert data1[0]["val"] == "a"
        assert data2[0]["val"] == "b"
