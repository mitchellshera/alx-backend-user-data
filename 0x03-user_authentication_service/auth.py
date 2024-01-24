#!/usr/bin/env python3
'''module for auth.py'''

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Generate a salted hash of the input password.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: A salted hash of the input password.
    """
    # Generate a salted hash using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password
