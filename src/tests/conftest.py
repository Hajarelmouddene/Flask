import pytest

from src import create_app, db
from src.api.models import User

# define test_app and test_database fixture
# fixtures are reusable objects for tests. Scope is associated to a given fixture and indicated how often
# the fixture is invoked (module = once per test module)


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("src.config.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def test_database():
    # test db setup
    db.create_all()
    yield db
    # test db teardown
    db.session.remove()
    db.drop_all()


# Because we have to add a few users to test get all users, we can add a fixture that uses the factory
# as fixture pattern. See pytest documentation. The factory as fixture pattern helps where the result of
# a fixture is needed many times in a single test. Instead of returning data directly, the fixture instead
# returns a function which generates the data.


@pytest.fixture(scope="function")
def add_user():
    def _add_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user
