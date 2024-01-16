#!/usr/bin/env python3
""" Provides the Authentication class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Provides authentication services
    """
    def require_auth(
            self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks whether a path requires authentication to
         be accessed

        Args:
            path (str): Path to be checked
            excluded_paths (List[str]): paths that do not need
             authentication

        Returns:
            bool: True if the path needs authentication (not
             excluded), False otherwise
        """
        if (path is None) or (excluded_paths is None):
            return True
        if (path[-1] == "/"):
            path2 = path[:-1]
        else:
            path2 = path + "/"
        if (path in excluded_paths) or (path2 in excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authentication header of a request

        Args:
            request (request, optional): the request whose
             authorization header is required. Defaults to None.

        Returns:
            str: the Authorization header, or None if absent
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the logged in User from a given request

        Args:
            request (request, optional): the request whose
             user is required. Defaults to None.

        Returns:
            _type_: the User, or None if not logged in
        """
        return None
