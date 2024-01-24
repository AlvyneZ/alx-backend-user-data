#!/usr/bin/env python3
"""
This "app.py" file Provides a basic flask app
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
