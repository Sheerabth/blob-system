from requests import Response
from src.exception import APIException


def response_validator(response: Response) -> Response:
    if response.status_code == 200:
        return response

    else:
        if "detail" in response.json():
            raise APIException(response.json()["detail"])
        raise APIException
