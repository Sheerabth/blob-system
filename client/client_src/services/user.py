from typing import Optional

import typer

from client_src.webapi.api import file_access_info


def user_file_prompt(access_token: str, file_id: str, prompt_message: Optional[str] = "Enter used id") -> str:
    file_info = file_access_info(access_token, file_id)
    typer.echo("Access users:")
    for user in file_info["users"]:
        typer.echo(f"User Id: {user['user_id']}, Access Type: {user['access_type']}")

    user_id = typer.prompt(prompt_message)
    return user_id
