from typer.testing import CliRunner
from cards.cli import app
import cards
import pytest
import shlex


runner = CliRunner()


@pytest.fixture(scope="module")
def db_path(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("cards_db")
    return db_path


@pytest.fixture()
def cards_db(db_path, monkeypatch):
    monkeypatch.setenv("CARDS_DB_DIR", str(db_path))
    db_ = cards.CardsDB(db_path)
    db_.delete_all()
    yield db_
    db_.close()


@pytest.fixture(scope="function")
def cards_db_three_cards(cards_db):
    """CardsDB with 3 cards"""
    cards_db.add_card(cards.Card("foo"))
    cards_db.add_card(cards.Card("bar"))
    cards_db.add_card(cards.Card("baz"))
    return cards_db


def cards_cli(command_string):
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    lines = result.stdout.rstrip().splitlines()
    output = '\n'.join([a_line.rstrip() for a_line in lines])
    return output


def test_version():
    assert cards_cli('version') == cards.__version__


def test_config(db_path, cards_db):
    assert cards_cli("config") == str(db_path)


def test_config_normal_path(db_path):
    assert cards_cli("config") != str(db_path)


def test_count(cards_db_three_cards):
    assert cards_cli('count') == '3'


def test_start(cards_db):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"start {i}")
    after = cards_db.get_card(i)
    assert after.state == 'in prog'


def test_finish(cards_db):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"finish {i}")
    after = cards_db.get_card(i)
    assert after.state == 'done'


def test_add(cards_db):
    cards_cli("add some task")
    expected = cards.Card("some task", owner="", state="todo")
    all = cards_db.list_cards()
    assert len(all) == 1
    assert all[0] == expected


def test_add_with_owner(cards_db):
    """
    A card shows up in the list with expected contents.
    """
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    all = cards_db.list_cards()
    assert len(all) == 1
    assert all[0] == expected


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
     ╷       ╷       ╷
  ID │ state │ owner │ summary
╺━━━━┿━━━━━━━┿━━━━━━━┿━━━━━━━━━━━╸
  1  │ todo  │       │ some task
  2  │ todo  │       │ another
     ╵       ╵       ╵"""


def test_list(cards_db):
    cards_db.add_card(cards.Card("some task"))
    cards_db.add_card(cards.Card("another"))
    output = cards_cli("list")
    assert output == expected_output


def test_main(cards_db):
    cards_db.add_card(cards.Card("some task"))
    cards_db.add_card(cards.Card("another"))
    output = cards_cli("")
    assert output == expected_output


# Error cases


@pytest.mark.parametrize("command", ["delete 25",
                                     "start 25",
                                     "finish 25",
                                     "update 25 -s foo -o brian"])
def test_invalid_card_id(cards_db, command):
    out = cards_cli(command)
    assert out == "Error: Invalid card id 25"


def test_missing_summary(cards_db):
    out = cards_cli("add")
    assert "Error: Missing argument 'SUMMARY...'" in out
