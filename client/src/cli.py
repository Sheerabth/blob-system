from os import path
from pathlib import Path
from typing import Optional
import typer
from passlib.context import CryptContext

from src import __app_name__, __version__
from src.exception import PermissionException, FileNotFoundException
from src.exception.handler import exception_handler
from src.models.permission import Permission
from src.services.file import file_prompt
from src.services.user import user_file_prompt
from src.services.token import set_tokens, get_token, set_token
from src.models.token import TokenType
from src.webapi.api import (
    register_user,
    login_user,
    logout_user,
    logout_all_users,
    get_user_files,
    upload_user_file,
    refresh_user,
    download_user_file,
    file_access_info,
    rename_user_file,
    change_user_access,
    remove_user_access,
    get_user_info,
    delete_user_file,
    edit_user_file, stream_upload_user_file, stream_edit_user_file,
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
def register(username: str, password: str = typer.Option(..., prompt="Enter your password")):
    """
    Register user with username
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    response_content = register_user(username, pwd_context.hash(password))
    set_tokens(response_content["tokens"])
    typer.echo("Register successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def login(username: str, password: str = typer.Option(..., prompt="Enter your password")):
    """
    Login user with username
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    response_content = login_user(username, pwd_context.hash(password))
    set_tokens(response_content["tokens"])
    typer.echo("Login successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def refresh():
    """
    Refresh user's token
    """
    refresh_token = get_token(TokenType.refresh_token)
    response_content = refresh_user(refresh_token)
    set_token(TokenType.access_token, response_content["tokens"])
    typer.echo("Refresh successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def logout():
    """
    Logout user
    """
    refresh_token = get_token(TokenType.refresh_token)
    logout_user(refresh_token)
    typer.echo("Logout successful")


@app.command()
@exception_handler
def logout_all():
    """
    Logout user from all sessions
    """
    refresh_token = get_token(TokenType.refresh_token)
    logout_all_users(refresh_token)
    typer.echo("Logout successful")


@app.command()
@exception_handler
def get_files():
    """
    List all files
    """
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    if len(files) == 0:
        raise FileNotFoundException
    typer.echo("Available Files:")
    for user_file in files:
        typer.echo(f"{files.index(user_file)+1}. File Name: {user_file['file']['file_name']}")


@app.command()
@exception_handler
def upload_file(file_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True), no_stream: bool = typer.Option(False, "--no-stream", "-n", help="Don't stream file upload")):
    """
    Upload new file

    If --no-stream is used, file will be streamed uploaded
    """
    input_file = open(file_path, "rb")
    access_token = get_token(TokenType.access_token)
    if no_stream:
        file = upload_user_file(access_token, input_file)
    else:
        file = stream_upload_user_file(access_token, path.basename(file_path), input_file)
    typer.echo("File uploaded")
    typer.echo(f"File Name: {file['file_name']}, File Size: {file['file_size']} bytes")


@app.command()
@exception_handler
def download_file(file_path: Path = typer.Option(..., exists=True, file_okay=False, dir_okay=True, resolve_path=True)):
    """
    Download file
    """
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index to download")
    downloaded_file = download_user_file(access_token, file_id)
    with open(str(path.join(file_path, downloaded_file["file_name"])), "wb") as target_file:
        for chunk in downloaded_file["content"]:
            if chunk:
                target_file.write(chunk)
    typer.echo("Download successful")


@app.command()
@exception_handler
def file_info():
    """
    Get file information of a file
    """
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index for info")
    file = file_access_info(access_token, file_id)
    typer.echo("File Info:")
    typer.echo(f"File Name: {file['file_name']}")
    typer.echo(f"File Size: {file['file_size']} bytes")
    typer.echo("Access users:")
    for user in file["users"]:
        user_info = get_user_info(access_token, user["user_id"])
        typer.echo(
            f"User Name: {user_info['username']}, Access Type: {user['access_type']}, User Id: {user['user_id']}"
        )


@app.command()
@exception_handler
def rename_file():
    """
    Rename file
    """
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index to rename", not_access_type=Permission.read)
    new_file_name = typer.prompt("Enter new file name")
    file = rename_user_file(access_token, file_id, new_file_name)

    typer.echo("File rename successful")
    typer.echo(f"File Name: {file['file_name']}, File Size: {file['file_size']} bytes")


@app.command()
@exception_handler
def edit_file(file_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True), no_stream: bool = typer.Option(False, "--no-stream", "-n", help="Don't stream file upload")):
    """
    Edit file
    """
    input_file = open(file_path, "rb")
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index to edit", not_access_type=Permission.read)
    if no_stream:
        file = edit_user_file(access_token, file_id, input_file)
    else:
        file = stream_edit_user_file(access_token, file_id, path.basename(file_path), input_file)
    typer.echo("File edited")
    typer.echo(f"File Name: {file['file_name']}, File Size: {file['file_size']} bytes")


@app.command()
@exception_handler
def change_access():
    """
    Add/modify access given to users for a file
    """
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index to change access", access_type=Permission.owner)
    user_id = user_file_prompt(access_token, file_id, prompt_message="Enter user id to change access")
    access_type = typer.prompt("Enter permission to be provided")

    if access_type != Permission.owner and access_type != Permission.edit and access_type != Permission.read:
        raise PermissionException
    result = change_user_access(access_token, user_id, file_id, access_type)
    typer.echo(f"Access change successful")


@app.command()
@exception_handler
def remove_access():
    """
    Remove access given to users for a file
    """
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index to remove access", access_type=Permission.owner)
    user_id = user_file_prompt(access_token, file_id, prompt_message="Enter user id to remove access")

    result = remove_user_access(access_token, user_id, file_id)
    typer.echo(f"Access removal successful")


@app.command()
@exception_handler
def delete_file():
    """
    Delete file
    """
    access_token = get_token(TokenType.access_token)
    file_id = file_prompt(access_token, prompt_message="Enter file index delete", access_type=Permission.owner)

    result = delete_user_file(access_token, file_id)
    typer.echo(f"File delete successful")
