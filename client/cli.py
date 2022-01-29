import os
from pathlib import Path
from typing import Optional
import typer


from client import __app_name__, __version__
from client.exceptions.handler import exception_handler
from client.token import set_tokens, get_token, set_token
from client.extras.token import TokenType
from client.webapi.api import register_user, login_user, logout_user, logout_all_users, get_user_files, \
    upload_user_file, refresh_user, download_user_file, file_access_info, rename_user_file

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
    response_content = register_user(username, password)
    set_tokens(response_content['tokens'])
    typer.echo("Register successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def login(username: str, password: str = typer.Option(..., prompt="Enter your password")):
    response_content = login_user(username, password)
    set_tokens(response_content['tokens'])
    typer.echo("Login successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def refresh():
    refresh_token = get_token(TokenType.refresh_token)
    response_content = refresh_user(refresh_token)
    set_token(TokenType.access_token, response_content['tokens'])
    typer.echo("Refresh successful")
    typer.echo(f"User Id: {response_content['user_id']}")


@app.command()
@exception_handler
def logout():
    refresh_token = get_token(TokenType.refresh_token)
    logout_user(refresh_token)


@app.command()
@exception_handler
def logout_all():
    refresh_token = get_token(TokenType.refresh_token)
    logout_all_users(refresh_token)


@app.command()
@exception_handler
def get_files():
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    for user_file in files:
        typer.echo(f"{files.index(user_file)+1}. File Name: {user_file['file']['file_name']}")


@app.command()
@exception_handler
def upload_file(file_path: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True)):
    input_file = open(file_path, 'rb')
    access_token = get_token(TokenType.access_token)
    upload_user_file(access_token, input_file)


@app.command()
@exception_handler
def download_file(file_path: Path = typer.Option(..., exists=True, file_okay=False, dir_okay=True, resolve_path=True)):
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    for user_file in files:
        typer.echo(f"{files.index(user_file)+1}. File Name: {user_file['file']['file_name']}")
    index = int(typer.prompt("Select your choice"))
    downloaded_file = download_user_file(access_token, files[index-1]['file_id'])
    with open(str(os.path.join(file_path, downloaded_file['file_name'])), 'wb') as target_file:
        for chunk in downloaded_file['content']:
            if chunk:
                target_file.write(chunk)
    typer.echo("Download successful")


@app.command()
@exception_handler
def file_info():
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    for user_file in files:
        typer.echo(f"{files.index(user_file)+1}. File Name: {user_file['file']['file_name']}")
    index = int(typer.prompt("Select your choice"))
    file = file_access_info(access_token, files[index-1]['file_id'])
    typer.echo(f"File Name: {file['file_name']}")
    typer.echo(f"File Size: {file['file_size']} bytes")
    typer.echo("Access users")
    for user in file['users']:
        typer.echo(f"User Id: {user['user_id']}, Access Type: {user['access_type']}")


@app.command()
@exception_handler
def rename_file():
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    for user_file in files:
        typer.echo(f"{files.index(user_file)+1}. File Name: {user_file['file']['file_name']}")
    index = int(typer.prompt("Select your choice"))
    new_file_name = typer.prompt("Enter new file name")
    file = rename_user_file(access_token, files[index - 1]['file_id'], new_file_name)

    typer.echo(f"File Name: {file['file_name']}")
    typer.echo(f"File Size: {file['file_size']} bytes")


@app.command()
@exception_handler
def change_access():
    access_token = get_token(TokenType.access_token)
    files = get_user_files(access_token)
    for user_file in files:
        typer.echo(f"{files.index(user_file) + 1}. File Name: {user_file['file']['file_name']}")
    index = int(typer.prompt("Select your choice"))
    file_id = files[index - 1]['file_id']
    user_id = typer.prompt("Enter user id")

    access_type = typer.prompt("Enter permission to be provided ()")

