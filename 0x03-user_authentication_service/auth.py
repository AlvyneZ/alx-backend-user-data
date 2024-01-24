#!/usr/bin/env python3
"""
This "auth.py" file Provides the authentication services
"""
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """Generates a unique id
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a user to the database
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(
                email, _hash_password(password)
            )
        raise ValueError(
            "User {} already exists".format(email)
        )

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(
            password.encode("utf-8"), user.hashed_password
        )

    def create_session(self, email: str) -> bool:
        """Validates login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        self._db.update_user(
            user.id, session_id=_generate_uuid()
        )
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves a user from the session
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Deletes a user's active session for loggin out
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Deletes a user's active session for loggin out
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        self._db.update_user(
            user.id, reset_token=_generate_uuid()
        )
        return user.reset_token
