from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schemas.user import UserSchema, UserCreateSchema
from server.db.database import SessionLocal
from dao.user import create_user, get_user_by_username

router = APIRouter(default_response_class=JSONResponse)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Already registered")

    return create_user(db=db, user=user)
