#!/usr/bin/env python3
"""
UserSession model module.

This module defines the UserSession model for storing user session information
in a database.
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class UserSession(Base):
    """
    UserSession model class for storing session information in a database.

    Attributes:
        __tablename__ (str): The name of the database table for this model.
        id (Column): The primary key column for the session record.
        user_id (Column): The user ID associated with the session.
        session_id (Column): The unique session ID.
        created_at (Column): The datetime when the session was created.
    """
    __tablename__ = 'user_sessions'
    id = Column(String(60), primary_key=True, nullable=False)
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args: list, **kwargs: dict):
        """
        Constructor for the UserSession model.

        Args:
            *args: Positional arguments (not used).
            **kwargs: Keyword arguments.
                user_id (str): The user ID associated with the session.
                session_id (str): The session ID generated for the user session.
        """
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())  # Generate a unique ID for the session
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')