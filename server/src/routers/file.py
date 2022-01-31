import gzip
import logging
from datetime import datetime
from os import path, remove
import shutil
from typing import List
from urllib import parse

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import StreamingResponse

from src.db.database import get_db
from src.middleware.auth import verify_access_token
from src.schemas.file import FileSchema, FileAccessSchema
from src.schemas.user import UserSchema
from src.schemas.userfile import UserFileInfoSchema, UserFileSchema
from src.services.file import (
    create_user_file,
    edit_user_file,
    get_user_file,
    change_file_access,
    add_file_access,
    remove_file_access,
    delete_user_file,
    get_user_files,
    get_file_info,
)
from src.config import FILE_BASE_PATH
from src.db.models import Permissions
from src.services.user import get_user
from src.exceptions.api import NotFoundException, UnauthorizedException, ForbiddenException

router = APIRouter(default_response_class=JSONResponse, dependencies=[Depends(get_db)])
logger = logging.getLogger()


@router.post("/", response_model=FileSchema)
def upload_file(input_file: UploadFile, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    file = create_user_file(db, user.id, input_file.filename)

    shutil.copyfileobj(input_file.file, gzip.open(FILE_BASE_PATH + file.id, "wb"))

    file = edit_user_file(
        db, file.id, file_size=path.getsize(FILE_BASE_PATH + file.id), file_path=FILE_BASE_PATH + file.id
    )
    logger.info("New file uploaded")
    return file


@router.post("/stream", response_model=FileSchema)
async def stream_upload_file(
    file_name: str, request: Request, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)
):

    file = create_user_file(db, user.id, file_name)

    compressed_file = gzip.open(FILE_BASE_PATH + file.id, "wb")

    async for chunk in request.stream():
        compressed_file.write(chunk)

    file = edit_user_file(
        db, file.id, file_size=path.getsize(FILE_BASE_PATH + file.id), file_path=FILE_BASE_PATH + file.id
    )
    logger.info("New file uploaded(streamed)")
    return file


