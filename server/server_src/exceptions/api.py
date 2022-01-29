from typing import Optional

from fastapi import HTTPException, status


class APIException(HTTPException):
    """Exception for http exceptions"""

    def __init__(self, *args, **kwargs):
        super(APIException, self).__init__(*args, **kwargs)


class InvalidCredentialsException(APIException):
    """Exception for refresh token expiration"""

    def __init__(self, detail: Optional[str] = "Invalid Credentials"):
        super(InvalidCredentialsException, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'error_code': 4000,
                'error_info': detail
            },
        )


class TokenExpiredException(APIException):
    """Exception for access token expiration"""

    def __init__(self, detail: Optional[str] = "Token expired"):
        super(TokenExpiredException).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'error_code': 4001,
                'error_info': detail
            },
        )


class UnauthorizedException(APIException):
    """Exception for unauthorized action"""

    def __init__(self, detail: Optional[str] = "Access Denied"):
        super(UnauthorizedException, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'error_code': 4002,
                'error_info': detail
            },
        )


class InvalidRequestException(APIException):
    """Exception for invalid request"""

    def __init__(self, detail: Optional[str] = "Invalid Request"):
        super(InvalidRequestException, self).__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'error_code': 4003,
                'error_info': detail
            },
        )


class NotFoundException(APIException):
    """Exception for file not found"""

    def __init__(self, detail: Optional[str] = "Not Found"):
        super(NotFoundException, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'error_code': 4004,
                'error_info': detail
            },
        )


class ForbiddenException(APIException):
    """Exception for forbidden"""

    def __init__(self, detail: Optional[str] = "Request forbidden"):
        super(ForbiddenException, self).__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'error_code': 4005,
                'error_info': detail
            }
        )

