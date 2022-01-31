# Blob System

Blob System is a simple blob storage server which allows for file upload, download, rename, edit and delete.

* Server - a [FastAPI](https://fastapi.tiangolo.com/) based web application to handle requests for the blob storage system.
* Client - a [Typer](https://typer.tiangolo.com/) based CLI application to interact with the server.

## Tools & technology used

* Database - PostgreSQL
* Cache - Redis
* ORM - SQLAlchemy

## Setting up the environment

### Cloning the repository

1. Using SSH :
```
git@github.com:Sheerabth/blob-system.git
```
2. Using HTTPS :
```
git clone https://github.com/Sheerabth/blob-system.git
```
3. Using GitHub CLI :
```
gh repo clone Sheerabth/blob-system
```

## Client Setup

### Installing Dependencies
Using [pip](https://pip.pypa.io/en/stable/). Creating a dedicated [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for the project is advised. Recommended python version `>=3.9`
```
cd blob-system/client
pip install -r requirements.txt
```

### Make `.env` configuration
Create a copy of `client/.env.example` in the same directory and name it `.env`. Fill in the required environment variables. You can also have those environment variables set up in your shell.

### Running the client
```
# Inside the client directory
Usage: python -m src [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version                   Show the application's version and exit.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  change-access  Add/modify access given to users for a file
  delete         Delete file
  download       Download file
  edit           Edit file
  get-files      List all files
  info           Get file information of a file
  login          Login user with username
  logout         Logout user
  logout-all     Logout user from all sessions
  refresh        Refresh user's token
  register       Register user with username
  remove-access  Remove access given to users for a file
  rename         Rename file
  upload         Upload new file
```

## Server Setup (Optional)
The deployment server is hosted at [http://52.186.137.111:8080](http://52.186.137.111:8080). So unless you want to run the server locally, this section is not required.

### Installing Dependencies
Using [pip](https://pip.pypa.io/en/stable/). Creating a dedicated [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for the project is advised. Recommended python version `>=3.9`
```
cd blob-system/server
pip install -r requirements.txt
```

### Change client config
As server is being setup locally, change the API URL in the client environment variables to the url where the server is about to be hosted ie. http://localhost:8080

### Database Setup
Databases can be setup locally using docker.
```
# Inside the server directory.
docker-compose up -d
```
Feel free to use your own databases.

### Make `.env` configuration
Create a copy of `server/.env.example` in the same directory and name it `.env`. Fill in the required environment variables. You can also have those environment variables set up in your shell.

### Running the server
```
# Inside the server directory
python -m src
```

## Contributing
All contributions and pull requests are welcome. Open an issue if you find any bugs/faults or if you want to implement a change and would like to discuss the implementation.



## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
* Sheerabth O S - [@Sheerabth](https://github.com/Sheerabth)
