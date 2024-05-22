#!/usr/bin/env python3
"""
DocDocDocDocDocDoc
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import index
from api.v1.views.users import show_users, show_user, create_user, update_user, destroy_user
from api.v1.views.session_auth import auth_session_login

from models.user import User

User.load_from_file()

app_views.add_url_rule('/', 'index', index)
app_views.add_url_rule('/users', 'show_users', show_users)
app_views.add_url_rule('/users/<user_id>', 'show_user', show_user)
app_views.add_url_rule('/users', 'create_user', create_user, methods=['POST'])
app_views.add_url_rule('/users/<user_id>', 'update_user', update_user, methods=['PUT'])
app_views.add_url_rule('/users/<user_id>', 'destroy_user', destroy_user, methods=['DELETE'])

app_views.add_url_rule('/auth_session/login', 'auth_session_login', auth_session_login, methods=['POST'])
