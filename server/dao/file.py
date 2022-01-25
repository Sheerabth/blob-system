from sqlalchemy.orm import Session

from db.models import FileModel
from schemas.user import FileSchema, FileCreateSchema


def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FileModel).offset(skip).limit(limit).all()


def create_user_file(
    db: Session,
    file: FileCreateSchema,
    user_id: int,
    file_size: int,
    file_path: str,
):
    db_file = FileModel(
        **file.dict(),
        access_id=user_id,
        file_size=file_size,
        file_path=file_path,
        is_owner=True
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
