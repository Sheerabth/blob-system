from typing import Optional


class Error(Exception):
    """Base class for other exceptions"""
    pass


class TokenFileNotFound(Error):
    """Base exception for token file not found"""
    pass


class APIException(Error):
    """Base exception for api exceptions"""

    def __init__(self, detail: Optional[dict] = None):
        self.detail = detail
