from typing import Optional

import typer

from src.exceptions import IndexException, FileNotFoundException
from src.models.permission import Permission
from src.webapi.api import get_user_files


def file_prompt(access_token: str, prompt_message: Optional[str] = "Enter file index", access_type: Optional[Permission] = None, not_access_type: Optional[Permission] = None) -> str:
    files = get_user_files(access_token)
    if len(files) == 0:
        raise FileNotFoundException
    typer.echo("Available Files:")
    indices = list()
    if access_type:
        for user_file in files:
            if user_file["access_type"] == access_type:
                indices.append(files.index(user_file) + 1)
                typer.echo(f"{files.index(user_file) + 1}. File Name: {user_file['file']['file_name']}")

    elif not_access_type:
        for user_file in files:
            if user_file["access_type"] != not_access_type:
                indices.append(files.index(user_file) + 1)
                typer.echo(f"{files.index(user_file) + 1}. File Name: {user_file['file']['file_name']}")

    else:
        for user_file in files:
            indices.append(files.index(user_file) + 1)
            typer.echo(f"{files.index(user_file) + 1}. File Name: {user_file['file']['file_name']}")

    try:
        index = int(typer.prompt(prompt_message))

    except ValueError:
        raise IndexException

    if index not in indices:
        raise IndexException

    file_id = files[index - 1]["file_id"]

    return file_id
