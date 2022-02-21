import pytest
import cards
from cards import Card


@pytest.fixture(scope="session")
def db_path(tmp_path_factory):
    """Path to temporary database"""
    return tmp_path_factory.mktemp("cards_db")


@pytest.fixture(scope="session")
def session_cards_db(db_path):
    """CardsDB"""
    db_ = cards.CardsDB(db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db(session_cards_db, request, faker):
    db = session_cards_db
    db.delete_all()
    # support for `@pytest.mark.num_cards(<some number>)`
    faker.seed_instance(101) # random seed
    m = request.node.get_closest_marker('num_cards')
    if m and len(m.args) > 0:
        num_cards = m.args[0]
        for _ in range(num_cards):
            db.add_card(Card(summary=faker.sentence(),
                             owner=faker.first_name()))
    return db




