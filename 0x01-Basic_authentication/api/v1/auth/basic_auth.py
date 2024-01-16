#!/usr/bin/env python3
""" Provides a Basic Authentication class
"""
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
