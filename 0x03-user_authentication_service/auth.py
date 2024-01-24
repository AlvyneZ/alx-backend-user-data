#!/usr/bin/env python3
"""
This "auth.py" file Provides the authentication services
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Hashes a password
    """
    return hashpw(password.encode("utf-8"), gensalt())
