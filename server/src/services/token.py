from redis import Redis
from src.config import REFRESH_TOKEN_EXPIRE_MINUTES


def set_refresh_token(key_store: Redis, user_id: str, refresh_token: str) -> None:
    key_store.set(refresh_token, user_id)
    key_store.expire(refresh_token, REFRESH_TOKEN_EXPIRE_MINUTES * 60)


def remove_refresh_token(key_store: Redis, refresh_token: str) -> None:
    key_store.delete(refresh_token)


def check_refresh_token(key_store: Redis, refresh_token: str) -> bool:
    if key_store.exists(refresh_token) == 0:
        return False
    return True
