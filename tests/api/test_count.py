"""
Test Cases
* `count` from an empty database
* `count` with one item
* `count` with more than one item
"""
from cards import Card


def test_count_no_cards(cards_db):
    assert cards_db.count() == 0


def test_count_one_card(cards_db):
    cards_db.add_card(Card("foo"))
    assert cards_db.count() == 1


def test_count_three_cards(cards_db_three_cards):
    cards_db = cards_db_three_cards
    assert cards_db.count() == 3
