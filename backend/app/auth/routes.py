from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.model import User
from app.auth.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este correo ya está en uso"
        )
    
    user = User(
        name = data.name,
        lastname = data.lastname,
        email = data.email,
        password = hash_password(data.password),
        phone = data.phone
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post(
        "/login", 
        response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401, 
            detail="Credenciales incorrectas"
        )

    token = create_access_token({"sub": str(user.user_id)})
    return {"access_token": token}