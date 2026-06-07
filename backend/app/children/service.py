from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.children.model import Child
from app.children.schemas import ChildCreate, ChildUpdate


async def get_children_by_user(db: AsyncSession, user_id: int) -> list[Child]:
    result = await db.execute(
        select(Child).where(Child.user_id == user_id, Child.is_active == True)
    )
    return result.scalars().all()


async def get_child_by_id(
    db: AsyncSession, child_id: int, user_id: int
) -> Child | None:
    result = await db.execute(
        select(Child).where(Child.child_id == child_id, Child.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_child(db: AsyncSession, data: ChildCreate, user_id: int) -> Child:
    child = Child(**data.model_dump(), user_id=user_id)
    db.add(child)
    await db.commit()
    await db.refresh(child)
    return child


async def update_child(db: AsyncSession, child: Child, data: ChildUpdate) -> Child:
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(child, key, value)
    await db.commit()
    await db.refresh(child)
    return child


async def deactivate_child(db: AsyncSession, child: Child) -> Child:
    child.is_active = False
    await db.commit()
    await db.refresh(child)
    return child
