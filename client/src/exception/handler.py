import typer
from requests.exceptions import RequestException

from src.exception import TokenFileNotFound, IndexException, PermissionException, FileNotFoundException
from src.exception import APIException
from functools import wraps

from src.utils.typer_utils import print_error


def exception_handler(api_function):
    @wraps(api_function)
    def inner(*args, **kwargs):

        try:
            api_function(*args, **kwargs)
        except (IndexException, PermissionException, FileNotFoundException) as e:
            print_error(e.message)

        except TokenFileNotFound:
            print_error("Token file not found")

        except APIException as e:
            print_error(e.detail["error_info"])

        except RequestException:
            print_error("Cant connect to host")

        raise typer.Exit(code=1)

    return inner
