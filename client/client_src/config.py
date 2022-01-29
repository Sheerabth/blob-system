from os import environ
from dotenv import load_dotenv

load_dotenv()

# API URL
URL = environ.get("URL")
TOKEN_FILE_PATH = environ.get("TOKEN_FILE_PATH")
