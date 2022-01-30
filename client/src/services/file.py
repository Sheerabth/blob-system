from typing import Optional, List, Dict
from tabulate import tabulate
import typer

from src.exception import IndexException, FileNotFoundException
from src.models.permission import Permission
from src.services.user import print_user_access_info
from src.utils.typer_utils import print_header
from src.utils.format_utils import format_iso_string, auto_unit


def filter_files(files: List[Dict], access_type: Optional[Permission] = None, not_access_type: Optional[Permission] = None) -> List:
    file_list = files
    if access_type:
        file_list = [file for file in files if file["access_type"] == access_type]
    elif not_access_type:
        file_list = [file for file in files if file["access_type"] != not_access_type]

    return file_list


def print_file_info(file_info: Dict, users: Optional[Dict[str, str]] = None, file_info_header: Optional[str] = "File Info:") -> None:
    file_info_data = [
        ["Name:", file_info["file_name"]],
        ["Size:", auto_unit(file_info["file_size"])],
        ["Created at:", format_iso_string(file_info["created_at"])],
        ["Updated at:", format_iso_string(file_info["updated_at"])],
    ]

    print_header(file_info_header)
    typer.echo(tabulate(file_info_data, tablefmt="plain", colalign=("right", "left")))

    if users:
        print_user_access_info(file_info["users"], users)


def print_file_table(files: List[Dict]) -> None:
    if len(files) == 0:
        raise FileNotFoundException
    print_header("Available Files:")

    data = [[i, file["file"]["file_name"], auto_unit(file["file"]["file_size"]), format_iso_string(file["file"]["created_at"]),
             format_iso_string(file["file"]["updated_at"])] for i, file in enumerate(files)]
    file_table = tabulate(data, headers=["Index", "Name", "Size", "Created Time", "Updated Time"])

    typer.echo(file_table)


def file_prompt(files: List[Dict], prompt_message: Optional[str] = "Enter file index", access_type: Optional[Permission] = None, not_access_type: Optional[Permission] = None) -> str:
    files = filter_files(files, access_type, not_access_type)
    print_file_table(files)
    try:
        index = int(typer.prompt(prompt_message))
    except ValueError:
        raise IndexException

    if index not in range(len(files)):
        raise IndexException

    file_id = files[index]["file_id"]
    return file_id

