"""
Test Cases
* a new card has no details (None) unless given some
* details can be updated without touching other fields
"""
from cards import Card


def test_details_default_empty(cards_db):
    i = cards_db.add_card(Card("foo"))
    assert cards_db.get_card(i).details is None


def test_add_with_details(cards_db):
    i = cards_db.add_card(Card("foo", details="line 1\nline 2"))
    assert cards_db.get_card(i).details == "line 1\nline 2"


def test_update_details_only(cards_db):
    i = cards_db.add_card(Card("foo", owner="Brian", details="old"))
    cards_db.update_card(i, Card(details="new", state=None))
    card = cards_db.get_card(i)
    assert (card.summary, card.owner, card.state, card.details) == ("foo", "Brian", "todo", "new")


def test_clear_details(cards_db):
    i = cards_db.add_card(Card("foo", details="old"))
    cards_db.update_card(i, Card(details="", state=None))
    assert cards_db.get_card(i).details is None
