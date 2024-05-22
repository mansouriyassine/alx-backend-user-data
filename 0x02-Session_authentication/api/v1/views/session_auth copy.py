#!/usr/bin/env python3
"""
SessionAuth module for the API

This module handles session-based authentication
using Flask and SessionAuth class.
"""

from flask import jsonify, request, make_response, abort
from os import getenv
from api.v1.app import auth
from models.user import User

sa = auth


def auth_session_login() -> str:
    """
    Function to login using session auth.

    POST /api/v1/auth_session/login

    Returns:
        str: JSON response with user data and sets session cookie on success.

    Raises:
        400: If email or password is missing.
        404: If no user found for the provided email.
        401: If the password is incorrect.

    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        abort(jsonify({"error": "email missing"}), 400)

    if not password:
        abort(jsonify({"error": "password missing"}), 400)

    try:
        user = User.search(email)
    except Exception as e:
        abort(jsonify({"error": "no user found for this email"}), 404)

    if not user.is_valid_password(password):
        abort(jsonify({"error": "wrong password"}), 401)

    session_id = sa.create_session(user.id)

    response = jsonify(user.to_json())

    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
