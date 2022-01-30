import json
from pathlib import Path
from os import path

from client_src.config import TOKEN_FILE_PATH
from client_src.exceptions import TokenFileNotFound
from client_src.models.token import TokenType


def get_token(token_type: TokenType) -> str:
    if TOKEN_FILE_PATH is None:
        token_file_path = path.join(Path.home(), "tokens.json")
    elif path.isfile(TOKEN_FILE_PATH):
        token_file_path = TOKEN_FILE_PATH
    elif path.isdir(TOKEN_FILE_PATH):
        token_file_path = path.join(TOKEN_FILE_PATH, "tokens.json")
    else:
        raise TokenFileNotFound

    try:
        with open(token_file_path, "r") as token_file:
            tokens = json.load(token_file)

        if type(tokens) != dict or token_type not in tokens:
            raise TokenFileNotFound

        return tokens[token_type]

    except json.decoder.JSONDecodeError:
        raise TokenFileNotFound

    except IOError:
        raise TokenFileNotFound


def set_token(token_type: TokenType, cookies) -> None:
    if TOKEN_FILE_PATH is None:
        token_file_path = path.join(Path.home(), "tokens.json")
    elif path.isfile(TOKEN_FILE_PATH):
        token_file_path = TOKEN_FILE_PATH
    elif path.isdir(TOKEN_FILE_PATH):
        token_file_path = path.join(TOKEN_FILE_PATH, "tokens.json")
    else:
        raise TokenFileNotFound

    if not path.isfile(token_file_path):
        with open(token_file_path, 'w') as fp:
            pass
    try:
        with open(token_file_path, "r") as token_file:
            tokens = json.load(token_file)

    except json.decoder.JSONDecodeError:
        tokens = dict()

    except IOError as e:
        raise TokenFileNotFound

    with open(token_file_path, "w+") as token_file:
        tokens[token_type] = cookies[token_type]
        json.dump(tokens, token_file)


def set_tokens(cookies) -> None:
    set_token(TokenType.access_token, cookies)
    set_token(TokenType.refresh_token, cookies)
