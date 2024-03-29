#!/usr/bin/env python3
""" Provides a Basic Authentication class
"""
from typing import Tuple, TypeVar
from base64 import b64decode

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Provides basic authentication services
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the base64 part of the auth
         header for Basic Auth

        Args:
            authorization_header (str): header

        Returns:
            str: extracted base64 part
        """
        if type(authorization_header) == str:
            if authorization_header[:6] == "Basic ":
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the base64 auth header

        Args:
            base64_authorization_header (str): to be decoded

        Returns:
            str: decoded auth header
        """
        if type(base64_authorization_header) == str:
            try:
                return b64decode(
                    base64_authorization_header,
                    validate=True
                ).decode("utf-8")
            except Exception:
                pass
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """
        Retrieves the email and password from the decoded
         auth header

        Args:
            decoded_base64_authorization_header (str): contains
             the email and password as a colon-separated string

        Returns:
            Tuple[str, str]: email and password
        """
        if type(decoded_base64_authorization_header) == str:
            if ":" in decoded_base64_authorization_header:
                sep = decoded_base64_authorization_header.find(":")
                email = decoded_base64_authorization_header[:sep]
                pwd = decoded_base64_authorization_header[(sep + 1):]
                return email, pwd
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """Retrieves User object from database

        Args:
            user_email (str): email of the user
            user_pwd (str): password of the user

        Returns:
            User: The user object if the credentials are correct
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if (len(users) == 1) and\
                    (users[0].is_valid_password(user_pwd)):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User from a given request with credentials
         in the auth header

        Args:
            request (request, optional): the request whose
             user is required. Defaults to None.

        Returns:
            _type_: the User, or None if not authed
        """
        auth_header = self.authorization_header(request)
        b64_auth_cred = self.extract_base64_authorization_header(auth_header)
        auth_cred = self.decode_base64_authorization_header(b64_auth_cred)
        email, pwd = self.extract_user_credentials(auth_cred)
        return self.user_object_from_credentials(email, pwd)
