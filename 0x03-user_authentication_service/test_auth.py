#!/usr/bin/env python3
"""
This "test_auth.py" file provides code for testing
 the Authentication code implemented in this project
"""

"""
Testing the _hash_password method in auth
"""
from auth import _hash_password

print(_hash_password("Hello Holberton"))

print("====================")

"""
Testing the _hash_password method in auth
"""
from auth import Auth

email = 'me@me.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

print("====================")

"""
Testing the valid_login method in auth
"""
print(auth.valid_login(email, password))

print(auth.valid_login(email, "WrongPwd"))

print(auth.valid_login("unknown@email", password))

print("====================")

"""
Testing the _generate_uuid method in auth
"""
from auth import _generate_uuid

print(_generate_uuid())

print("====================")

"""
Testing the create_session method in auth
"""
session_id = auth.create_session(email)
print(session_id)
print(auth.create_session("unknown@email.com"))

print("====================")

"""
Testing the create_session method in auth
"""
rtrvd_user = auth.get_user_from_session_id(session_id)
print(rtrvd_user.email)

print("====================")
