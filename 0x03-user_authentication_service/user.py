#!/usr/bin/env python3
"""
This "user.py" file Provides the sqlAlchemy User model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """Stores User credentials and details

    Attributes:
        id(Integer): the integer primary key
        email(String(250)): a non-nullable string
        hashed_password(String(250)): a non-nullable string
        session_id(String(250)): a nullable string
        reset_token(String(250)): a nullable string
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
