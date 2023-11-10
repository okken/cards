import cards
import pytest

from cards_cli_helper import cards_cli


@pytest.fixture(autouse=True)
def patch_db_for_cards_cli(tmp_db_path, monkeypatch):
    """Make the CLI use the temporary directory"""
    monkeypatch.setenv("CARDS_DB_DIR", str(tmp_db_path))


def test_version():
    assert cards_cli("version") == cards.__version__


def test_config(tmp_db_path, cards_db):
    assert cards_cli("config") == str(tmp_db_path)


def test_config_normal_path(tmp_db_path, monkeypatch):
    """Undo the autouse fixture, for just this test."""
    monkeypatch.delenv("CARDS_DB_DIR")
    assert cards_cli("config") != str(tmp_db_path)


def test_count(cards_db_three_cards):
    assert cards_cli("count") == "3"


def test_start(cards_db):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"start {i}")
    after = cards_db.get_card(i)
    assert after.state == "in prog"


def test_finish(cards_db):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"finish {i}")
    after = cards_db.get_card(i)
    assert after.state == "done"


def test_add(cards_db):
    cards_cli("add some task")
    expected = cards.Card("some task", owner="", state="todo")
    all_cards = cards_db.list_cards()
    assert len(all_cards) == 1
    assert all_cards[0] == expected


def test_add_with_owner(cards_db):
    """
    A card shows up in the list with expected contents.
    """
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    all_cards = cards_db.list_cards()
    assert len(all_cards) == 1
    assert all_cards[0] == expected


def test_delete(cards_db):
    i = cards_db.add_card(cards.Card("foo"))
    cards_cli(f"delete {i}")
    assert cards_db.count() == 0


def test_update(cards_db):
    i = cards_db.add_card(cards.Card("foo"))
    cards_cli(f"update {i} -o okken -s something")
    expected = cards.Card("something", owner="okken", state="todo")
    actual = cards_db.get_card(i)
    assert actual == expected


expected_output = """\

  ID   state   owner   summary    
 ──────────────────────────────── 
  1    todo            some task  
  2    todo            another
"""


def test_list(cards_db):
    cards_db.add_card(cards.Card("some task"))
    cards_db.add_card(cards.Card("another"))
    output = cards_cli("list")
    assert output.strip() == expected_output.strip()


def test_main(cards_db):
    cards_db.add_card(cards.Card("some task"))
    cards_db.add_card(cards.Card("another"))
    output = cards_cli("")
    assert output.strip() == expected_output.strip()


# Error cases


@pytest.mark.parametrize(
    "command",
    ["delete 25", "start 25", "finish 25", "update 25 -s foo -o brian"],
)
def test_invalid_card_id(cards_db, command):
    out = cards_cli(command)
    assert out == "Error: Invalid card id 25"


def test_missing_summary(cards_db):
    out = cards_cli("add")
    assert "Error" in out
    assert "Missing argument 'SUMMARY...'" in out
