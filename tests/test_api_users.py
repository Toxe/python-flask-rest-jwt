def test_get_users(client):
    r = client.get("/api/users")
    assert r.status_code == 200
    assert r.is_json
    assert len(r.get_json()) > 0


def test_get_user(client):
    r = client.get("/api/users/2")
    assert r.status_code == 200
    assert r.is_json
    user = r.get_json()
    assert user["id"] == 2


def test_get_missing_user(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404


def test_get_users_does_not_return_passwords(client):
    for user in client.get("/api/users").get_json():
        assert "password" not in user


def test_get_user_does_not_return_password(client):
    user = client.get("/api/users/1").get_json()
    assert "password" not in user
