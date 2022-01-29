from redis import Redis
from server.config import REFRESH_TOKEN_EXPIRE_MINUTES


def set_refresh_token(key_store: Redis, user_id: str, refresh_token: str):
    key_store.set(refresh_token, user_id)
    return key_store.expire(refresh_token, REFRESH_TOKEN_EXPIRE_MINUTES*60)


def remove_refresh_token(key_store: Redis, refresh_token: str):
    return key_store.delete(refresh_token)


def check_refresh_token(key_store: Redis, refresh_token: str):
    if key_store.exists(refresh_token) == 0:
        return False
    return True
