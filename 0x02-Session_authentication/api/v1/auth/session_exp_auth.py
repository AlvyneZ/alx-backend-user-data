#!/usr/bin/env python3
"""
Provides a Session Authentication class
 whose sessions expire
"""
from datetime import datetime, timedelta
from os import getenv

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Provides expiring session authentication services
    """
    def __init__(self):
        """Sets up the session expiration time
        """
        sess_dur = getenv("SESSION_DURATION", 0)
        try:
            self.session_duration = int(sess_dur)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a given User ID

        Args:
            user_id (str, optional): Defaults to None.

        Returns:
            str: the ID of the created session
        """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves a stored User ID from their session ID

        Args:
            session_id (str, optional): Defaults to None.

        Returns:
            str: The user ID corresponding to the given session
        """
        if (session_id is None) or (type(session_id) != str):
            return None
        sess_dict = self.user_id_by_session_id.get(session_id, None)
        if sess_dict is None:
            return None
        user_id = sess_dict.get("user_id", None)
        if (self.session_duration == 0) or (user_id is None):
            return user_id
        created = sess_dict.get("created_at", None)
        if created is None:
            return None
        expiry = created + timedelta(seconds=self.session_duration)
        if datetime.now() > expiry:
            return None
        return user_id
