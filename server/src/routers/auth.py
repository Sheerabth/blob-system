from typing import Optional
import logging

from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from redis import Redis
from passlib.context import CryptContext

from src.cache.cache_client import get_connection
from src.db.database import get_db
from src.exceptions.api import InvalidCredentialsException, ForbiddenException
from src.middleware.auth import verify_refresh_token
from src.middleware.jwt import create_access_token, create_refresh_token
from src.schemas.user import UserCreateSchema, UserSchema
from src.services.token import remove_refresh_token, set_refresh_token
from src.services.user import get_user_by_username, create_user, logout_all_users

router = APIRouter(default_response_class=JSONResponse)
logger = logging.getLogger(__name__)


@router.post("/login")
def login(
    response: Response,
    form_data: UserCreateSchema,
    db: Session = Depends(get_db),
    key_store: Redis = Depends(get_connection),
):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = get_user_by_username(db, form_data.username, pwd_context.hash(form_data.password))

    if not user:
        logging.error("Invalid Login")
        raise InvalidCredentialsException
    access_token = create_access_token(data={"username": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(data={"username": user.username, "user_id": user.id})

    set_refresh_token(key_store, user.id, refresh_token)

    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)

    return {"user_id": user.id}


@router.post("/register")
def register(
    response: Response,
    form_data: UserCreateSchema,
    db: Session = Depends(get_db),
    key_store: Redis = Depends(get_connection),
):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = get_user_by_username(db, form_data.username, pwd_context.hash(form_data.password))

    if user:
        logging.error("User already exists")
        raise ForbiddenException("User already exists")
    user = create_user(db, form_data)
    access_token = create_access_token(data={"username": user.username, "user_id": user.id})
    refresh_token = create_refresh_token(data={"username": user.username, "user_id": user.id})

    set_refresh_token(key_store, user.id, refresh_token)
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)
    return {"user_id": user.id}


@router.get("/refresh")
def refresh(response: Response, user: UserSchema = Depends(verify_refresh_token)):
    access_token = create_access_token(data={"username": user.username, "user_id": user.id})

    response.set_cookie(key="access_token", value=access_token)
    return {"user_id": user.id}


@router.get("/logout")
def logout(
    refresh_token: Optional[str] = Cookie(None),
    user: UserSchema = Depends(verify_refresh_token),
    key_store: Redis = Depends(get_connection),
):
    remove_refresh_token(key_store, refresh_token)



@router.get("/logout_all")
def logout_all(user: UserSchema = Depends(verify_refresh_token), db: Session = Depends(get_db)):
    return logout_all_users(db, user.id)
