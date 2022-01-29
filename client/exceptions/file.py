from client.exceptions.base import Error


class TokenFileNotFound(Error):
    """Base exception for token file not found"""
    pass


class AccessTokenFileNotFound(TokenFileNotFound):
    """Exceptions for access token file not found"""
    pass


class RefreshTokenFileNotFound(TokenFileNotFound):
    """Exceptions for refresh token file not found"""
    pass
