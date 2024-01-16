#!/usr/bin/env python3
""" Provides a Basic Authentication class
"""
from typing import Tuple
from .auth import Auth
from base64 import b64decode


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
                return decoded_base64_authorization_header.split(":")
        return None, None
