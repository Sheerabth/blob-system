from typing import Optional

from client_src.exceptions.base import Error


class APIException(Error):
    """Base exception for api exceptions"""

    def __init__(self, detail: Optional[object] = None):
        self.detail = detail


class BadRequestAPIException(APIException):
    """Exception for bad request api response"""

    def __init__(self, detail: Optional[object] = None):
        super().__init__(detail)


class UnauthorizedAPIException(APIException):
    """Exception for unauthorized api response"""

    def __init__(self, detail: Optional[object] = None):
        super().__init__(detail)


class TokenExpiredException(UnauthorizedAPIException):
    """Exception for access token expiry"""

    def __init__(self, detail: Optional[object] = None):
        super().__init__(detail)


class InvalidCredentialsException(UnauthorizedAPIException):
    """Exception for access token expiry"""

    def __init__(self, detail: Optional[object] = None):
        super().__init__(detail)


class ForbiddenAPIException(APIException):
    """Exception for forbidden api response"""

    def __init__(self, detail: Optional[object] = None):
        super().__init__(detail)


class NotFoundAPIException(APIException):
    """Exception for not found api response"""

    def __init__(self, detail: Optional[object] = None):
        super().__init__(detail)


