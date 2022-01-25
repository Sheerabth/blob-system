from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()


def create_user_file(
    db: Session,
    file: schemas.FileCreate,
    user_id: int,
    file_size: int,
    file_path: str,
):
    db_file = models.File(
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
