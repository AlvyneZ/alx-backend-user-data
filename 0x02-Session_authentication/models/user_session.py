#!/usr/bin/env python3
""" User Session Authentication module
"""
from models.base import Base


class UserSession(Base):
    """ User Session authentication class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User Session instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        # self.created_at = kwargs.get('created_at')
        # Base has its own created_at
