from typing import Optional, List, Dict

import typer
from tabulate import tabulate

from src.exception import InvalidUserException
from src.utils.typer_utils import print_header


def print_user_access_info(access_entries: List[Dict], users: Dict[str, str]) -> None:
    user_data = [[users[entry["user_id"]], entry["user_id"], entry["access_type"]] for entry in access_entries]
    user_table = tabulate(user_data, headers=["Username", "User ID", "Access"])

    print_header("User Access Info:")
    typer.echo(user_table)


def user_file_prompt(
    access_entries: List[Dict],
    users: Dict[str, str],
    check_user_id: Optional[bool] = False,
    prompt_message: Optional[str] = "Enter used id",
) -> str:
    print_user_access_info(access_entries, users)

    user_id = typer.prompt(prompt_message)

    if check_user_id and user_id not in users.keys():
        raise InvalidUserException

    return user_id
