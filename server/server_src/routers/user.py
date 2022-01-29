from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from server_src.db.database import get_db
from server_src.middleware.auth import verify_access_token
from server_src.schemas.user import UserSchema
from server_src.services.user import get_user

router = APIRouter(default_response_class=JSONResponse)


@router.get("/{user_id}", response_model=UserSchema)
def get_user_info(user_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    return get_user(db, user_id)
