from redis import Redis, ConnectionPool
from server_src.config import REDIS_HOST, REDIS_PORT, REDIS_DB

pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def get_connection() -> Redis:
    return Redis(connection_pool=pool)
