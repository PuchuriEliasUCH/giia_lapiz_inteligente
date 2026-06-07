from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.model import User
from app.auth.schemas import UserRegister
from app.core.security import hash_password


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, data: UserRegister) -> User:
    user = User(
        name=data.name,
        lastname=data.lastname,
        email=data.email,
        password=hash_password(data.password),
        phone=data.phone,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
