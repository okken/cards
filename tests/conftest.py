import cards
import pytest
from cards import Card


@pytest.fixture(scope="session")
def tmp_db_path(tmp_path_factory):
    """Path to temporary database"""
    return tmp_path_factory.mktemp("cards_db")


@pytest.fixture(scope="session")
def session_cards_db(tmp_db_path):
    """CardsDB"""
    db_ = cards.CardsDB(tmp_db_path)
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db(session_cards_db):
    """Empty CardsDB"""
    db = session_cards_db
    db.delete_all()
    return db


@pytest.fixture(scope="function")
def cards_db_three_cards(cards_db):
    """CardsDB with 3 cards"""
    cards_db.add_card(Card("foo"))
    cards_db.add_card(Card("bar"))
    cards_db.add_card(Card("baz"))
    return cards_db
