import pytest

from server import create_app, database

app = create_app()
app.app_context().push()


@pytest.fixture(scope='session')
def test_client():
    return app.test_client()


@pytest.fixture
def init_db():
    database.init_db()


@pytest.fixture
def seed_db(init_db):
    database.seed_db()
