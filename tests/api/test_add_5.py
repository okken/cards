import cards
import pytest
from cards import Card


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

# @dataclass
# class Card:
#     summary: str = None
#     owner: str = None
#     done: bool = None
#     id: int = field(default=None, compare=False)

@pytest.fixture(params=[
    Card('first task', 'brian', False),
    Card(),
    Card(None, None, None),
    Card(summary='do something'),
    Card(owner='brian'),
    Card(done=True),
    Card('do something', 'Brian', True),
    Card('Something Else', 'Okken', False)],
    ids=repr)
def a_card(request):
    return request.param

def test_add(empty_db, a_card):
    id = cards.add_card(a_card)
    c2 = cards.get_card(id)
    assert a_card == c2

