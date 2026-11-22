"""
Test Cases
* a new card is on the Sooner list (later is None) unless added as later
* `later` and `sooner` move a card without touching its other fields
* moving an invalid id
"""
import pytest
from cards import Card, InvalidCardId


def test_new_card_is_sooner(cards_db):
    i = cards_db.add_card(Card("foo"))
    assert cards_db.get_card(i).later is None


def test_add_later(cards_db):
    i = cards_db.add_card(Card("foo", later=True))
    assert cards_db.get_card(i).later is True


@pytest.mark.parametrize("state", ("todo", "in prog", "blocked", "done"))
def test_later_and_sooner_keep_state(cards_db, state):
    i = cards_db.add_card(Card("foo", owner="Brian", state=state, details="notes"))
    cards_db.later(i)
    assert cards_db.get_card(i) == Card("foo", "Brian", state, "notes", later=True)
    cards_db.sooner(i)
    assert cards_db.get_card(i) == Card("foo", "Brian", state, "notes")


@pytest.mark.parametrize("move", ("later", "sooner"))
def test_move_non_existent(cards_db, move):
    with pytest.raises(InvalidCardId):
        getattr(cards_db, move)(123)
