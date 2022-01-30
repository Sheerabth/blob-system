import typer


def print_header(content: str) -> None:
    typer.secho("\n" + content, fg=typer.colors.BRIGHT_WHITE, bold=True)


def print_entry(content: str) -> None:
    typer.secho(content, fg=typer.colors.BRIGHT_BLUE)


def print_success(content: str) -> None:
    typer.secho(content, fg=typer.colors.GREEN)


def print_error(content: str) -> None:
    typer.secho("ERROR: " + content, fg=typer.colors.RED)
