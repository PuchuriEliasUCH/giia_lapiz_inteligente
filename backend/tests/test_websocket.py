import asyncio
import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from app.main import app
from app.websocket.manager import manager
from app.core.security import create_access_token


class TestWebSocket:
    def test_ws_connect_valid_token(self):
        token = create_access_token({"sub": "1"})
        with TestClient(app) as client:
            with client.websocket_connect(f"/ws/sessions/1?token={token}") as ws:
                assert manager.is_connected(1)

    def test_ws_rejects_invalid_token(self):
        with TestClient(app) as client:
            with pytest.raises(WebSocketDisconnect) as exc:
                with client.websocket_connect("/ws/sessions/1?token=invalid"):
                    pass
            assert exc.value.code == 1008

    def test_ws_rejects_missing_token(self):
        with TestClient(app) as client:
            with pytest.raises(WebSocketDisconnect) as exc:
                with client.websocket_connect("/ws/sessions/1"):
                    pass
            assert exc.value.code == 1008

    def test_manager_send_delivers_json(self):
        token = create_access_token({"sub": "1"})
        with TestClient(app) as client:
            with client.websocket_connect(f"/ws/sessions/2?token={token}") as ws:
                asyncio.run(manager.send(2, {"id": "test", "feedback": "hello"}))
                data = ws.receive_json()
                assert data["id"] == "test"
                assert data["feedback"] == "hello"
