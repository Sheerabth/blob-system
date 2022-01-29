from os import environ
from dotenv import load_dotenv

load_dotenv()

# Redis Config
REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = int(environ.get("REDIS_PORT"))
REDIS_DB = int(environ.get("REDIS_DB"))
REDIS_USER = environ.get("REDIS_USER")
REDIS_PASSWORD = environ.get("REDIS_PASSWORD")

# Database Config
DATABASE_HOST = environ.get("DATABASE_HOST")
DATABASE_PORT = int(environ.get("DATABASE_PORT"))
DATABASE_NAME = environ.get("DATABASE_NAME")
DATABASE_USER = environ.get("DATABASE_USER")
DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")

# Secret Tokens
ACCESS_TOKEN_SECRET = environ.get("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = environ.get("REFRESH_TOKEN_SECRET")
CRYPTR_SECRET = environ.get("CRYPTR_SECRET")
BCRYPT_SECRET = environ.get("BCRYPT_SECRET")

# Token
ALGORITHM = environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))

# File Storage
FILE_BASE_PATH = environ.get("FILE_BASE_PATH")
