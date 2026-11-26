from typing import Literal
from pydantic import BaseModel
from datetime import datetime


class MemberResponse(BaseModel):
    user_id: str
    name: str
    email: str
    role: str
    joined_at: datetime


#  to change the role of a person or member
class RoleUpdate(BaseModel):
    role: Literal["admin", "member"]


class TransferOwnership(BaseModel):
    new_owner_id: str
