import cards
import pytest
from cards import Card


def test_add(empty_db):
    a_card = Card('first task', 'brian', False)
    id = cards.add_card(a_card)
    c2 = cards.get_card(id)
    assert a_card == c2