@router.get("/", response_model=List[UserFileInfoSchema])
def get_files(user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    return get_user_files(db, user.id)


@router.get("/download/{file_id}", response_class=FileResponse)
def download_file(file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested invalid file")
        raise NotFoundException(detail="Requested file not found")

    encoded = parse.quote(user_file.file.file_name)
    if encoded == user_file.file.file_name:
        content_disposition = {"Content-Disposition": f'attachment; filename="{encoded}"'}
    else:
        content_disposition = {"Content-Disposition": f"attachment; filename*=utf-8''{encoded}"}

    def iter_file():
        file_like = gzip.open(FILE_BASE_PATH + file_id, mode="rb")
        while True:
            chunk = file_like.read(size=4096)
            if not chunk:
                break
            yield chunk

    try:
        return StreamingResponse(iter_file(), headers=content_disposition)
    except IOError:
        logger.error("File exists in database but missing in storage")
        raise NotFoundException(detail="File not found")


@router.get("/access/{file_id}", response_model=FileAccessSchema)
def file_access_info(file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested invalid file")
        raise NotFoundException(detail="Requested file not found")

    file = get_file_info(db, file_id)
    return file


@router.patch("/{file_id}", response_model=FileSchema)
def rename_file(
    file_id: str, file_name: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)
):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested invalid file")
        raise NotFoundException(detail="Requested file not found")

    if user_file.access_type == Permissions.read:
        logger.error("User requested to rename file with read permission")
        raise UnauthorizedException(detail="No rename permissions")

    return edit_user_file(db, user_file.file_id, file_name=file_name, updated_at=datetime.utcnow().isoformat())


@router.put("/{file_id}", response_model=FileSchema)
def edit_file(
    file_id: str, input_file: UploadFile, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)
):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested invalid file")
        raise NotFoundException(detail="Requested file not found")

    if user_file.access_type == Permissions.read:
        logger.error("User requested to edit file without edit permission")
        raise UnauthorizedException(detail="No edit permissions")

    shutil.copyfileobj(input_file.file, gzip.open(FILE_BASE_PATH + file_id, "wb"))

    file = edit_user_file(
        db,
        file_id,
        file_name=input_file.filename,
        file_size=path.getsize(FILE_BASE_PATH + file_id),
        file_path=FILE_BASE_PATH + file_id,
        updated_at=datetime.utcnow().isoformat(),
    )
    logger.info("Existing file edited")
    return file


@router.put("/stream/{file_id}", response_model=FileSchema)
async def stream_edit_file(
    file_id: str,
    file_name: str,
    request: Request,
    user: UserSchema = Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested invalid file")
        raise NotFoundException(detail="Requested file not found")

    if user_file.access_type == Permissions.read:
        logger.error("User requested to edit file without edit permission")
        raise UnauthorizedException(detail="No edit permissions")

    compressed_file = gzip.open(FILE_BASE_PATH + file_id, "wb")

    async for chunk in request.stream():
        compressed_file.write(chunk)

    file = edit_user_file(
        db,
        file_id,
        file_name=file_name,
        file_size=path.getsize(FILE_BASE_PATH + file_id),
        file_path=FILE_BASE_PATH + file_id,
        updated_at=datetime.utcnow().isoformat(),
    )
    logger.info("Existing file edited(streamed)")
    return file


@router.get("/", response_model=List[UserFileInfoSchema])
def get_files(user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    return get_user_files(db, user.id)


@router.patch("/access/{file_id}", response_model=UserFileSchema)
def change_access(
    user_id: str,
    file_id: str,
    access_type: Permissions,
    user: UserSchema = Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    if user_id == user.id:
        logger.error("User trying to change their own permission")
        raise ForbiddenException(detail="Trying to change your own permission")

    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested file not found")
        raise NotFoundException(detail="File not found")

    if user_file.access_type != Permissions.owner:
        logger.error("User requested to change file access without owner permission")
        raise UnauthorizedException(detail="Only owners can change file permission")

    access_user = get_user(db, user_id)
    if access_user is None:
        logger.error("User requested access user not found")
        raise NotFoundException(detail="Access user not found")

    if access_type == Permissions.owner:
        change_file_access(db, user.id, file_id, Permissions.edit)

    access_file = get_user_file(db, user_id, file_id)

    if access_file is None:
        return add_file_access(db, user_id, file_id, access_type)

    return change_file_access(db, user_id, file_id, access_type)


@router.delete("/access/{file_id}", response_model=UserFileSchema)
def remove_access(
    user_id: str, file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)
):
    if user_id == user.id:
        logger.error("User trying to remove their own permission")
        raise ForbiddenException(detail="Trying to remove your own permission")

    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested file not found")
        raise NotFoundException(detail="File not found")

    if user_file.access_type != Permissions.owner:
        logger.error("User requested to remove file access without owner permission")
        raise UnauthorizedException(detail="Owner permission required")

    access_user = get_user(db, user_id)
    if access_user is None:
        logger.error("User requested access user not found")
        raise NotFoundException(detail="User not found")

    access_file = get_user_file(db, user_id, file_id)

    if not access_file:
        logger.error("User requested access user already doesn't have permission")
        raise NotFoundException(detail="Requested user already doesn't have permission")
    return remove_file_access(db, user_id, file_id)


@router.delete("/{file_id}", response_model=FileSchema)
def delete_file(file_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user_file = get_user_file(db, user.id, file_id)
    if user_file is None:
        logger.error("User requested invalid file")
        raise NotFoundException(detail="File not found")

    user_file = get_user_file(db, user.id, file_id)
    if user_file.access_type != Permissions.owner:
        logger.error("User requested to delete file access without owner permission")
        raise UnauthorizedException(detail="Owner permission required")

    deleted_file = delete_user_file(db, user_file.file_id)
    try:
        remove(deleted_file.file_path)
    except IOError:
        logger.error("File exists in database but missing in storage")
        raise NotFoundException(detail="File not found")

    logger.info("User deleted a file from storage")
    return deleted_file
