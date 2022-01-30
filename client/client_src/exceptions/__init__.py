from typing import Optional


class Error(Exception):
    """Base class for other exceptions"""

    pass


class TokenFileNotFound(Error):
    """Base exception for token file not found"""

    pass


class APIException(Error):
    """Base exception for api exceptions"""

    def __init__(self, detail: Optional[dict] = "API Exception Occurred"):
        self.detail = detail


class IndexException(Error):
    """Exception for handing invalid indices"""

    def __init__(self, message: Optional[str] = "Invalid index"):
        self.message = message


class PermissionException(Error):
    """Exception for handling invalid permissions"""

    def __init__(self, message: Optional[str] = "Invalid permission"):
        self.message = message
