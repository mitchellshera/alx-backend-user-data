#!/usr/bin/env python3
'''module for auth.py'''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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

def _generate_uuid() -> str:
        """
        Generate a uuid and return its string representation
        """
        return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            # User does not exist, proceed with registration
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        ''' checks if the password is valid'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        psswd = password.encode("utf-8")
        return bcrypt.checkpw(psswd, user_password)
