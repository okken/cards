"""
Test Cases
* `block` from "todo", "in prog", and "done" states
* `block` an invalid id
"""
import pytest
from cards import Card, InvalidCardId


@pytest.mark.parametrize("start_state", ("todo", "in prog", "done"))
def test_block(cards_db, start_state):
    i = cards_db.add_card(Card("foo", state=start_state))
    cards_db.block(i)
    assert cards_db.get_card(i).state == "blocked"


def test_block_non_existent(cards_db):
    with pytest.raises(InvalidCardId):
        cards_db.block(123)
