#!/usr/bin/env python3
""" Provides a Session Authentication class
"""
from uuid import uuid4
from typing import TypeVar

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Provides session authentication services
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a given User ID

        Args:
            user_id (str, optional): Defaults to None.

        Returns:
            str: the ID of the created session
        """
        if (user_id is None) or (type(user_id) != str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id.update({session_id: user_id})
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a stored User ID from their session ID

        Args:
            session_id (str, optional): Defaults to None.

        Returns:
            str: The user ID corresponding to the given session
        """
        if (session_id is None) or (type(session_id) != str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the logged in User from a given request

        Args:
            request (request, optional): the request whose
             user is required. Defaults to None.

        Returns:
            User: the User, or None if not logged in
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Deletes a user's login session

        Args:
            request (request, optional): the request from
             the user to be logged out. Defaults to None.

        Returns:
            bool: True if successful, False otherwise
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
