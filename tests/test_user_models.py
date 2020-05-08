from app.models import list_users, find_user, remove_password
from app.models import users


def test_remove_password_does_not_modify_argument():
    user_orig = {"name": "username", "password": "password"}
    user_new = remove_password(user_orig)
    assert "password" in user_orig


def test_remove_password():
    user_orig = {"name": "username", "password": "password"}
    user_new = remove_password(user_orig)
    assert "password" not in user_new


def test_list_users_returns_list():
    users = list_users()
    assert len(users) > 0


def test_find_existing_user():
    user = find_user(1)
    assert user != None
    assert user["id"] == 1


def test_find_non_existing_user():
    user = find_user(1000)
    assert user == None


def test_find_user_removes_password():
    user = find_user(1)
    assert "password" not in user


def test_list_users_removes_passwords():
    for user in list_users():
        assert "password" not in user
