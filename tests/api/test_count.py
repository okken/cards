"""
Test Cases
* `count` from an empty database
* `count` with one item
* `count` with more than one item
"""
import pytest


def test_count_no_cards(cards_db):
    assert cards_db.count() == 0


@pytest.mark.num_cards(1)
def test_count_one_card(cards_db):
    assert cards_db.count() == 1


@pytest.mark.num_cards(3)
def test_count_three_cards(cards_db):
    assert cards_db.count() == 3
