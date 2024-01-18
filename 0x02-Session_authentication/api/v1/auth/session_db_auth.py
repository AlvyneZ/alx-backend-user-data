#!/usr/bin/env python3
"""
Provides a Session Authentication class
 whose sessions expire and are stored
"""
from datetime import datetime, timedelta

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Provides expiring stored session authentication
     services
    """
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
            "session_id": sess_id
        }
        user_session = UserSession(**session_dictionary)
        user_session.save()
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
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        sess_dict = sessions[0]
        user_id = sess_dict.user_id
        if (self.session_duration == 0):
            return user_id
        created = sess_dict.created_at
        if created is None:
            return None
        expiry = created + timedelta(seconds=self.session_duration)
        if datetime.now() > expiry:
            return None
        return user_id

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
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
