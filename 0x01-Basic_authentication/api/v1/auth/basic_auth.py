#!/usr/bin/env python3
"""
Basic auth module.

This module defines the BasicAuth class, which inherits from Auth.
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class.

    This class inherits from Auth and provides basic authentication methods.

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool:
      Determines if authentication is required based on the
      path and excluded_paths.

    - authorization_header(request=None) -> str:
      Returns the value of the authorization header from the request.

    - current_user(request=None) -> TypeVar('User'):
      Returns None (placeholder for future implementation).

    Attributes:
    None
    """
    pass
