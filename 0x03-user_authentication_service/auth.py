#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User


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
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except ValueError:
            pass
        except Exception as e:
            raise e

        hashed_password = self._hash_password(password)

        user = self._db.add_user(email, hashed_password)

        return user


if __name__ == "__main__":
    auth = Auth()
    try:
        user = auth.register_user("me@me.com", "mySecuredPwd")
        print("Successfully created a new user!")
    except ValueError as err:
        print(f"Could not create a new user: {err}")
