import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from app.db.config import db
from app.users.service import secret_key, algo

bearer_schema = HTTPBearer()


async def get_current_user(creds=Depends(bearer_schema)):
    # 1. Get the token from the "Authorization: Bearer <token>" header
    token = creds.credentials

    # 2. Decode the token (fails if it's fake or expired)
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algo])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 3. Get the user id we stored in the token at login
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 4. Find the user in the database
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        print(type(user))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    user["id"] = str(user["_id"])
    user.pop("_id")
    user.pop("password")
    return user
