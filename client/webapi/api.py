from urllib.parse import unquote
from typing import Optional, Dict, BinaryIO
import re

import requests

from client.config import URL
from client.exceptions.api import APIException
from client.webapi.response_validator import response_validator


RE_FILENAME = re.compile(r'filename="(.+)"')
RE_ENCODED_FILENAME = re.compile(r"filename\*=utf-8''(.+)")


def get_request(path: str, query_params: Optional[Dict[str, str]] = None, cookies: Optional[Dict[str, str]] = None, stream: Optional[bool] = False):
    response_body = requests.get(URL + path, cookies=cookies, params=query_params, stream=stream)
    return response_validator(response_body)


def post_request(path: str, body: Optional[Dict[str, str]] = None, file: Optional[Dict[str, BinaryIO]] = None, cookies: Optional[Dict[str, str]] = None):
    response_body = requests.post(URL + path, cookies=cookies, json=body, files=file)
    return response_validator(response_body)


def patch_request(path: str, body: Optional[Dict[str, str]] = None, query_params: Optional[Dict[str, str]] = None, cookies: Optional[Dict[str, str]] = None):
    response_body = requests.patch(URL + path, cookies=cookies, json=body, params=query_params)
    return response_validator(response_body)


def register_user(username: str, password: str):
    user_data = {
        "username": username,
        "password": password
    }
    response = post_request("/auth/register", body=user_data)
    return {'user_id': response.json()['user_id'], 'tokens': response.cookies}


def login_user(username: str, password: str):
    user_data = {
        "username": username,
        "password": password
    }
    response = post_request("/auth/login", body=user_data)
    return {'user_id': response.json()['user_id'], 'tokens': response.cookies}


def refresh_user(refresh_token: str):
    response = get_request("/auth/refresh", cookies={'refresh_token': refresh_token})
    return {'user_id': response.json()['user_id'], 'tokens': response.cookies}


def logout_user(refresh_token: str):
    response = get_request("/auth/logout", cookies={'refresh_token': refresh_token})
    return response.json()


def logout_all_users(refresh_token: str):
    response = get_request("/auth/logout_all", cookies={'refresh_token': refresh_token})
    return response.json()


def get_user_files(access_token: str):
    response = get_request("/file/", cookies={'access_token': access_token})
    return response.json()


def upload_user_file(access_token: str, input_file: BinaryIO):
    file = {'input_file': input_file}
    response = post_request("/file/", file=file, cookies={'access_token': access_token})
    return response.json()


def download_user_file(access_token: str, file_id: str) -> dict:
    response = get_request(f"/file/download/{file_id}", cookies={'access_token': access_token}, stream=True)
    content_disposition = response.headers.get('content-disposition')
    matches = re.findall(RE_ENCODED_FILENAME, content_disposition)
    if len(matches) == 0:
        matches = re.findall(RE_FILENAME, content_disposition)
        if len(matches) == 0:
            raise APIException
    file_name = unquote(matches[0])
    return {"file_name": file_name, "content": response.iter_content(chunk_size=1024)}


def file_access_info(access_token: str, file_id: str):
    response = get_request(f"/file/access/{file_id}", cookies={'access_token': access_token})
    return response.json()


def rename_user_file(access_token: str, file_id: str, new_file_name: str):
    response = patch_request(f"/file/{file_id}", query_params={'file_name': new_file_name}, cookies={'access_token': access_token})
    return response.json()
