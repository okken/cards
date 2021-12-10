"""
Test Cases
* `list` from an empty database
* `list` from a non-empty database
"""
import pytest
from cards import Card

def test_list_no_cards(cards_db):
    """Empty db, empty list"""
    assert cards_db.list_cards() == []


def test_list_several_cards(cards_db):
    """"
    Given a variety of cards, make sure they get returned.
    """
    orig = [
        Card("foo"),
        Card("bar", owner="me"),
        Card("baz", owner="you", state="in prog"),
    ]

    for c in orig:
        cards_db.add_card(c)

    the_list = cards_db.list_cards()

    assert len(the_list) == len(orig)
    for c in orig:
        assert c in the_list

# list filter
# - no owner
# - specific owner
# - specific state
# - owner and state

@pytest.fixture()
def known_set():
    return [Card(summary="zero", owner="Brian", state="todo"),
            Card(summary="one", owner="Brian", state="in prog"),
            Card(summary="two", owner="Brian", state="done"),

            Card(summary="three", owner="Okken", state="todo"),
            Card(summary="four", owner="Okken", state="in prog"),
            Card(summary="five", owner="Okken", state="done"),

            Card(summary="six", state="todo"),
            Card(summary="seven", state="in prog"),
            Card(summary="eight", state="done")]

@pytest.fixture()
def db_filled(cards_db, known_set):
    for c in known_set:
        cards_db.add_card(c)
    return cards_db

@pytest.mark.parametrize('owner_, state_, expected_indices', [
    ("", None, (6, 7, 8)),
    ("Brian", None, (0, 1, 2)),
    ("Okken", None, (3, 4, 5)),
    (None, "todo", (0, 3, 6)),
    (None, "in prog", (1, 4, 7)),
    (None, "done", (2, 5, 8)),
    ("Brian", "todo", (0,)),
], ids=str)
def test_list_filter(db_filled, known_set, owner_, state_, expected_indices):
    result = db_filled.list_cards(owner=owner_, state=state_)
    assert len(result) == len(expected_indices)
    for i in expected_indices:
        assert known_set[i] in result

