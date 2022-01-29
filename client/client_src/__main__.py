from client_src import __app_name__
from client_src import cli


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
