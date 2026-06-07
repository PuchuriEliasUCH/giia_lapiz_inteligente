from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.children.schemas import ChildCreate, ChildUpdate, ChildResponse
from app.children import service
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/children", tags=["children"])


@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child(
    data: ChildCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.create_child(db, data, current_user.user_id)


@router.get("/", response_model=list[ChildResponse])
async def get_children(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.get_children_by_user(db, current_user.user_id)


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    child = await service.get_child_by_id(db, child_id, current_user.user_id)
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    return child


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(
    child_id: int,
    data: ChildUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    child = await service.get_child_by_id(db, child_id, current_user.user_id)
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    return await service.update_child(db, child, data)


@router.patch("/{child_id}/deactivate", response_model=ChildResponse)
async def deactivate_child(
    child_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    child = await service.get_child_by_id(db, child_id, current_user.user_id)
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    if not child.is_active:
        raise HTTPException(status_code=400, detail="El niño ya está desactivado")
    return await service.deactivate_child(db, child)
