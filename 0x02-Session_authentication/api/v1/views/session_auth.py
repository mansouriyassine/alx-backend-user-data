#!/usr/bin/env python3
"""
SessionAuth module for the API
"""

from api.v1.auth.session_auth import SessionAuth
from flask import jsonify, request, make_response, abort
from models.user import User
from os import getenv

sa = SessionAuth()


@sa.exempt
def auth_session_login() -> str:
    """
    Function to login using session auth
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
    auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, auth.user_id_by_session_id)
    return response
