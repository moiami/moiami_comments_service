import pytest
from src.main import init_app
from src.core.config import config
from src.core.db import db as _db


@pytest.fixture
def client():
    original_uri = config.SQLALCHEMY_DATABASE_URI
    config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    app = init_app()
    app.config["TESTING"] = True

    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.session.remove()
        _db.drop_all()

    config.SQLALCHEMY_DATABASE_URI = original_uri
