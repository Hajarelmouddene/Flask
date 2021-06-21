import pytest

from src import create_app, db

# define test_app and test_database fixture
# fixtures are reusable objects for tests. Scope is associated to a given fixture and indicated how often
# the fixture is invoked (module = once per test module)
@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def test_database():
    # test db setup
    db.create_all()
    yield db
    # test db teardown
    db.session.remove()
    db.drop_all()

