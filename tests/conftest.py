import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        yield client
