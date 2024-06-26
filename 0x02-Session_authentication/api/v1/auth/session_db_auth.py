#!/usr/bin/env python3
"""
Session database authentication module.

This module provides a class for session-based authentication with database storage.
"""
from datetime import datetime, timedelta
from flask import request
from models.user import User
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class that inherits from SessionExpAuth.

    This class implements session-based authentication with database storage.

    Attributes:
        session_duration (int): Duration in seconds after which sessions expire.
            Default is 0 (no expiration).
        _session_db (UserSession): Database to store user sessions.
        _user_db (User): Database to store user information.
    """

    def __init__(self):
        """Initialize a new instance of the SessionDBAuth class."""
        super().__init__()
        self._session_db = UserSession()
        self._user_db = User()

    def create_session(self, user_id=None):
        """
        Create a new user session and store it in the database.

        Args:
            user_id (str, optional): The ID of the user to create a session for.
                If None, no session is created.

        Returns:
            str: The session ID if successful, None otherwise.
        """
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            self._session_db[new_session.id] = new_session
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a given session ID from the database.

        Args:
            session_id (str, optional): The session ID to retrieve the user ID for.

        Returns:
            str: The user ID if the session ID is valid and not expired, None otherwise.
        """
        if session_id is None:
            return None

        session_info = self._session_db.get(session_id)
        if not session_info:
            return None

        if self.session_duration > 0:
            expiration_time = session_info.created_at + timedelta(seconds=self.session_duration)
            if expiration_time < datetime.now():
                return None

        return session_info.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session based on the Session ID from the request cookie.

        Args:
            request (Request, optional): The request object containing the session ID.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        session_id = self.session_cookie(request)
        if session_id:
            session_info = self._session_db.get(session_id)
            if session_info:
                del self._session_db[session_id]
                return True
        return False

    def current_user(self, request=None):
        """
        Get the current user from the request using the session.

        Args:
            request (Request, optional): The request object containing the session ID.

        Returns:
            User: The current user instance or None if not found.
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            return self._user_db.get(user_id)
        return None