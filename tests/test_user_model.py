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


def test_find_existing_user_by_name():
    user = db.get_user_by_name("guest")
    assert user is not None
    assert type(user) is User
    assert user.id == 2


def test_find_non_existing_user_by_name():
    user = db.get_user_by_name("?")
    assert user is None


def test_get_next_user_id_from_populated_list():
    users = [
        User(id=3, name="user3", password="pwd3"),
        User(id=7, name="user7", password="pwd7"),
    ]
    assert db.get_next_user_id(users) == 8


def test_get_next_user_id_from_empty_list():
    users = []
    assert db.get_next_user_id(users) == 1


def test_add_user():
    user = User(id=0, name="user", password="pwd")
    user = db.add_user(user)
    assert user.id > 0


def test_add_user_with_nonzero_id():
    user = User(id=20, name="user", password="pwd")
    assert db.add_user(user) == None


def test_add_user_with_none_argument():
    assert db.add_user(None) == None


def test_update_user():
    userA = User(id=2, name="new_name", password="?")
    assert db.update_user(userA)
    userB = db.get_user(2)
    assert userA.id == userB.id
    assert userA.name == userB.name


def test_update_non_existing_user():
    user = User(id=5, name="?", password="?")
    assert db.update_user(user) == False


def test_update_user_with_bad_id():
    user1 = User(id=0, name="?", password="?")
    user2 = User(id=-1, name="?", password="?")
    assert db.update_user(user1) == False
    assert db.update_user(user2) == False


def test_update_user_with_none_argument():
    assert db.update_user(None) == False


def test_delete_user():
    old_len = len(db.all_users())
    user = User(id=0, name="?", password="?")
    user = db.add_user(user)
    assert user.id > 0
    assert db.delete_user(user.id)
    assert db.get_user(user.id) == None
    assert len(db.all_users()) == old_len


def test_delete_user_with_bad_id():
    assert db.delete_user(0) == False
    assert db.delete_user(-1) == False
    assert db.delete_user(99) == False
