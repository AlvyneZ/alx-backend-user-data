#!/usr/bin/env python3
""" Provides a Session Authentication class
"""
from uuid import uuid4

from .auth import Auth


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
