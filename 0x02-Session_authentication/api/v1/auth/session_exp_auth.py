#!/usr/bin/env python3
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth.

    This class extends session-based authentication with an expiration mechanism
    for sessions. It provides methods for creating sessions with timeouts and
    verifying their validity.

    Attributes:
        session_duration (int): The duration (in seconds)
        afterwhich a session expires.
            Defaults to 0 (no expiration).
        user_id_by_session_id (dict): A dictionary that maps session IDs to user IDs
            along with session creation timestamps. This dictionary is used to track
            active sessions and their expiration times.
    """

    def __init__(self):
        """
        Constructor for SessionExpAuth.

        Reads the session duration from the environment variable SESSION_DURATION.
        If the variable is not set or its value cannot be converted to an integer,
        the session_duration attribute will be set to 0 (no expiration).
        """
        super().__init__()
        session_duration = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration) if session_duration else 0
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID with an expiration timestamp.

        This method calls the parent class's create_session method to generate a new
        session ID. If successful, it stores the user ID and the current timestamp
        associated with the session ID in the user_id_by_session_id dictionary.

        Args:
            user_id (str, optional): The user ID to create a session for. Defaults to None.

        Returns:
            str: The newly created session ID (if successful), None otherwise.
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
        Returns the User ID associated with a given Session ID, considering expiration.

        This method checks if the provided session ID exists in the
        user_id_by_session_id dictionary. If it does, it retrieves the creation
        timestamp associated with the session. If a session duration is set
        (session_duration > 0), it verifies if the session has expired by comparing
        the creation timestamp with the current time plus the session duration.

        Args:
            session_id (str, optional): The session ID to retrieve the user ID for. Defaults to None.

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
