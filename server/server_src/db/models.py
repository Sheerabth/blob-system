import uuid

from sqlalchemy import Column, Float, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
import enum

from .database import Base
from datetime import datetime


class Permissions(str, enum.Enum):
    owner = 'owner'
    read = 'read'
    edit = 'edit'


class UserFileModel(Base):
    __tablename__ = "userfile"

    user_id = Column(String, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    file_id = Column(String, ForeignKey('files.id', ondelete="CASCADE"), primary_key=True)
    access_type = Column(Enum(Permissions))
    file = relationship("FileModel", back_populates="users")
    user = relationship("UserModel", back_populates="files")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, index=True)
    hashed_password = Column(String)
    latest_time = Column(String, default=lambda: datetime.utcnow().isoformat())
    files = relationship("UserFileModel", back_populates="user")


class FileModel(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String, index=True)
    file_size = Column(Float)
    file_path = Column(String, index=True)
    users = relationship("UserFileModel", back_populates="file")
