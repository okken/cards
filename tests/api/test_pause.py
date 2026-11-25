"""
Test Cases
* `pause` from "todo", "in prog", and "done" states
* `pause` an invalid id
"""
import pytest
from cards import Card, InvalidCardId


@pytest.mark.parametrize("start_state", ("todo", "in prog", "done"))
def test_pause(cards_db, start_state):
    i = cards_db.add_card(Card("foo", state=start_state))
    cards_db.pause(i)
    assert cards_db.get_card(i).state == "paused"


def test_pause_non_existent(cards_db):
    with pytest.raises(InvalidCardId):
        cards_db.pause(123)
