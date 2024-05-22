#!/usr/bin/env python3
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth.
    This class extends session-based authentication with session expiration.

    Attributes:
        session_duration (int): Duration in seconds after which sessions expire.
                               Default is 0 (no expiration).
        user_id_by_session_id (dict): Dictionary storing session information.
    """

    def __init__(self):
        """
        Constructor for SessionExpAuth.
        Assigns session duration from environment variable SESSION_DURATION.
        """
        super().__init__()
        session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration) if session_duration else 0
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID with expiration.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: The session ID if successful, None otherwise.
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID based on a Session ID with expiration.

        Args:
            session_id (str): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID if the session ID is valid and not expired, None otherwise.
        """
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)
        if not session_info:
            return None

        created_at = session_info.get("created_at")
        if not created_at:
            return None

        if self.session_duration > 0:
            expiration_time = created_at + timedelta(seconds=self.session_duration)
            if expiration_time < datetime.now():
                return None

        return session_info.get("user_id")
