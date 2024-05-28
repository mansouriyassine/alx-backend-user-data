#!/usr/bin/env python3
"""
UserSession model
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class UserSession(Base):
    """
    UserSession model class for storing session information in a database.
    """

    __tablename__ = 'user_sessions'

    id = Column(String(60), primary_key=True, nullable=False)
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args: list, **kwargs: dict):
        """
        Constructor for UserSession model.

        Args:
            user_id (str): The user ID associated with the session.
            session_id (str): The session ID generated for the user session.
        """
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
