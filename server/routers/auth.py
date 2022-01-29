from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status, Response, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from redis import Redis

from server.middleware.auth import verify_refresh_token, verify_access_token
from server.schemas.user import UserSchema, UserCreateSchema
from server.db.database import get_db
from server.services.token import set_refresh_token, remove_refresh_token
from server.services.user import create_user, get_user_by_username, logout_all_users
from server.middleware import jwt
from server.cache.cache_client import get_connection

router = APIRouter(default_response_class=JSONResponse)


@router.post("/login")
def login(response: Response, form_data: UserCreateSchema, db: Session = Depends(get_db), key_store: Redis = Depends(get_connection)):
    user = get_user_by_username(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    access_token = jwt.create_access_token(data={"username": user.username, "user_id": user.id})
    refresh_token = jwt.create_refresh_token(data={"username": user.username, "user_id": user.id})

    set_refresh_token(key_store, user.id, refresh_token)

    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)

    return {"user_id": user.id}


@router.post("/register")
def register(response: Response, form_data: UserCreateSchema, db: Session = Depends(get_db), key_store: Redis = Depends(get_connection)):
    user = get_user_by_username(db, form_data.username, form_data.password)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    user = create_user(db, form_data)
    access_token = jwt.create_access_token(data={"username": user.username, "user_id": user.id})
    refresh_token = jwt.create_refresh_token(data={"username": user.username, "user_id": user.id})

    set_refresh_token(key_store, user.id, refresh_token)
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="refresh_token", value=refresh_token)
    return {"user_id": user.id}


@router.get("/refresh")
def refresh(response: Response, user: UserSchema = Depends(verify_refresh_token)):
    access_token = jwt.create_access_token(data={"username": user.username, "user_id": user.id})

    response.set_cookie(key="access_token", value=access_token)
    return {"user_id": user.id}


@router.get("/logout")
def logout(refresh_token: Optional[str] = Cookie(None), user: UserSchema = Depends(verify_refresh_token), key_store: Redis = Depends(get_connection)):
    remove_refresh_token(key_store, refresh_token)


@router.get("/logout_all")
def logout_all(user: UserSchema = Depends(verify_refresh_token), db: Session = Depends(get_db)):
    return logout_all_users(db, user.id)
