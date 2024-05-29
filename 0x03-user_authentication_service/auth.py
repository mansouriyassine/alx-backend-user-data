#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a new UUID.

    Returns:
        str: The string representation of the generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to
                            register.

        Returns:
            User: The User object of the newly registered user.

        Raises:
            ValueError: If a user with the given email
                        already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        except Exception as e:
            raise e

        hashed_password = _hash_password(password)

        user = self._db.add_user(email, hashed_password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_pw = user.hashed_password
            return bcrypt.checkpw(password.encode('utf-8'),
                                  hashed_pw)
        except NoResultFound:
            return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID as a string, or None if the user
                 is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets a user from a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The User object, or None if not found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session by updating the user's session ID to
           None.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass
        except Exception as e:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user with the given email does
                        not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User {email} does not exist")

        reset_token = _generate_uuid()
        try:
            self._db.update_user(user.id, reset_token=reset_token)
        except Exception as e:
            raise e

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)
        try:
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except Exception as e:
            raise e
