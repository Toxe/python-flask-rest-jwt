import pytest
from app import create_app


class Authentication:
    def __init__(self, client):
        self.client = client
    def login(self, id=1, username="user", password="password"):
        r = self.client.post("/auth/login", json={"username": username, "password": password})
        if r.status_code != 200:
            raise RuntimeError("Login failed")
        self.id = id
        self.access_token = r.get_json().get("access_token")
        self.refresh_token = r.get_json().get("refresh_token")
        self.headers = {"Authorization": "Bearer {}".format(self.access_token)}


@pytest.fixture
def app():
    app = create_app()
    app.testing = True

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth(client):
    return Authentication(client)
