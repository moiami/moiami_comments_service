import pytest
from src.main import init_app

@pytest.fixture
def client():
    app = init_app()

    with app.app_context():
        yield app.test_client()