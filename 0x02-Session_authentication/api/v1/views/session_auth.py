#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if login details are absent
      - 404 if can't find the User
      - 401 if password is incorrect
    """
    email = request.form.get("email")
    if (email is None) or (email == ""):
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if (password is None) or (password == ""):
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    sessiond_id = auth.create_session(getattr(users[0], 'id'))
    res = jsonify(users[0].to_json())
    res.set_cookie(getenv("SESSION_NAME"), sessiond_id)
    return res
