from os.path import exists
from os import listdir, remove, rename
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from db.models import FileModel
from schemas.file import FileSchema, FileCreateSchema
from db.database import SessionLocal, engine
from db import utils

router = APIRouter(default_response_class=JSONResponse)
path = "./files/"


@router.post("/uploadfile/", tags=["files"])
def create_upload_file(input_file: UploadFile):
    with input_file.file as source_file, open(
        path + input_file.filename, "wb"
    ) as target_file:
        for line in source_file:
            target_file.write(line)

    return {"filename": input_file.filename}


@router.get("/files/", tags=["files"])
def get_files():
    files_list = listdir(path)

    return {"files": files_list}


@router.get("/files/{file_name}", response_class=FileResponse, tags=["files"])
def download_file(file_name: str):
    if not exists(path + file_name):
        raise HTTPException(status_code=404, detail="File not found")

    return path + file_name


@router.patch("/files/{file_name}", tags=["files"])
def rename_file(target_file_name: str, file_name: str):
    if not exists(path + file_name):
        raise HTTPException(status_code=404, detail="File not found")

    rename(path + file_name, path + target_file_name)


@router.delete("/files/{file_name}", tags=["files"])
def delete_file(file_name: str):
    if not exists(path + file_name):
        raise HTTPException(status_code=404, detail="File not found")

    remove(path + file_name)
