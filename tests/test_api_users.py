from flask_jwt_extended import create_access_token


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


def test_create_user(client):
    r = client.post("/api/users", json={"name": "new-name", "password": "secret"})
    assert r.status_code == 201
    assert r.is_json
    user = r.get_json()
    assert user["id"] > 0
    assert user["name"] == "new-name"
    assert "Location" in r.headers
    assert r.headers["Location"].endswith("/api/users/{}".format(user["id"]))


def test_create_user_fails_if_required_field_is_missing(client):
    r = client.post("/api/users", json={"name": "user"})
    assert r.status_code == 400
    assert r.is_json
    user = r.get_json()
    assert "message" in user
    assert "password" in user["message"]
    assert user["message"]["password"][0] == "Missing data for required field."


def test_create_user_fails_if_input_fields_are_too_short(client):
    r = client.post("/api/users", json={"name": "?", "password": "?"})
    assert r.status_code == 400
    assert r.is_json
    data = r.get_json()
    assert "message" in data
    assert "name" in data["message"]
    assert "password" in data["message"]
    assert data["message"]["name"][0] == "Shorter than minimum length 2."
    assert data["message"]["password"][0] == "Shorter than minimum length 4."


def test_create_user_fails_if_data_is_of_wrong_type(client):
    r = client.post("/api/users", json={"name": -1, "password": False})
    assert r.status_code == 400
    assert r.is_json
    user = r.get_json()
    assert "message" in user
    assert "name" in user["message"]
    assert "password" in user["message"]
    assert user["message"]["name"][0] == "Not a valid string."
    assert user["message"]["password"][0] == "Not a valid string."


def test_create_user_fails_if_data_contains_id(client):
    r = client.post("/api/users", json={"id": 1, "name": "??", "password": "????"})
    assert r.status_code == 400


def test_create_user_fails_if_username_is_already_taken(client):
    client.post("/api/users", json={"name": "already-taken", "password": "????"}).status_code == 201
    r = client.post("/api/users", json={"name": "already-taken", "password": "????"})
    assert r.status_code == 400
    assert r.get_json().get("message") == "User already exists."


def test_update_user(client, auth):
    auth.login()
    r = client.put("/api/users/{}".format(auth.id), headers=auth.headers, json={"id": auth.id, "name": "new-name", "password": "new-pwd"})
    assert r.status_code == 200
    assert r.is_json
    user = r.get_json()
    assert user["id"] == 1
    assert user["name"] == "new-name"


def test_update_user_without_login(client):
    assert client.put("/api/users/1", json={"id": 1, "name": "new-name", "password": "new-pwd"}).status_code == 401


def test_update_non_existing_user(client):
    r = client.put("/api/users/99", json={"id": 99, "name": "??", "password": "????"}, headers={"Authorization": "Bearer " + create_access_token(identity=99)})
    assert r.status_code == 404


def test_update_user_ensures_request_data_id_matches_resource_id(client, auth):
    """If request data contains an (optional) "id" then it has to match the resource id."""
    auth.login()
    assert client.put("/api/users/{}".format(auth.id), headers=auth.headers, json={"id": auth.id, "name": "??", "password": "????"}).status_code == 200
    assert client.put("/api/users/{}".format(auth.id), headers=auth.headers, json={"name": "??", "password": "????"}).status_code == 200
    r = client.put("/api/users/{}".format(auth.id), headers=auth.headers, json={"id": auth.id + 1, "name": "??", "password": "????"})
    assert r.status_code == 400
    json = r.get_json()
    assert "message" in json
    assert json["message"] == "Request data id has to match resource id."


def test_update_different_user_is_forbidden(client, auth):
    auth.login()
    r = client.put("/api/users/2", headers=auth.headers, json={"name": "new-name", "password": "new-pwd"})
    assert r.status_code == 403


def test_delete_user(client, auth):
    auth.login()
    assert client.delete("/api/users/{}".format(auth.id), headers=auth.headers).status_code == 204


def test_delete_user_without_login(client):
    assert client.delete("/api/users/1").status_code == 401


def test_delete_user_that_does_not_exist(client, auth):
    auth.login()
    assert client.delete("/api/users/{}".format(auth.id), headers=auth.headers).status_code == 204
    assert client.delete("/api/users/{}".format(auth.id), headers=auth.headers).status_code == 404


def test_delete_different_user_is_forbidden(client, auth):
    auth.login()
    assert client.delete("/api/users/2", headers=auth.headers).status_code == 403
