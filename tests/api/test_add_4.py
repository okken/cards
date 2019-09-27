import cards
import pytest
from cards import Card


@pytest.fixture(params=[
    Card('first task', 'brian', False),
    Card(),
    Card(summary='do something'),
    Card(owner='brian'),
    Card(done=True)], ids=repr)
def a_card(request):
    return request.param

def test_add(empty_db, a_card):
    id = cards.add_card(a_card)
    c2 = cards.get_card(id)
    assert a_card == c2

