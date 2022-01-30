from typing import Optional, List
from pydantic import BaseModel

from src.schemas.userfile import UserFileSchema


class UserBase(BaseModel):
    username: str


class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: str
    latest_time: str

    class Config:
        orm_mode = True


class UserAccessSchema(UserSchema):
    files: Optional[List[UserFileSchema]]
