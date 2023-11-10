"""
Test Cases
* `add` to an empty database, with summary
* `add` to a non-empty database, with summary
* `add` a card with both summary and owner set
* `add` a card with a missing summary
* `add` a duplicate card
"""
import pytest
from cards import Card, MissingSummary


def test_add_from_empty(cards_db):
    """
    count should be 1 and card retrievable
    """
    c = Card(summary="do something")
    i = cards_db.add_card(c)
    assert cards_db.count() == 1
    assert cards_db.get_card(i) == c


def test_add_from_nonempty(cards_db_three_cards):
    """
    count should increase by 1 and card retrievable
    """
    cards_db = cards_db_three_cards
    c = Card(summary="do something")
    starting_count = cards_db.count()
    i = cards_db.add_card(c)
    assert cards_db.count() == starting_count + 1
    assert cards_db.get_card(i) == c


def test_add_with_summary_and_owner(cards_db):
    """
    count should be 1 and card retrievable
    """
    c = Card(summary="do something", owner="Brian")
    i = cards_db.add_card(c)
    assert cards_db.count() == 1
    assert cards_db.get_card(i) == c


def test_add_missing_summary(cards_db):
    """
    Should raise an exception
    """
    c = Card()
    with pytest.raises(MissingSummary):
        cards_db.add_card(c)


def test_add_duplicate(cards_db):
    """
    Duplicates allowed, both retrievable, separate indices
    """
    c = Card(summary="do something")
    i_1 = cards_db.add_card(c)
    i_2 = cards_db.add_card(c)
    c1 = cards_db.get_card(i_1)
    c2 = cards_db.get_card(i_2)
    assert i_1 != i_2
    assert c1 == c2 == c
