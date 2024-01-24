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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
