from pydantic import BaseModel


class FileBase(BaseModel):
    filename: str


class FileCreateSchema(FileBase):
    pass


class FileSchema(FileBase):
    id: int
    file_path: str
    file_size: float
    access_id: int
    is_owner: bool

    class Config:
        orm_mode = True
