#!/usr/bin/env python3
"""
SessionAuth module for the API
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class that inherits from Auth
    This class will be used for session-based authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.
        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID if the session ID is valid, None otherwise.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id)
