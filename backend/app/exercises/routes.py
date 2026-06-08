from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.exercises.schemas import (
    StrokeTypeResponse,
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseResponse,
)
from app.exercises import service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="", tags=["exercises"])


@router.get("/stroke-types", response_model=list[StrokeTypeResponse])
async def list_stroke_types(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.get_stroke_types(db)


@router.get("/exercises", response_model=list[ExerciseResponse])
async def list_exercises(
    stroke_type_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.get_exercises(db, stroke_type_id)


@router.get("/exercises/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    exercise = await service.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return exercise


@router.post(
    "/exercises",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_exercise(
    data: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    stroke_type = await service.get_stroke_type_by_id(db, data.stroke_type_id)
    if not stroke_type:
        raise HTTPException(status_code=400, detail="Tipo de trazo no válido")
    return await service.create_exercise(db, data)


@router.put("/exercises/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    data: ExerciseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    exercise = await service.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return await service.update_exercise(db, exercise, data)


@router.patch(
    "/exercises/{exercise_id}/deactivate",
    response_model=ExerciseResponse,
)
async def deactivate_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    exercise = await service.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    if not exercise.is_active:
        raise HTTPException(status_code=400, detail="El ejercicio ya está desactivado")
    return await service.deactivate_exercise(db, exercise)
