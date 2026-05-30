from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.children.model import Child
from app.children.schemas import ChildCreate, ChildUpdate, ChildResponse
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/children", tags=["children"])


@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
def create_child(
    data: ChildCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    child = Child(**data.model_dump(), user_id=current_user.user_id)
    db.add(child)
    db.commit()
    db.refresh(child)
    return child


@router.get("/", response_model=list[ChildResponse])
def get_children(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Child).filter(Child.user_id == current_user.user_id, Child.is_active == True).all()


@router.get("/{child_id}", response_model=ChildResponse)
def get_child(
    child_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    child = (
        db.query(Child)
        .filter(Child.child_id == child_id, Child.user_id == current_user.user_id)
        .first()
    )
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    return child


@router.put("/{child_id}", response_model=ChildResponse)
def update_child(
    child_id: int,
    data: ChildUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    child = (
        db.query(Child)
        .filter(Child.child_id == child_id, Child.user_id == current_user.user_id)
        .first()
    )
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(child, key, value)
    db.commit()
    db.refresh(child)
    return child


@router.patch("/{child_id}/deactivate", response_model=ChildResponse)
def deactivate_child(child_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    child = db.query(Child).filter(Child.child_id == child_id, Child.user_id == current_user.user_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    if not child.is_active:
        raise HTTPException(status_code=400, detail="El niño ya está desactivado")
    child.is_active = False
    db.commit()
    db.refresh(child)
    return child