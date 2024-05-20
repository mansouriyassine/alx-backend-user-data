#!/usr/bin/env python3
"""AUTHORIZATION Class"""

from flask import request
from typing import List, TypeVar


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

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if path == excluded_path:
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
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None - request will be the Flask request object.

        Args:
        - request: The Flask request object.

        Returns:
        - None: Placeholder for future implementation.
        """
        return None
