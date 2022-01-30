import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.exceptions.api import NotFoundException
from src.middleware.auth import verify_access_token
from src.schemas.user import UserSchema
from src.services.user import get_user

router = APIRouter(default_response_class=JSONResponse)
logger = logging.getLogger(__name__)


@router.get("/{user_id}", response_model=UserSchema)
def get_user_info(user_id: str, user: UserSchema = Depends(verify_access_token), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        logger.error("User requested an invalid user information")
        raise NotFoundException(detail="User not found exception")
    return user
