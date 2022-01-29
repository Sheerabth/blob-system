import os
from typing import List

from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from server_src.db.database import get_db
from server_src.middleware.auth import verify_access_token
from server_src.schemas.file import FileSchema, FileAccessSchema
from server_src.schemas.user import UserSchema
from server_src.schemas.userfile import UserFileInfoSchema, UserFileSchema
from server_src.services.file import create_user_file, edit_user_file, get_user_file, change_file_access, add_file_access, \
    remove_file_access, delete_user_file, get_user_files, get_file_info
from server_src.config import FILE_BASE_PATH
from server_src.db.models import Permissions
from server_src.services.user import get_user
from server_src.exceptions.api import NotFoundException, UnauthorizedException, ForbiddenException

router = APIRouter(default_response_class=JSONResponse, dependencies=[Depends(get_db)])


@router.post("/", response_model=FileSchema)
def create_upload_file(input_file: UploadFile, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    file = create_user_file(db, user.id, input_file.filename)

    with input_file.file as source_file, open(FILE_BASE_PATH + file.id, "wb") as target_file:
        for line in source_file:
            target_file.write(line)

    file = edit_user_file(db, file.id, file_size=os.stat(FILE_BASE_PATH + file.id).st_size, file_path=FILE_BASE_PATH + file.id)
    return file


@router.get("/", response_model=List[UserFileInfoSchema])
def get_files(user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    return get_user_files(db, user.id)


@router.get("/download/{file_id}", response_class=FileResponse)
def download_file(file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        raise NotFoundException(detail="Requested file not found")

    return FileResponse(FILE_BASE_PATH + file_id, filename=user_file.file.file_name)


@router.get("/access/{file_id}", response_model=FileAccessSchema)
def file_access_info(file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        raise NotFoundException(detail="Requested file not found")

    file = get_file_info(db, file_id)
    return file


@router.patch("/{file_id}", response_model=FileSchema)
def rename_file(file_id: str, file_name: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        raise NotFoundException(detail="Requested file not found")

    if user_file.access_type == Permissions.owner or user_file.access_type == Permissions.edit:
        return edit_user_file(db, user_file.file_id, file_name=file_name)

    raise UnauthorizedException(detail="No rename permissions")


@router.patch("/access/{file_id}", response_model=UserFileSchema)
def change_access(user_id: str, file_id: str, access_type: Permissions, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    if user_id == user.id:
        raise ForbiddenException(detail="Trying to change your own permission")

    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        raise NotFoundException(detail="File not found")

    if user_file.access_type != Permissions.owner:
        raise UnauthorizedException(detail="Only owners can change file permission")

    access_user = get_user(db, user_id)
    if access_user is None:
        raise NotFoundException(detail="User not found")

    if access_type == Permissions.owner:
        change_file_access(db, user.id, file_id, Permissions.edit)

    access_file = get_user_file(db, user_id, file_id)

    if access_file is None:
        return add_file_access(db, user_id, file_id, access_type)

    return change_file_access(db, user_id, file_id, access_type)


@router.delete("/access/{file_id}", response_model=UserFileSchema)
def remove_access(user_id: str, file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    if user_id == user.id:
        raise ForbiddenException(detail="Trying to change your own permission")

    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        raise NotFoundException(detail="File not found")

    if user_file.access_type != Permissions.owner:
        raise UnauthorizedException(detail="Owner permission required")

    access_user = get_user(db, user_id)
    if access_user is None:
        raise NotFoundException(detail="User not found")

    access_file = get_user_file(db, user_id, file_id)

    if access_file:
        return remove_file_access(db, user_id, file_id)

    return access_file


@router.delete("/{file_id}", response_model=FileSchema)
def delete_file(file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        raise NotFoundException(detail="File not found")

    user_file = get_user_file(db, user.id, file_id)
    if user_file.access_type != Permissions.owner:
        raise UnauthorizedException(detail="Owner permission required")

    deleted_file = delete_user_file(db, user_file.file_id)
    os.remove(deleted_file.file_path)
    return deleted_file
