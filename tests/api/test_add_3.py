import cards
import pytest
from cards import Card

# @dataclass
# class Card:
#     summary: str = None
#     owner: str = None
#     done: bool = None
#     id: int = field(default=None, compare=False)

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


def test_add(empty_db):
    c1 = Card('first task', 'brian', False)
    id = cards.add_card(c1)
    c2 = cards.get_card(id)
    assert c1 == c2

