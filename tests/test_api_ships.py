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
