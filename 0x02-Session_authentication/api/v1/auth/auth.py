#!/usr/bin/env python3
"""
auth module
"""
from flask import request
from typing import List, TypeVar
from os import getenv
import os


class Auth:
    '''Auth class'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path."""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the Flask request."""
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
