from pydantic import BaseModel
from schemas import File


class UserBase(BaseModel):
    username: str


class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool
    files: list[File] = []

    class Config:
        orm_mode = True
