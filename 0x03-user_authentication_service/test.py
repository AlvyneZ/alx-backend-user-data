#!/usr/bin/env python3
"""
This "test.py" file provides code for testing
 the code implemented in this project
"""

"""
Testing the sqlAlchemy User Model
"""
from user import User


print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

print("====================")

"""
Testing the add_user method in the db
"""
from db import DB
from user import User

my_db = DB()

user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

print("====================")

"""
Testing the find_user_by method in db
"""
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com", id=user_2.id)
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")

try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")

print("====================")

"""
Testing the update_user method in db
"""
print("Old Password: {}".format(user_1.hashed_password))

try:
    my_db.update_user(user_1.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

print("New Password: {}".format(
    my_db.find_user_by(id=user_1.id).hashed_password)
)

print("====================")
