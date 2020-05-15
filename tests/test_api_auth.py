from flask_jwt_extended import decode_token


def test_login(client):
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    assert r.status_code == 200
    assert r.is_json
    access_token = r.get_json().get("access_token")
    refresh_token = r.get_json().get("refresh_token")
    assert access_token is not None
    assert refresh_token is not None
    token_data = decode_token(access_token)
    refresh_token_data = decode_token(refresh_token)
    assert token_data.get("identity") == 1
    assert refresh_token_data.get("identity") == 1


def test_login_username_missing(client):
    r = client.post("/api/login", json={"password": "password"})
    assert r.status_code == 400
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password missing."
    assert "access_token" not in data


def test_login_password_missing(client):
    r = client.post("/api/login", json={"username": "user"})
    assert r.status_code == 400
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password missing."
    assert "access_token" not in data


def test_login_unknown_user(client):
    r = client.post("/api/login", json={"username": "?", "password": "password"})
    assert r.status_code == 401
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password invalid."
    assert "access_token" not in data


def test_login_with_wrong_password(client):
    r = client.post("/api/login", json={"username": "user", "password": "?"})
    assert r.status_code == 401
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password invalid."
    assert "access_token" not in data


def test_refresh_token(client):
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    refresh_token = r.get_json().get("refresh_token")
    old_access_token = r.get_json().get("access_token")
    r = client.post("/api/refresh", headers={"Authorization": "Bearer {}".format(refresh_token)})
    assert r.status_code == 200
    assert r.is_json
    access_token = r.get_json().get("access_token")
    assert access_token is not None
    assert access_token != old_access_token
    token_data = decode_token(access_token)
    assert token_data.get("identity") == 1


def test_cannot_call_refresh_for_unknown_user(client):
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    access_token = r.get_json().get("access_token")
    refresh_token = r.get_json().get("refresh_token")
    user_id = decode_token(access_token).get("identity")
    assert client.delete("/api/users/{}".format(user_id), headers={"Authorization": "Bearer {}".format(access_token)}).status_code == 204
    assert client.post("/api/refresh", headers={"Authorization": "Bearer {}".format(refresh_token)}).status_code == 401


def test_cannot_call_refresh_with_access_token(client):
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    access_token = r.get_json().get("access_token")
    r = client.post("/api/refresh", headers={"Authorization": "Bearer {}".format(access_token)})
    assert r.status_code == 422
    assert r.is_json
    assert r.get_json().get("error") == "Only refresh tokens are allowed"


def test_cannot_call_protected_api_with_refresh_token(client):
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    refresh_token = r.get_json().get("refresh_token")
    r = client.delete("/api/ships/1", headers={"Authorization": "Bearer {}".format(refresh_token)})
    assert r.status_code == 422
    assert r.is_json
    assert r.get_json().get("error") == "Only access tokens are allowed"
