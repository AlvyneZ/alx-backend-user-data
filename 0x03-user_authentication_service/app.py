#!/usr/bin/env python3
"""
This "app.py" file Provides a basic flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


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
    res.set_cookie("session_id", sessiond_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
