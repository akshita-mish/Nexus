from fastapi import APIRouter, Depends
from app.users.schemas import UserResponse, UserCreate, UserLogin
from app.users.service import register_user, login_user
from app.users.dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await register_user(user)


@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)


# to test protected route
@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return current_user
