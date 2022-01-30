from pydantic import BaseModel
from typing import Optional


class PayloadSchema(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None


class RefreshTokenPayloadSchema(PayloadSchema):
    created_at: Optional[str] = None
