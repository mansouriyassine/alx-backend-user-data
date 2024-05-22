#!/usr/bin/env python3
"""
AUTHORIZATION Class
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Auth class to manage API authentication.

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool:
      Determines if authentication is required based on the path and
      excluded_paths.

    - authorization_header(request=None) -> str:
      Returns the value of the authorization header from the request.

    - current_user(request=None) -> TypeVar('User'):
      Returns None (placeholder for future implementation).

    - session_cookie(request=None) -> str:
      Returns the value of the session cookie from the request.

    Attributes:
    None
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required.

        Args:
        - path (str): The path of the request.
        - excluded_paths (List[str]): List of paths that do not require
          authentication.

        Returns:
        - bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the authorization header from the request.

        Args:
        - request: The Flask request object.

        Returns:
        - str: The value of the Authorization header or None if not present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None - request will be the Flask request object.

        Args:
        - request: The Flask request object.

        Returns:
        - None: Placeholder for future implementation.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Returns a cookie value from a request.

        Args:
        - request: The Flask request object.

        Returns:
        - str: The value of the session cookie or None if not present.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
