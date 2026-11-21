import cards
import pytest

from cards.cli import app

from .cards_cli_helper import cards_cli, cards_cli_out_err, runner


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


def test_delete_asks_first(cards_db):
    i = cards_db.add_card(cards.Card("foo"))
    result = runner.invoke(app, ["delete", str(i)], input="y\n")
    assert f"Delete card {i}: foo? [y/N]" in result.stdout
    assert cards_db.count() == 0


@pytest.mark.parametrize("answer", ["n\n", "\n"])
def test_delete_keeps_card_unless_yes(cards_db, answer):
    i = cards_db.add_card(cards.Card("foo"))
    result = runner.invoke(app, ["delete", str(i)], input=answer)
    assert "Not deleted." in result.stdout
    assert cards_db.count() == 1


@pytest.mark.parametrize("flag", ["-y", "--yes"])
def test_delete_yes_skips_question(cards_db, flag):
    i = cards_db.add_card(cards.Card("foo"))
    out = cards_cli(f"delete {i} {flag}")
    assert "?" not in out
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
    out, err = cards_cli_out_err("add")
    assert "Error" in err
    assert "Missing argument 'SUMMARY...'" in err


def test_block(cards_db):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"block {i}")
    assert cards_db.get_card(i).state == "blocked"


def test_list_marks_cards_with_details(cards_db):
    cards_db.add_card(cards.Card("plain"))
    cards_db.add_card(cards.Card("noted", details="more info"))
    out = cards_cli("list")
    assert "noted *" in out
    assert "plain *" not in out
    assert "* has details: cards details ID" in out


def test_list_no_marker_note_without_details(cards_db):
    cards_db.add_card(cards.Card("plain"))
    assert "has details" not in cards_cli("list")


def test_details_show(cards_db):
    i = cards_db.add_card(cards.Card("noted", details="line 1\nline 2"))
    assert cards_cli(f"details {i}") == f"{i}: noted\n\nline 1\nline 2"


def test_details_show_empty(cards_db):
    i = cards_db.add_card(cards.Card("plain"))
    assert cards_cli(f"details {i}") == f"{i}: plain\n\n(no details)"


def test_details_edit(cards_db, monkeypatch):
    i = cards_db.add_card(cards.Card("noted", details="old"))
    monkeypatch.setattr("typer.edit", lambda text: text.replace("old", "new") + "\n")
    cards_cli(f"details {i} --edit")
    assert cards_db.get_card(i).details == "new"


def test_details_edit_unchanged(cards_db, monkeypatch):
    i = cards_db.add_card(cards.Card("noted", details="old"))
    monkeypatch.setattr("typer.edit", lambda text: None)
    assert cards_cli(f"details {i} --edit") == "No changes."
    assert cards_db.get_card(i).details == "old"


def test_details_invalid_id(cards_db):
    assert cards_cli("details 99") == "Error: Invalid card id 99"


def test_list_shows_sooner_with_later_note(cards_db):
    cards_db.add_card(cards.Card("soon"))
    cards_db.add_card(cards.Card("someday", later=True))
    out = cards_cli("list")
    assert "soon" in out and "someday" not in out
    assert "1 more on the Later list: cards list --later" in out


def test_list_later(cards_db):
    cards_db.add_card(cards.Card("soon"))
    cards_db.add_card(cards.Card("someday", later=True))
    out = cards_cli("list --later")
    assert "someday" in out and "soon\n" not in out and "more on the Later list" not in out


def test_list_all_shows_list_column(cards_db):
    cards_db.add_card(cards.Card("soon"))
    cards_db.add_card(cards.Card("someday", later=True))
    out = cards_cli("list --all")
    assert "list" in out and "sooner" in out and "later" in out and "someday" in out


def test_add_later(cards_db):
    cards_cli("add parked --later")
    assert cards_db.list_cards()[0].later is True


def test_later_and_sooner(cards_db):
    i = cards_db.add_card(cards.Card("foo"))
    cards_cli(f"later {i}")
    assert cards_db.get_card(i).later is True
    cards_cli(f"sooner {i}")
    assert cards_db.get_card(i).later is None


def test_later_invalid_id(cards_db):
    assert cards_cli("later 99") == "Error: Invalid card id 99"


def test_list_hides_done_by_default(cards_db):
    cards_db.add_card(cards.Card("open one"))
    cards_db.add_card(cards.Card("finished one", state="done"))
    for command in ("", "list", "list -s open"):
        out = cards_cli(command)
        assert "open one" in out and "finished one" not in out, command
    out = cards_cli("list -s all")
    assert "open one" in out and "finished one" in out
    out = cards_cli("list -s done")
    assert "open one" not in out and "finished one" in out


def test_later_note_counts_open_cards_only(cards_db):
    cards_db.add_card(cards.Card("parked", later=True))
    cards_db.add_card(cards.Card("parked and done", state="done", later=True))
    assert "1 more on the Later list" in cards_cli("list")


def test_add_with_details(cards_db, monkeypatch):
    monkeypatch.setattr("typer.edit", lambda text: "some notes\n")
    cards_cli("add noted -d")
    assert cards_db.list_cards()[0].details == "some notes"


def test_add_with_details_editor_closed(cards_db, monkeypatch):
    monkeypatch.setattr("typer.edit", lambda text: None)
    cards_cli("add plain --details")
    card = cards_db.list_cards()[0]
    assert (card.summary, card.details) == ("plain", None)


@pytest.mark.parametrize("command", ["list -p web", "add thing -p web", "projects", "projects add web"])
def test_projects_need_the_web_app(cards_db, command):
    assert cards_cli(command) == "Error: projects need the web app (set CARDS_URL)."


def test_cards_project_env_is_ignored_locally(cards_db, monkeypatch):
    monkeypatch.setenv("CARDS_PROJECT", "web")
    cards_cli("add thing")
    assert "thing" in cards_cli("list")
