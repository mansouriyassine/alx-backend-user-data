#!/usr/bin/env python3
"""
Basic auth module.

Defines the BasicAuth class, which inherits from Auth.
"""

import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class.

    Inherits from Auth and provides basic authentication methods.

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool:
      Determines if authentication is required based on the path and
      excluded_paths.

    - authorization_header(request=None) -> str:
      Returns the value of the authorization header from the request.

    - current_user(request=None) -> TypeVar('User'):
      Returns None (placeholder for future implementation).

    - extract_base64_authorization_header(
        authorization_header: str) -> str:
      Extracts the Base64 part of the Authorization header for Basic
      Authentication.

    - decode_base64_authorization_header(
        base64_authorization_header: str) -> str:
      Decodes the Base64 string from the Authorization header into a UTF-8
      string.

    - extract_user_credentials(
        decoded_base64_authorization_header: str) -> (str, str):
      Extracts user email and password from the decoded Base64
      Authorization header.

    - user_object_from_credentials(
        user_email: str, user_pwd: str) -> TypeVar('User'):
      Retrieves the User instance based on email and password.

    - current_user(request=None) -> TypeVar('User'):
      Retrieves the User instance for a request using Basic Auth.

    Attributes:
    None
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic
        Authentication.

        Args:
        - authorization_header (str): The Authorization header string.

        Returns:
        - str: The Base64 part of the Authorization header or None if not
          valid.
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str)):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 string from the Authorization header into a UTF-8
        string.

        Args:
        - base64_authorization_header (str): The Base64 Authorization header
          string.

        Returns:
        - str: The decoded UTF-8 string or None if not valid Base64.
        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None

        try:
            base64_bytes = base64_authorization_header.encode('ascii')
            base64_bytes_decoded = base64.b64decode(base64_bytes)
            utf8_string = base64_bytes_decoded.decode('utf-8')
            return utf8_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from the decoded Base64
        Authorization header.

        Args:
        - decoded_base64_authorization_header (str): The decoded Base64
          Authorization header string.

        Returns:
        - tuple: (user_email, user_password) or (None, None) if not valid.
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password.

        Args:
        - user_email (str): The email of the user.
        - user_pwd (str): The password of the user.

        Returns:
        - TypeVar('User'): The User instance if valid credentials, else None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request using Basic Auth.

        Args:
        - request: The request object.

        Returns:
        - TypeVar('User'): The User instance if valid credentials, else None.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)


if __name__ == "__main__":
    pass
