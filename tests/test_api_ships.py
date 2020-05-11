def test_get_ships(client):
    r = client.get("/api/ships")
    assert r.status_code == 200
    assert r.is_json
    assert len(r.get_json()) > 0


def test_get_ship(client):
    r = client.get("/api/ships/3")
    assert r.status_code == 200
    assert r.is_json
    ship = r.get_json()
    assert ship["id"] == 3


def test_get_missing_ship(client):
    r = client.get("/api/ships/999")
    assert r.status_code == 404


def test_create_ship(client):
    r = client.post("/api/ships", json={
        "affiliation": "Affiliation", "crew": 1, "length": 1, "model": "Model", "ship_class": "Class", "roles": ["Role1", "Role2"], "category": "Category", "manufacturer": "Manufacturer"
    })
    assert r.status_code == 201
    assert r.is_json
    ship = r.get_json()
    assert ship["id"] > 0
    assert ship["ship_class"] == "Class"
    assert "Location" in r.headers
    assert r.headers["Location"].endswith("/api/ships/{}".format(ship["id"]))


def test_create_ship_fails_if_data_is_missing(client):
    r = client.post("/api/ships", json={
        "affiliation": "Affiliation", "crew": 1, "length": 1, "model": "Model", "ship_class": "Class", "roles": ["Role1", "Role2"]
    })
    assert r.status_code == 400
    assert r.is_json
    ship = r.get_json()
    assert "message" in ship
    assert "category" in ship["message"]
    assert "manufacturer" in ship["message"]
    assert ship["message"]["category"][0] == "Missing data for required field."
    assert ship["message"]["manufacturer"][0] == "Missing data for required field."


def test_create_ship_fails_if_data_is_of_wrong_type(client):
    r = client.post("/api/ships", json={
        "affiliation": "Affiliation", "crew": "BAD", "length": False, "model": "Model", "ship_class": "Class", "roles": ["Role1", "Role2"], "category": "Category", "manufacturer": "Manufacturer"
    })
    assert r.status_code == 400
    assert r.is_json
    ship = r.get_json()
    assert "message" in ship
    assert "crew" in ship["message"]
    assert "length" in ship["message"]
    assert ship["message"]["crew"][0] == "Not a valid integer."
    assert ship["message"]["length"][0] == "Not a valid integer."


def test_create_ship_fails_if_data_contains_id(client):
    r = client.post("/api/ships", json={
        "id": 1, "affiliation": "Affiliation", "crew": 1, "length": 1, "model": "Model", "ship_class": "Class", "roles": ["Role1", "Role2"], "category": "Category", "manufacturer": "Manufacturer"
    })
    assert r.status_code == 400
