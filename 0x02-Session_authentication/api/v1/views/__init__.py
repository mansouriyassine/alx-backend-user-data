#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import auth_session_login  # Import the new function here

User.load_from_file()

# Register the new route with the app_views blueprint
app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)(auth_session_login)
