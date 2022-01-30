from typing import Optional
from datetime import datetime

from fastapi import Depends
from fastapi.params import Cookie
from jose import jwt, JWTError
from redis import Redis
from sqlalchemy.orm import Session

from src.cache.cache_client import get_connection
from src.config import REFRESH_TOKEN_SECRET, ALGORITHM, ACCESS_TOKEN_SECRET
from src.db.database import get_db
from src.exceptions.api import InvalidCredentialsException, TokenExpiredException
from src.schemas.token import PayloadSchema
from src.schemas.user import UserSchema
from src.services.token import check_refresh_token
from src.services.user import get_user


def verify_refresh_token(
    db: Session = Depends(get_db),
    key_store: Redis = Depends(get_connection),
    refresh_token: Optional[str] = Cookie(None),
) -> UserSchema:
    if refresh_token is None or not check_refresh_token(key_store, refresh_token):
        raise InvalidCredentialsException

    try:
        payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        user_name: str = payload.get("username")
        user_id: str = payload.get("user_id")
        created_at: str = payload.get("created_at")
        if user_id is None:
            raise InvalidCredentialsException
        token_data = PayloadSchema(username=user_name, user_id=user_id, created_at=created_at)
    except JWTError:
        raise InvalidCredentialsException
    user = get_user(db, user_id=token_data.user_id)
    if user is None or datetime.fromisoformat(created_at) < datetime.fromisoformat(user.latest_time):
        raise InvalidCredentialsException
    return user


def verify_access_token(db: Session = Depends(get_db), access_token: Optional[str] = Cookie(None)) -> UserSchema:
    if access_token is None:
        raise TokenExpiredException

    try:
        payload = jwt.decode(access_token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        user_name: str = payload.get("username")
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise InvalidCredentialsException
        token_data = PayloadSchema(username=user_name, user_id=user_id)
    except JWTError:
        raise TokenExpiredException
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise InvalidCredentialsException
    return user
