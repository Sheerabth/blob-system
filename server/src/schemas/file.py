from typing import Optional, List
from pydantic import BaseModel

from src.schemas.userfile import UserFileBaseSchema


class FileBase(BaseModel):
    file_name: str


class FileCreateSchema(FileBase):
    pass


class FileSchema(FileCreateSchema):
    id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class FileAccessSchema(FileSchema):
    users: Optional[List[UserFileBaseSchema]]
