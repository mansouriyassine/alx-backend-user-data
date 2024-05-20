#!/usr/bin/env python3
"""
Basic auth module.

Defines the BasicAuth class, which inherits from Auth.
"""

import base64
from api.v1.auth.auth import Auth


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
