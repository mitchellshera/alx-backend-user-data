#!/usr/bin/env python3
"""
basic_auth module
"""
from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Auth.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        auth_parts = authorization_header.split(" ")
        if len(auth_parts) != 2 or auth_parts[0] != "Basic":
            return None

        return auth_parts[1]
