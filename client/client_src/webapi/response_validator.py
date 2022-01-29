from requests import Response
from client_src.exceptions import APIException


def response_validator(response: Response):
    if response.status_code == 200:
        return response

    else:
        if "detail" in response.json():
            raise APIException(response.json()["detail"])
        raise APIException
