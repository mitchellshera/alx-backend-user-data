#!/usr/bin/env python3
"""
auth module
"""
from flask import request
from typing import List, TypeVar

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path."""
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the Flask request."""
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the Flask request."""
        # Placeholder for user retrieval logic
        return None
