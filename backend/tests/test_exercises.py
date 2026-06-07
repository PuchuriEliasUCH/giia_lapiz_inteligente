import pytest
from httpx import AsyncClient


class TestStrokeTypes:
    async def test_list_stroke_types(self, client: AsyncClient):
        resp = await client.get("/stroke-types")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)


class TestExercises:
    async def test_list_exercises(self, client: AsyncClient):
        resp = await client.get("/exercises")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    async def test_get_exercise_not_found(self, client: AsyncClient):
        resp = await client.get("/exercises/99999")
        assert resp.status_code == 404
