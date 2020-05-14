from flask_jwt_extended import decode_token


def test_login(client):
    r = client.post("/api/login", json={"username": "user", "password": "password"})
    assert r.status_code == 200
    assert r.is_json
    access_token = r.get_json().get("access_token")
    assert access_token is not None
    token_data = decode_token(access_token)
    assert token_data.get("identity") == 1


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
