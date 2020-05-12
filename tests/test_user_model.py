from app import db
from app.models import User


def test_all_users_returns_list():
    users = db.all_users()
    assert len(users) > 0
    assert type(users[0]) is User


def test_find_existing_user():
    user = db.get_user(1)
    assert user != None
    assert type(user) is User
    assert user.id == 1


def test_find_non_existing_user():
    user = db.get_user(1000)
    assert user == None
