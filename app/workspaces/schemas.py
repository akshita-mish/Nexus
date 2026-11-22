from pydantic import BaseModel, Field
from datetime import datetime


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class WorkspaceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str
    owner_id: str
    my_role: str
    create_at: datetime
    updated_at: datetime
