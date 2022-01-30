from enum import Enum


class TokenType(str, Enum):
    access_token = "access_token"
    refresh_token = "refresh_token"
