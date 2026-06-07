import pytest
from httpx import AsyncClient


class TestChildrenCRUD:
    async def test_create_child_success(self, client: AsyncClient, token: str):
        payload = {"name": "Hijo Uno"}
        resp = await client.post(
            "/children/",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Hijo Uno"
        assert data["is_active"] is True
        assert "child_id" in data

    async def test_list_children(self, client: AsyncClient, token: str):
        resp = await client.get(
            "/children/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    async def test_get_child_by_id(self, client: AsyncClient, token: str):
        create = await client.post(
            "/children/",
            json={"name": "Hijo Para Get"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create.json()["child_id"]

        resp = await client.get(
            f"/children/{child_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Hijo Para Get"

    async def test_get_child_not_found(self, client: AsyncClient, token: str):
        resp = await client.get(
            "/children/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404

    async def test_update_child(self, client: AsyncClient, token: str):
        create = await client.post(
            "/children/",
            json={"name": "Antes"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create.json()["child_id"]

        resp = await client.put(
            f"/children/{child_id}",
            json={"name": "Despues"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Despues"

    async def test_deactivate_child(self, client: AsyncClient, token: str):
        create = await client.post(
            "/children/",
            json={"name": "Para Desactivar"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create.json()["child_id"]

        resp = await client.patch(
            f"/children/{child_id}/deactivate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    async def test_deactivate_twice_returns_400(self, client: AsyncClient, token: str):
        create = await client.post(
            "/children/",
            json={"name": "Desactivar Dos"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create.json()["child_id"]

        await client.patch(
            f"/children/{child_id}/deactivate",
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.patch(
            f"/children/{child_id}/deactivate",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400

    async def test_unauthorized_returns_403(self, client: AsyncClient):
        resp = await client.get("/children/")
        assert resp.status_code == 403
