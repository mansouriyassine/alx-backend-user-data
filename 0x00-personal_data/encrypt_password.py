#!/usr/bin/python3
"""
Module for password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a given password using bcrypt.

    Args:
    password (str): The plaintext password to hash.

    Returns:
    bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if a given password matches the hashed password.

    Args:
    hashed_password (bytes): The hashed password to compare against.
    password (str): The plaintext password to check.

    Returns:
    bool: True if the password matches the hashed password, False otherwise.
    """
    decoded_hashed_password = hashed_password.decode()
    return bcrypt.checkpw(password.encode(), decoded_hashed_password.encode())
