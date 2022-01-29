from typing import Optional
from pydantic import BaseModel

from server.db.models import Permissions


class UserFileBaseSchema(BaseModel):
    user_id: str
    access_type: Permissions

    class Config:
        orm_mode = True


class UserFileSchema(UserFileBaseSchema):
    file_id: str


class UserFileInfoSchema(UserFileSchema):
    file: Optional[object]


class UserInfoFileSchema(UserFileSchema):
    user: Optional[object]

