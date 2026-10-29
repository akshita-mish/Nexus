import os
from dotenv import load_dotenv
from app.db.config import db
from app.users.schemas import UserCreate, UserResponse, UserLogin
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta

load_dotenv()


exp_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
print(type(exp_minutes))
secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")


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


def create_access_token(data: dict, expires_minutes: int = exp_minutes) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algo)


async def login_user(user: UserLogin):
    existing_user = await db.users.find_one({"email": user.email})
    if not existing_user:
        raise ValueError("User is not registered")

    entered_password = user.password.encode("utf-8")
    stored_hash = existing_user["password"].encode("utf-8")
    if bcrypt.checkpw(entered_password, stored_hash):
        print("Password matches!")
    else:
        print("Invalid password!")
    token = create_access_token({"sub": str(existing_user["_id"])})

    return {"access_token": token, "token_type": "bearer"}
