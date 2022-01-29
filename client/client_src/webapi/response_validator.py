from requests import Response
from client_src.exceptions.api import APIException, BadRequestAPIException, TokenExpiredException, UnauthorizedAPIException, ForbiddenAPIException, NotFoundAPIException


def response_validator(response: Response):
    if response.status_code == 200:
        return response

    elif response.status_code == 400:
        raise BadRequestAPIException(response)

    elif response.status_code == 401:
        if "detail" in response.json() and response.json()["detail"] == "token expired":
            raise TokenExpiredException(response)
        raise UnauthorizedAPIException(response)

    elif response.status_code == 403:
        raise ForbiddenAPIException(response)

    elif NotFoundAPIException == 404:
        raise NotFoundAPIException(response)

    else:
        raise APIException(response)
