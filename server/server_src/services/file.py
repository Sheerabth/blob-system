from typing import Optional
from sqlalchemy.orm import Session, joinedload

from server_src.db.models import FileModel, UserFileModel, Permissions


def create_user_file(db: Session, user_id: str, file_name: str):
    db_file = FileModel(file_name=file_name)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    user_file = UserFileModel(user_id=user_id, file_id=db_file.id, access_type=Permissions.owner)
    db.add(user_file)
    db.commit()
    db.refresh(user_file)
    return db_file


def edit_user_file(db: Session, file_id: str, file_size: Optional[float] = None, file_name: Optional[str] = None, file_path: Optional[str] = None):
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if file_size:
        file.file_size = file_size
    if file_name:
        file.file_name = file_name
    if file_path:
        file.file_path = file_path

    db.commit()
    db.refresh(file)

    return file


def get_file_info(db: Session, file_id: str):
    return db.query(FileModel).filter(FileModel.id == file_id).first()


def get_user_files(db: Session, user_id: str):
    return db.query(UserFileModel).filter(UserFileModel.user_id == user_id).all()


def get_user_file(db: Session, user_id: str, file_id: str):
    return db.query(UserFileModel).filter(UserFileModel.user_id == user_id, UserFileModel.file_id == file_id).first()


def change_file_access(db: Session, user_id: str, file_id: str, access_type: Permissions):
    user_file = db.query(UserFileModel).filter(UserFileModel.user_id == user_id, UserFileModel.file_id == file_id).first()
    user_file.access_type = access_type

    db.commit()
    db.refresh(user_file)

    return user_file


def add_file_access(db: Session, user_id: str, file_id: str, access_type: Permissions):
    user_file = UserFileModel(user_id=user_id, file_id=file_id, access_type=access_type)
    db.add(user_file)
    db.commit()
    db.refresh(user_file)
    return user_file


def remove_file_access(db: Session, user_id: str, file_id: str):
    user_file = db.query(UserFileModel).filter(UserFileModel.user_id == user_id, UserFileModel.file_id == file_id).first()
    db.delete(user_file)
    db.commit()
    return user_file


def delete_user_file(db: Session, file_id: str):
    user_files = db.query(UserFileModel).filter(UserFileModel.file_id == file_id).all()
    for file in user_files:
        db.delete(file)
    db.commit()

    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    db.delete(file)
    db.commit()
    return file
