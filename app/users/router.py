from fastapi import APIRouter
from app.users.schemas import UserResponse, UserCreate
from app.users.service import register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await register_user(user)
