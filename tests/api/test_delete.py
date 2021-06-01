"""
Test Cases:
* `delete` one from a database with more than one
* `delete` the last card
* `delete` a non-existent card
"""
import pytest
from cards import Card, InvalidCardId


@pytest.fixture()
def three_cards(cards_db):
    i = cards_db.add_card(Card("foo"))
    j = cards_db.add_card(Card("bar"))
    k = cards_db.add_card(Card("baz"))
    return (i, j, k)  # ids for the cards


def test_delete_from_many(cards_db, three_cards):
    """
    Count should go from 3 to 2
    And card shouldn't be retrievable.
    But the rest should be.
    """
    (i, j, k) = three_cards  # ids
    id_to_delete = j
    ids_still_there = (i, k)

    cards_db.delete_card(id_to_delete)

    assert cards_db.count() == 2
    # card should not be retrievable after deletion
    with pytest.raises(InvalidCardId):
        cards_db.get_card(id_to_delete)
    # non-deleted cards should still be retrievable
    for i in ids_still_there:
        # just making sure this doesn't throw an exception
        cards_db.get_card(i)


def test_delete_last_card(cards_db):
    """
    Count should be back to 0
    And card shouldn't be retrievable.
    """
    i = cards_db.add_card(Card("foo"))
    cards_db.delete_card(i)
    assert cards_db.count() == 0
    with pytest.raises(InvalidCardId):
        cards_db.get_card(i)


def test_delete_non_existent(cards_db):
    """
    Shouldn't be able to start a non-existent card.
    """
    i = 123  # any number will do, db is empty
    with pytest.raises(InvalidCardId):
        cards_db.delete_card(i)
