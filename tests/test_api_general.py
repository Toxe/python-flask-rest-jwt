def test_api_slash_request_forbidden(client):
    assert client.get("/").status_code == 404


def test_api_root_request_forbidden(client):
    assert client.get("/api").status_code == 404
    assert client.get("/api/").status_code == 404
