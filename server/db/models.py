from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    files = relationship("File", back_populates="owner")


class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    file_size = Column(Float)
    file_path = Column(String, index=True)
    access_id = Column(Integer, ForeignKey("users.id"))
    is_owner = Column(Boolean, default=False)

    owner = relationship("User", back_populates="items")
