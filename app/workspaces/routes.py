from fastapi import APIRouter, Depends, HTTPException
from app.users.dependency import get_current_user
from app.workspaces.constants import OWNER, ADMIN, MEMBER
from app.workspaces.schemas import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate
from app.workspaces import services
from app.workspaces.dependencies import require_role

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.post("", response_model=WorkspaceResponse, status_code=201)
async def create_workspace(
    data: WorkspaceCreate,
    current_user=Depends(get_current_user),
):
    return await services.create_workspace(data, current_user["id"])


@router.get("", response_model=WorkspaceResponse, status_code=200)
async def list_my_workspace(current_user=Depends(get_current_user)):
    return await services.list_my_workspace(current_user["id"])


# need to write the role dependency here
@router.get("/{workspace_id}", response_model=WorkspaceResponse, status_code=200)
async def get_workspace(workspace_id: str, member=Depends(require_role(OWNER, ADMIN))):
    workspace = await services.get_workspace(workspace_id, member["role"])
    if workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace


@router.delete("/{workspace_id}", status_code=200)
async def delete_workspace(workspace_id: str, member=Depends(require_role(OWNER))):
    await services.delete_workspace(workspace_id)
    return {"message": "Workspace deleted"}


@router.patch("/{workspace_id}", response_model=WorkspaceUpdate, status_code=200)
async def update_workspace(
    workspace_id: str,
    data: WorkspaceUpdate,
    member=Depends(require_role(OWNER, ADMIN)),
):
    # model_dump() :: it is used to conevrt a pydantic model into dict because db mai it is dict
    # exclude_unset=True ka matlab: "jo fields client ne set nahi ki (bheji nahi),
    #  unhe dict se bahar rakho." Ab dict mein sirf wahi hai jo client ne bheja.
    changes = data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Nothing to update")

    workspace = await services.update_workspace(workspace_id, changes, member["role"])
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace
