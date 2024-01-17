#!/usr/bin/env python3
"""
basic_auth module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, List, Type, Tuple
import base64


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the
        Authorization header for Basic Auth.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        auth_parts = authorization_header.split(" ")
        if len(auth_parts) != 2 or auth_parts[0] != "Basic":
            return None

        return auth_parts[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string and returns the decoded value as a UTF8 string.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user_instance = users[0]

        if not user_instance.is_valid_password(user_pwd):
            return None

        return user_instance

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request using Basic Authentication.
        """
        if request is None or 'Authorization' not in request.headers:
            return None

        auth_header = request.headers['Authorization']
        base64_header = self.extract_base64_authorization_header(auth_header)

        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_email, user_password = self.extract_user_credentials(
            decoded_header)

        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
