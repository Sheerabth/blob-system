from enum import Enum


class Permission(str, Enum):
    owner = "owner"
    read = "read"
    edit = "edit"
