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
