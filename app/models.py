from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class CleaningHistory(Base):
    __tablename__ = "cleaning_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    cleaned_filename = Column(String, nullable=False)
    steps = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class FileHistory(Base):
    __tablename__ = "file_history"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    original_file = Column(String, nullable=False)
    cleaned_file = Column(String)
    steps = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
