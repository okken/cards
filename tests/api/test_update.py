"""
Test Cases
* `update` the owner of a card
* `update` the summary of a card
* `update` owner and summary of a card at the same time
* `update` a non-existent card
"""
import pytest
from cards import Card, InvalidCardId


def test_update_owner(cards_db):
    """
    summary and state should stay the same
    owner should change
    """
    i = cards_db.add_card(Card("foo", owner="me"))
    cards_db.update_card(i, Card(owner="not me", state=None))

    mod = cards_db.get_card(i)
    assert mod == Card("foo", owner="not me")


def test_update_summary(cards_db):
    """
    owner and state should stay the same
    summary should change
    """
    i = cards_db.add_card(Card("foo", owner="me", state="done"))
    cards_db.update_card(i, Card(summary="bar", state=None))

    mod = cards_db.get_card(i)
    assert mod == Card("bar", owner="me", state="done")


def test_update_both(cards_db):
    """
    state should stay the same
    owner and summary should change
    """
    i = cards_db.add_card(Card("foo", owner="me"))
    cards_db.update_card(i, Card(summary="bar", owner="not me"))

    mod = cards_db.get_card(i)
    assert mod == Card("bar", owner="not me", state="todo")


def test_update_non_existent(cards_db):
    """
    Shouldn't be able to update a non-existent card.
    """
    i = 123  # any number will do, db is empty
    with pytest.raises(InvalidCardId):
        cards_db.update_card(i, Card(summary="bar", owner="not me"))
