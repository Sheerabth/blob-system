import json
from pathlib import Path
from os import path

from client.config import TOKEN_FILE_PATH
from client.exceptions.file import TokenFileNotFound
from client.exceptions.api import UnauthorizedAPIException, TokenExpiredException
from client.extras.token import TokenType


def get_token(token_type: TokenType):
    if TOKEN_FILE_PATH:
        token_file_path = TOKEN_FILE_PATH
    else:
        token_file_path = path.join(Path.home(), "tokens.json")

    try:
        with open(token_file_path, 'r') as token_file:
            tokens = json.load(token_file)

        if type(tokens) != dict or token_type not in tokens:
            raise TokenFileNotFound

        return tokens[token_type]

    except json.decoder.JSONDecodeError:
        raise TokenFileNotFound

    except IOError:
        raise TokenFileNotFound


def set_token(token_type: TokenType, cookies):
    if TOKEN_FILE_PATH:
        token_file_path = TOKEN_FILE_PATH
    else:
        token_file_path = path.join(Path.home(), "tokens.json")

    if token_type not in cookies:
        if token_type == TokenType.access_token:
            raise TokenExpiredException
        raise UnauthorizedAPIException

    try:
        with open(token_file_path, 'r+') as token_file:
            tokens = json.load(token_file)

    except json.decoder.JSONDecodeError:
        tokens = dict()

    except IOError:
        raise TokenFileNotFound

    with open(token_file_path, 'w+') as token_file:
        tokens[token_type] = cookies[token_type]
        json.dump(tokens, token_file)


def set_tokens(cookies):
    set_token(TokenType.access_token, cookies)
    set_token(TokenType.refresh_token, cookies)



