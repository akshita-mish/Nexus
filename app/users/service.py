from app.db.config import db
from app.users.schemas import UserCreate, UserResponse
import bcrypt
from datetime import datetime, timezone


async def register_user(user: UserCreate):
    existing_user = await db.users.find_one({"email": str(user.email)})
    if existing_user:
        raise ValueError("Email already exists")

    plain_password = user.password
    # Convert the password string to bytes
    password_bytes = plain_password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")
    now = datetime.now(timezone.utc)

    user_doc = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "is_active": True,
        "is_verified": False,
        "created_at": now,
        "updated_at": now,
    }

    result = await db.users.insert_one(user_doc)

    return UserResponse(
        id=str(result.inserted_id),
        name=user.name,
        email=str(user.email),
        is_active=True,
        is_verified=False,
        created_at=now,
        updated_at=now,
    )
