from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exercises.model import StrokeType, Exercise
from app.exercises.schemas import ExerciseCreate, ExerciseUpdate


async def get_stroke_types(db: AsyncSession) -> list[StrokeType]:
    result = await db.execute(select(StrokeType).order_by(StrokeType.name))
    return result.scalars().all()


async def get_stroke_type_by_id(
    db: AsyncSession, stroke_type_id: int
) -> StrokeType | None:
    result = await db.execute(
        select(StrokeType).where(StrokeType.stroke_type_id == stroke_type_id)
    )
    return result.scalar_one_or_none()


async def get_exercises(
    db: AsyncSession, stroke_type_id: int | None = None
) -> list[Exercise]:
    stmt = select(Exercise).where(Exercise.is_active == True)
    if stroke_type_id is not None:
        stmt = stmt.where(Exercise.stroke_type_id == stroke_type_id)
    stmt = stmt.order_by(Exercise.name)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_exercise_by_id(db: AsyncSession, exercise_id: int) -> Exercise | None:
    result = await db.execute(
        select(Exercise).where(Exercise.exercise_id == exercise_id)
    )
    return result.scalar_one_or_none()


async def create_exercise(db: AsyncSession, data: ExerciseCreate) -> Exercise:
    exercise = Exercise(**data.model_dump())
    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)
    return exercise


async def update_exercise(
    db: AsyncSession, exercise: Exercise, data: ExerciseUpdate
) -> Exercise:
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(exercise, key, value)
    await db.commit()
    await db.refresh(exercise)
    return exercise


async def deactivate_exercise(db: AsyncSession, exercise: Exercise) -> Exercise:
    exercise.is_active = False
    await db.commit()
    await db.refresh(exercise)
    return exercise
