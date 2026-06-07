from collections.abc import AsyncGenerator
from uuid import uuid4
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.core.config import settings
from app.db.database import get_db, AsyncSessionLocal
from app.auth.model import User
from app.core.security import hash_password, create_access_token


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    conn = await engine.connect()
    await conn.begin()

    session = AsyncSession(bind=conn, expire_on_commit=False)

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield session
    finally:
        await session.close()
        await conn.rollback()
        await conn.close()
        await engine.dispose()
        app.dependency_overrides.pop(get_db, None)


def _unique_email() -> str:
    return f"test_{uuid4().hex[:8]}@test.com"


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    user = User(
        name="Test",
        lastname="User",
        email=_unique_email(),
        password=hash_password("123456"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def token(test_user: User) -> str:
    return create_access_token({"sub": str(test_user.user_id)})
