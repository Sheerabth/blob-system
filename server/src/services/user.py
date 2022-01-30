from datetime import datetime

from sqlalchemy.orm import Session

from src.db.models import UserModel
from src.schemas.user import UserCreateSchema


def get_user(db: Session, user_id: str):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_username(db: Session, username: str, password: str):
    return db.query(UserModel).filter(UserModel.username == username, password == password).first()


def create_user(db: Session, user: UserCreateSchema):
    fake_hashed_password = user.password
    db_user = UserModel(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def logout_all_users(db: Session, user_id: str):
    user = get_user(db, user_id)
    user.latest_time = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(user)

    return user
