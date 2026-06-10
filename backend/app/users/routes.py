from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.auth.model import User
from app.users.schemas import UserProfile

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserProfile)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user
