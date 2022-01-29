from fastapi import HTTPException, status


class APIException(HTTPException):
    """Exception for http exceptions"""

    def __init__(self, *args, **kwargs):
        super(APIException, self).__init__(*args, **kwargs)


class InvalidCredentialsException(APIException):
    """Exception for refresh token expiration"""

    def __init__(self):
        super(InvalidCredentialsException, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="login required",
        )


class TokenExpiredException(APIException):
    """Exception for access token expiration"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expired",
        )
