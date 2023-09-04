import pytest


@pytest.mark.num_cards(3)
def test_count(cards_cli):
    assert cards_cli("count") == "3"
