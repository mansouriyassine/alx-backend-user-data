#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Returns:
            User: The User object of the newly registered user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if the user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass  # User not found, continue with registration
        except Exception as e:
            raise e  # Propagate any unexpected errors

        # Hash the password
        hashed_password = self._hash_password(password)

        # Add the user to the database
        user = self._db.add_user(email, hashed_password)

        return user

# For testing the function
if __name__ == "__main__":
    print(Auth()._hash_password("Hello Holberton"))
