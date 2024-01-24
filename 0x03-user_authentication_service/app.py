#!/usr/bin/env python3
"""
This "app.py" file Provides a basic flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()
SESS_ID_COOKIE = "session_id"


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
    Endpoint for testing the running of the API

    Returns:
        - basic test json {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Endpoint for registering a new user
    JSON body:
      - email
      - password

    Returns:
        - json object representing the user
        - 400 if email already registered
    """
    email = request.form.get("email")
    if (email is None) or (email == ""):
        return jsonify({"message": "email missing"}), 400
    password = request.form.get("password")
    if (password is None) or (password == ""):
        return jsonify({"message": "password missing"}), 400
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Endpoint for Logging in a user
    JSON body:
      - email
      - password

    Returns:
        - json object representing the user
        - 401 if credentials are invalid
    """
    email = request.form.get("email")
    if (email is None) or (email == ""):
        abort(401)
    password = request.form.get("password")
    if (password is None) or (password == ""):
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    sessiond_id = AUTH.create_session(email)
    res = jsonify({
        "email": email,
        "message": "logged in"
    })
    res.set_cookie(SESS_ID_COOKIE, sessiond_id)
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Endpoint for Logging out a user
    Cookies:
      - session_id

    Returns:
        - redirect to "/"
        - 403 if user does not exist
    """
    session_id = request.cookies.get(SESS_ID_COOKIE)
    logged_in_user = AUTH.get_user_from_session_id(session_id)
    if logged_in_user is None:
        abort(403)
    AUTH.destroy_session(logged_in_user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Endpoint for getting the logged in user's details
    Cookies:
      - session_id

    Returns:
        - json representation of the user
        - 403 if session is invalid
    """
    session_id = request.cookies.get(SESS_ID_COOKIE)
    logged_in_user = AUTH.get_user_from_session_id(session_id)
    if logged_in_user is None:
        abort(403)
    return jsonify({"email": logged_in_user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Endpoint for Requesting a password reset token
    JSON body:
      - email

    Returns:
        - json object with reset token
        - 403 if email is not registered
    """
    email = request.form.get("email")
    if (email is None) or (email == ""):
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Endpoint for updating a user's password
    JSON body:
      - email
      - reset_token
      - new_password

    Returns:
        - json object representing the user
        - 401 if token is invalid
    """
    email = request.form.get("email")
    if (email is None) or (email == ""):
        abort(403)
    new_password = request.form.get("new_password")
    if (new_password is None) or (new_password == ""):
        abort(403)
    reset_token = request.form.get("reset_token")
    if (reset_token is None) or (reset_token == ""):
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
