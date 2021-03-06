from flask_jwt_extended import decode_token


def test_login(client):
    r = client.post("/auth/login", json={"username": "user", "password": "password"})
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
    r = client.post("/auth/login", json={"password": "password"})
    assert r.status_code == 400
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password missing."
    assert "access_token" not in data


def test_login_password_missing(client):
    r = client.post("/auth/login", json={"username": "user"})
    assert r.status_code == 400
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password missing."
    assert "access_token" not in data


def test_login_unknown_user(client):
    r = client.post("/auth/login", json={"username": "?", "password": "password"})
    assert r.status_code == 401
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password invalid."
    assert "access_token" not in data


def test_login_with_wrong_password(client):
    r = client.post("/auth/login", json={"username": "user", "password": "?"})
    assert r.status_code == 401
    assert r.is_json
    data = r.get_json()
    assert data.get("message") == "Username or password invalid."
    assert "access_token" not in data


def test_refresh_token(client, auth):
    auth.login()
    old_access_token = auth.access_token
    r = client.post("/auth/refresh", headers={"Authorization": "Bearer {}".format(auth.refresh_token)})
    assert r.status_code == 200
    assert r.is_json
    access_token = r.get_json().get("access_token")
    assert access_token is not None
    assert access_token != old_access_token
    token_data = decode_token(access_token)
    assert token_data.get("identity") == 1


def test_cannot_call_refresh_for_unknown_user(client, auth):
    auth.login()
    assert client.delete("/api/users/{}".format(auth.id), headers={"Authorization": "Bearer {}".format(auth.access_token)}).status_code == 204
    assert client.post("/auth/refresh", headers={"Authorization": "Bearer {}".format(auth.refresh_token)}).status_code == 401


def test_cannot_call_refresh_with_access_token(client, auth):
    auth.login()
    r = client.post("/auth/refresh", headers={"Authorization": "Bearer {}".format(auth.access_token)})
    assert r.status_code == 422
    assert r.is_json
    assert r.get_json().get("error") == "Only refresh tokens are allowed"


def test_cannot_call_protected_api_with_refresh_token(client, auth):
    auth.login()
    r = client.delete("/api/ships/1", headers={"Authorization": "Bearer {}".format(auth.refresh_token)})
    assert r.status_code == 422
    assert r.is_json
    assert r.get_json().get("error") == "Only access tokens are allowed"


def test_logout_access_token(client, auth):
    auth.login()
    # logout and blacklist access token
    r = client.delete("/auth/logout", headers={"Authorization": "Bearer {}".format(auth.access_token)})
    assert r.status_code == 200
    assert r.is_json
    assert r.get_json().get("message") == "Successfully logged out."
    # no longer logged in
    r = client.delete("/api/ships/1", headers={"Authorization": "Bearer {}".format(auth.access_token)})
    assert r.status_code == 401
    assert r.is_json
    assert r.get_json().get("error") == "Token has been revoked"
    # request new access token
    r = client.post("/auth/refresh", headers={"Authorization": "Bearer {}".format(auth.refresh_token)})
    assert r.status_code == 200


def test_logout_refresh_token(client, auth):
    auth.login()
    # logout refresh token
    r = client.delete("/auth/logout2", headers={"Authorization": "Bearer {}".format(auth.refresh_token)})
    assert r.status_code == 200
    assert r.is_json
    assert r.get_json().get("message") == "Successfully logged out."
    # cannot request new access token
    r = client.post("/auth/refresh", headers={"Authorization": "Bearer {}".format(auth.refresh_token)})
    assert r.status_code == 401
    assert r.is_json
    assert r.get_json().get("error") == "Token has been revoked"
