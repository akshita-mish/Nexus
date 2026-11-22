from datetime import datetime, timezone
from bson import ObjectId

from app.db.config import db
from app.workspaces.constants import OWNER
from app.workspaces.schemas import WorkspaceResponse


def to_response(workspace: dict, role: str) -> WorkspaceResponse:
    return WorkspaceResponse(
        id=str(workspace["_id"]),
        name=workspace["name"],
        description=workspace.get["description"],
        owner_id=str(workspace["owner_id"]),
        my_role=role,
        created_at=workspace["created_at"],
        updated_at=workspace["updated_at"],
    )


async def create_workspace(data, user_id: str) -> WorkspaceResponse:
    now = datetime.now(timezone.utc)

    # create the workspace
    workspace = {
        "name": data.name,
        "description": data.description,
        "owner_id": ObjectId(user_id),
        "created_id": now,
        "updated_at": now,
    }

    result = await db.workspace.insert_one(workspace)
    workspace["_id"] = result.inserted_id

    # 2. Add the creator as the owner member
    await db.workspace_member.insert_one(
        {
            "workspace_id": result.inserted_id,
            "user_id": user_id,
            "role": OWNER,
            "joined_at": now,
        }
    )

    return to_response(workspace, OWNER)


async def list_my_workspace(user_id: str) -> list[WorkspaceResponse]:
    # find the membership of the user
    membership = await db.workspace_member.find({"user_id": ObjectId(user_id)}).to_list(
        length=None
    )

    if not membership:
        return []
    # now store the workspace id and respective role in that
    role_by_workspace = {m["workspace_id"]: m["role"] for m in membership}

    workspaces = await db.workspace.find(
        {"_id": {"$in": list(role_by_workspace.keys())}}
    ).to_list(length=None)

    return [to_response(w, role_by_workspace[w["_id"]]) for w in workspaces]


async def get_workspace(workspace_id: str, role: str) -> WorkspaceResponse | None:
    workspace = await db.workspace.find_one({"_id": ObjectId(workspace_id)})
    if not workspace:
        return None
    return to_response(workspace, role)


async def update_workspace(
    workspace_id: str, changes: dict, role: str
) -> WorkspaceResponse | None:
    changes["updated_at"] = datetime.now(timezone.utc())
    workspace = await db.workspace.find_one_and_update(
        {"_id": ObjectId(workspace_id)},
        {"$set": changes},
        return_document=True,
    )
    if not workspace:
        return None
    return to_response(workspace, role)


async def delete_workspace(workspace_id: str):
    oid = ObjectId(workspace_id)
    await db.workspace.delete_one({"_id": oid})
    await db.workspace_member.delete_many({"workspace_id": oid})
