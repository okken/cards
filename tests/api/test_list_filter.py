"""
Test Cases for list filter
# - specific owner
# - specific state
# - owner and state
"""
import pytest
from cards import Card


@pytest.fixture(scope="module")
def known_set():
    # summary matches index into this list
    return [
        Card(summary="zero", owner="Brian", state="todo"),
        Card(summary="one", owner="Brian", state="in prog"),
        Card(summary="two", owner="Brian", state="done"),
        Card(summary="three", owner="Okken", state="todo"),
        Card(summary="four", owner="Okken", state="in prog"),
        Card(summary="five", owner="Okken", state="done"),
    ]


@pytest.fixture(scope="module")
def db_filled(session_cards_db, known_set):
    cards_db = session_cards_db

    # make sure it's empty
    cards_db.delete_all()

    # then add our known set
    for c in known_set:
        cards_db.add_card(c)
    return cards_db


def test_list_filter_owner(db_filled, known_set):
    """
    Should get cards 3, 4, 5 back:
        Card(summary="three", owner="Okken", state="todo"),
        Card(summary="four", owner="Okken", state="in prog"),
        Card(summary="five", owner="Okken", state="done"),
    """
    result = db_filled.list_cards(owner="Okken")
    assert len(result) == 3
    for i in (3, 4, 5):
        assert known_set[i] in result


def test_list_filter_state(db_filled, known_set):
    """
    Should get cards 1 and 4 back:
        Card(summary="one", owner="Brian", state="in prog"),
        Card(summary="four", owner="Okken", state="in prog"),
    """
    result = db_filled.list_cards(state="in prog")
    assert len(result) == 2
    for i in (1, 4):
        assert known_set[i] in result


def test_list_filter_both(db_filled, known_set):
    """
    Should get just card 2 back:
        Card(summary="two", owner="Brian", state="done"),
    """
    result = db_filled.list_cards(owner="Brian", state="done")
    assert len(result) == 1
    assert result[0] == known_set[2]
