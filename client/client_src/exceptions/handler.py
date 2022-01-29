import typer
from requests.exceptions import RequestException

from client_src.exceptions import TokenFileNotFound
from client_src.exceptions import APIException
from functools import wraps


def exception_handler(api_function):
    @wraps(api_function)
    def inner(*args, **kwargs):

        try:
            api_function(*args, **kwargs)

        except TokenFileNotFound:
            typer.echo("Token file not found")

        except APIException as e:

            typer.echo(f"Error Code: {e.detail['error_code']}, Error Info: {e.detail['error_info']}")

        except RequestException:

            typer.echo("Cant connect to host")

        raise typer.Exit(code=1)

    return inner
