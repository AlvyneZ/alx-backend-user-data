#!/usr/bin/env python3
""" Provides a Basic Authentication class
"""
from .auth import Auth


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
