import pytest

from server.database import get_db
from server import create_app, database

app = create_app()
app.app_context().push()


@pytest.fixture(scope='session')
def test_client():
    return app.test_client()


@pytest.fixture
def db():
    return get_db()

@pytest.fixture
def init_db():
    database.init_db()


@pytest.fixture(autouse=True)
def seed_db(init_db):
    database.seed_db()
