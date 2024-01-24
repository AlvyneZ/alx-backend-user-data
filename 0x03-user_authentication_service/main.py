#!/usr/bin/env python3
"""
This "main.py" file provides code for testing
 the Endpoints provided by the Flask app
"""
import requests


API_URL = "http://0.0.0.0:5000"
SESS_ID_COOKIE = "session_id"


def register_user(email: str, password: str) -> None:
    """Tests the register endpoint [POST /users]
    """
    res = requests.post(
        url="{}/users".format(API_URL),
        data={
            "email": email,
            "password": password
        }
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}


def reregister_user(email: str, password: str) -> None:
    """Tests the register endpoint with an already registered user
    """
    res = requests.post(
        url="{}/users".format(API_URL),
        data={
            "email": email,
            "password": password
        }
    )
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests the login endpoint with wrong credentials
    """
    res = requests.post(
        url="{}/sessions".format(API_URL),
        data={
            "email": email,
            "password": password
        }
    )
    assert res.status_code == 401
    session_id = res.cookies.get(SESS_ID_COOKIE)
    assert session_id is None


def log_in(email: str, password: str) -> str:
    """Tests the login endpoint [POST /sessions]
    """
    res = requests.post(
        url="{}/sessions".format(API_URL),
        data={
            "email": email,
            "password": password
        }
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    session_id = res.cookies.get(SESS_ID_COOKIE)
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Tests the profile endpoint without log in credentials
    """
    res = requests.get(
        url="{}/profile".format(API_URL)
    )
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests the profile endpoint [GET /profile] with
     log in credentials
    """
    res = requests.get(
        url="{}/profile".format(API_URL),
        cookies={SESS_ID_COOKIE: session_id}
    )
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Tests the logout endpoint [DELETE /sessions]
    """
    res = requests.delete(
        url="{}/sessions".format(API_URL),
        cookies={SESS_ID_COOKIE: session_id}
    )
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests the reset password endpoint [POST /reset_password]
    """
    res = requests.post(
        url="{}/reset_password".format(API_URL),
        data={"email": email}
    )
    assert res.status_code == 200
    assert res.json().get("email") == email
    assert "reset_token" in res.json()
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests the update password endpoint [PUT /reset_password]
    """
    res = requests.put(
        url="{}/reset_password".format(API_URL),
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
