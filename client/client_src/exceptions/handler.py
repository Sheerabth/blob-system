import typer
from client_src.exceptions.base import Error
from client_src.exceptions.file import TokenFileNotFound, AccessTokenFileNotFound, RefreshTokenFileNotFound
from client_src.exceptions.api import APIException, BadRequestAPIException, TokenExpiredException, UnauthorizedAPIException, ForbiddenAPIException, NotFoundAPIException
from functools import wraps


def exception_handler(api_function):

    @wraps(api_function)
    def inner(*args, **kwargs):

        try:
            api_function(*args, **kwargs)

        except AccessTokenFileNotFound:
            typer.echo("Access token file not found")

        except RefreshTokenFileNotFound:
            typer.echo("Refresh token file not found")

        except TokenFileNotFound:
            typer.echo("Token file not found")

        except BadRequestAPIException:
            typer.echo("Bad request")

        except TokenExpiredException:
            typer.echo("Token expired")

        except UnauthorizedAPIException:
            typer.echo("Invalid credentials")

        except ForbiddenAPIException:
            typer.echo("Request Forbidden")

        except NotFoundAPIException:
            typer.echo("Not found")

        except APIException:
            typer.echo("API exception")

        except Error:
            typer.echo("Base exception")

        raise typer.Exit(code=1)

    return inner

