from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException

from app.db.config import db
from app.users.dependency import get_current_user


def require_role(*allowed_roles: str):  # all the rolw wil be stored in a tuple
    async def checker(workspace_id: str, current_user=Depends(get_current_user)):
        # 1. Make sure the id in the URL is a valid ObjectId
        try:
            workspace_oid = ObjectId(workspace_id)
        except InvalidId:
            raise HTTPException(status_code=404, detail="Workspace not found")

        # 2. Is this user a member of this workspace?
        member = await db.workspace_members.find_one(
            {
                "workspace_id": workspace_oid,
                "user_id": ObjectId(current_user["id"]),
            }
        )
        if not member:
            # 404 (not 403) so we don't reveal the workspace exists
            raise HTTPException(status_code=404, detail="Workspace not found")

        # 3. Does their role allow this action?
        if member["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")

        return member  # contains "role", "user_id", "workspace_id"

    return checker
