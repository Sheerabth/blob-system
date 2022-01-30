from os import path
from pathlib import Path
from typing import Optional
import typer
from passlib.context import CryptContext

from src import __app_name__, __version__
from src.exception import PermissionException, FileNotFoundException
from src.exception.handler import exception_handler
from src.models.permission import Permission
from src.services.file import file_prompt, filter_files, print_file_table, print_file_info
from src.services.user import user_file_prompt
from src.services.token import set_tokens, get_token, set_token
from src.models.token import TokenType
from src.utils.typer_utils import print_success
from src.webapi.api import (
    register_user,
    login_user,
    logout_user,
    logout_all_users,
    get_user_files,
    refresh_user,
    download_user_file,
    file_access_info,
    rename_user_file,
    change_user_access,
    remove_user_access,
    get_user_info,
    delete_user_file,
    stream_upload_user_file, stream_edit_user_file,
)

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
@exception_handler
def register(username: str, password: str = typer.Option(..., prompt="Enter your password", hide_input=True)):
    """
    Register user with username
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    response_content = register_user(username, pwd_context.hash(password))
    set_tokens(response_content["tokens"])
    print_success("Register successful")
    typer.echo(f"User Id: {response_content['user_id']}, Username: {username}")


@app.command()
@exception_handler
def login(username: str, password: str = typer.Option(..., prompt="Enter your password", hide_input=True)):
    """
    Login user with username
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    response_content = login_user(username, pwd_context.hash(password))
    set_tokens(response_content["tokens"])
    print_success("Login successful")
    typer.echo(f"User Id: {response_content['user_id']}, Username: {username}")


@app.command()
@exception_handler
def refresh():
    """
    Refresh user's token
    """
    refresh_token = get_token(TokenType.refresh_token)
    response_content = refresh_user(refresh_token)
    set_token(TokenType.access_token, response_content["tokens"])
    print_success("Refresh successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def logout():
    """
    Logout user
    """
    refresh_token = get_token(TokenType.refresh_token)
    logout_user(refresh_token)
    print_success("Logout successful")


@app.command()
@exception_handler
def logout_all():
    """
    Logout user from all sessions
    """
    refresh_token = get_token(TokenType.refresh_token)
    logout_all_users(refresh_token)
    print_success("Logout successful")


@app.command()
@exception_handler
def get_files(access: Optional[Permission] = typer.Option(None, show_choices=True, case_sensitive=False)):
    """
    List all files
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    if len(files) == 0:
        raise FileNotFoundException

    files = filter_files(files, access)
    print_file_table(files)


@app.command()
@exception_handler
def upload_file(file_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True)):
    """
    Upload new file

    If --no-stream is used, file will be streamed uploaded
    """
    input_file = open(file_path, "rb")
    access_token = get_token(TokenType.access_token)
    file = stream_upload_user_file(access_token, path.basename(file_path), input_file)
    print_success("File uploaded")
    print_file_info(file)


@app.command()
@exception_handler
def download_file(file_path: Path = typer.Option(..., exists=True, file_okay=False, dir_okay=True, resolve_path=True)):
    """
    Download file
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index to download")
    downloaded_file = download_user_file(access_token, file_id)

    with open(str(path.join(file_path, downloaded_file["file_name"])), "wb") as target_file:
        for chunk in downloaded_file["content"]:
            if chunk:
                target_file.write(chunk)
    print_success("Download successful")


@app.command()
@exception_handler
def file_info():
    """
    Get file information of a file
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index for info")
    file = file_access_info(access_token, file_id)
    user_ids = [user["user_id"] for user in file["users"]]
    users = {user_id: get_user_info(access_token, user_id)["username"] for user_id in user_ids}
    print_file_info(file, users)


@app.command()
@exception_handler
def rename_file():
    """
    Rename file
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index to rename", not_access_type=Permission.read)
    new_file_name = typer.prompt("Enter new file name")
    file = rename_user_file(access_token, file_id, new_file_name)

    print_success("File rename successful")
    print_file_info(file, file_info_header="Updated File Info:")


@app.command()
@exception_handler
def edit_file(file_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True)):
    """
    Edit file
    """
    input_file = open(file_path, "rb")
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index to edit", not_access_type=Permission.read)
    file = stream_edit_user_file(access_token, file_id, path.basename(file_path), input_file)
    print_success("File edited")
    print_file_info(file, file_info_header="Updated File Info:")


@app.command()
@exception_handler
def change_access():
    """
    Add/modify access given to users for a file
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index to change access", access_type=Permission.owner)
    file = file_access_info(access_token, file_id)
    user_ids = [user["user_id"] for user in file["users"]]
    users = {user_id: get_user_info(access_token, user_id)["username"] for user_id in user_ids}
    user_id = user_file_prompt(file["users"], users, prompt_message="Enter user id to change access")
    access_type = typer.prompt("Enter permission to be provided")

    if access_type != Permission.owner and access_type != Permission.edit and access_type != Permission.read:
        raise PermissionException
    change_user_access(access_token, user_id, file_id, access_type)
    print_success(f"Access changed")


@app.command()
@exception_handler
def remove_access():
    """
    Remove access given to users for a file
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index to remove access", access_type=Permission.owner)
    file = file_access_info(access_token, file_id)
    user_ids = [user["user_id"] for user in file["users"]]
    users = {user_id: get_user_info(access_token, user_id)["username"] for user_id in user_ids}
    user_id = user_file_prompt(file["users"], users, prompt_message="Enter user id to remove access")

    remove_user_access(access_token, user_id, file_id)
    print_success(f"Access removed")


@app.command()
@exception_handler
def delete_file():
    """
    Delete file
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    file_id = file_prompt(files, prompt_message="Enter file index delete", access_type=Permission.owner)

    result = delete_user_file(access_token, file_id)
    print_success(f"File deleted")
    print_file_info(result, file_info_header="Deleted File Info:")
