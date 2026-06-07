import uuid
from httpx import AsyncClient


class TestAuthRegister:
    async def test_register_success(self, client: AsyncClient):
        email = f"juan_{uuid.uuid4().hex[:8]}@test.com"
        payload = {
            "name": "Juan",
            "lastname": "Pérez",
            "email": email,
            "password": "123456",
            "phone": "555-0101",
        }
        resp = await client.post("/auth/register", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == email
        assert data["name"] == "Juan"
        assert "user_id" in data
        assert "password" not in data

    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        payload = {
            "name": "Otro",
            "lastname": "User",
            "email": test_user.email,
            "password": "123456",
        }
        resp = await client.post("/auth/register", json=payload)
        assert resp.status_code == 400
        assert "ya está en uso" in resp.json()["detail"]


class TestAuthLogin:
    async def test_login_success(self, client: AsyncClient, test_user):
        payload = {"email": test_user.email, "password": "123456"}
        resp = await client.post("/auth/login", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        payload = {"email": test_user.email, "password": "wrong"}
        resp = await client.post("/auth/login", json=payload)
        assert resp.status_code == 401
        assert "incorrectas" in resp.json()["detail"]

    async def test_login_nonexistent_user(self, client: AsyncClient):
        payload = {"email": "noexiste@test.com", "password": "123456"}
        resp = await client.post("/auth/login", json=payload)
        assert resp.status_code == 401
