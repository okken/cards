import pytest


@pytest.mark.parametrize(
    "command",
    ["delete 25", "start 25", "finish 25", "update 25 -s foo -o brian"],
)
def test_invalid_card_id(cards_db, command, cards_cli):
    out = cards_cli(command)
    assert out == "Error: Invalid card id 25"


def test_missing_summary(cards_db, cards_cli):
    out = cards_cli("add")
    assert "Error: Missing argument 'SUMMARY...'" in out
