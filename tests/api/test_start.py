"""
Test Cases
* `start` from "todo", "in prog", and "done" states
* `start` an invalid id
"""
import pytest
from cards import Card, InvalidCardId


@pytest.mark.parametrize("start_state", ("todo", "in prog", "done"))
def test_start(cards_db, start_state):
    """
    End state should be "in prog"
    """
    c = Card("foo", state=start_state)
    i = cards_db.add_card(c)
    cards_db.start(i)
    c = cards_db.get_card(i)
    assert c.state == "in prog"


def test_start_non_existent(cards_db):
    """
    Shouldn't be able to start a non-existent card.
    """
    i = 123  # any number will do, db is empty
    with pytest.raises(InvalidCardId):
        cards_db.start(i)
