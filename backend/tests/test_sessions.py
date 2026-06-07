import uuid
from httpx import AsyncClient


async def _ensure_seed_data(db_session, client, token):
    from app.exercises.model import StrokeType
    from sqlalchemy import select

    result = await db_session.execute(select(StrokeType))
    stroke_types = result.scalars().all()
    if stroke_types:
        return stroke_types[0].stroke_type_id

    st = StrokeType(name=f"trazado_{uuid.uuid4().hex[:6]}")
    db_session.add(st)
    await db_session.commit()
    await db_session.refresh(st)

    name = f"ej_{uuid.uuid4().hex[:8]}"
    resp = await client.post(
        "/exercises",
        json={"name": name, "stroke_type_id": st.stroke_type_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    return resp.json()["exercise_id"]


class TestSessions:
    async def test_create_session(self, client: AsyncClient, token: str, db_session):
        exercise_id = await _ensure_seed_data(db_session, client, token)
        create_child = await client.post(
            "/children/",
            json={"name": "Niño Sesión"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create_child.json()["child_id"]

        resp = await client.post(
            "/sessions",
            json={"child_id": child_id, "exercise_id": exercise_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["child_id"] == child_id
        assert data["exercise_id"] == exercise_id
        assert "session_id" in data

    async def test_get_session_not_found(self, client: AsyncClient, token: str):
        resp = await client.get(
            "/sessions/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404

    async def test_list_sessions_by_child(
        self, client: AsyncClient, token: str, db_session
    ):
        exercise_id = await _ensure_seed_data(db_session, client, token)
        create_child = await client.post(
            "/children/",
            json={"name": "Niño Historial"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create_child.json()["child_id"]

        await client.post(
            "/sessions",
            json={"child_id": child_id, "exercise_id": exercise_id},
            headers={"Authorization": f"Bearer {token}"},
        )

        resp = await client.get(
            f"/children/{child_id}/sessions",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_end_session(self, client: AsyncClient, token: str, db_session):
        exercise_id = await _ensure_seed_data(db_session, client, token)
        create_child = await client.post(
            "/children/",
            json={"name": "Niño Cerrar"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create_child.json()["child_id"]

        create = await client.post(
            "/sessions",
            json={"child_id": child_id, "exercise_id": exercise_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        session_id = create.json()["session_id"]

        resp = await client.patch(
            f"/sessions/{session_id}/end",
            json={
                "avg_pressure": 12.5,
                "max_pressure": 45.0,
                "result_summary": "Buen trabajo",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["avg_pressure"] == 12.5
        assert data["ended_at"] is not None

    async def test_end_session_twice_returns_400(
        self, client: AsyncClient, token: str, db_session
    ):
        exercise_id = await _ensure_seed_data(db_session, client, token)
        create_child = await client.post(
            "/children/",
            json={"name": "Niño Doble"},
            headers={"Authorization": f"Bearer {token}"},
        )
        child_id = create_child.json()["child_id"]

        create = await client.post(
            "/sessions",
            json={"child_id": child_id, "exercise_id": exercise_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        session_id = create.json()["session_id"]

        await client.patch(
            f"/sessions/{session_id}/end",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.patch(
            f"/sessions/{session_id}/end",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400
