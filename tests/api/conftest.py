import pytest
import cards

@pytest.fixture(scope='session')
def db(tmp_path_factory):
    d = tmp_path_factory.mktemp('cards_db')
    cards.set_db_path(d)
    cards.connect()
    yield
    cards.disconnect()


@pytest.fixture(scope='function')
def empty_db(db):
    cards.delete_all()
