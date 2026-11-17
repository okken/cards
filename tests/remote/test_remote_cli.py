"""
The CLI uses the web app when CARDS_URL is set.
"""
import shlex

import pytest
from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def run(command_string, input=None):
    result = runner.invoke(app, shlex.split(command_string), input=input)
    return result.exit_code, result.stdout


def test_add_and_list(remote_env):
    run("add some task -o anna")
    code, out = run("list")
    assert code == 0
    assert "some task" in out
    assert "Anna Smith" in out


def test_config_shows_web_app(remote_env):
    assert run("config")[1].strip() == "http://cards.test (team: sox)"


def test_count(remote_env):
    run("add one")
    run("add two")
    assert run("count")[1].strip() == "2"


def test_start_finish(remote_env):
    run("add work")
    run("start 1")
    assert remote_env.cards[1]["state"] == "in prog"
    run("finish 1")
    assert remote_env.cards[1]["state"] == "done"


def test_invalid_id(remote_env):
    assert run("start 99")[1].strip() == "Error: Invalid card id 99"


def test_owner_typo_confirmed(remote_env):
    code, out = run("add some task -o brain", input="y\n")
    assert code == 0
    assert "Did you mean Brian Okken (brian@pythontest.com)?" in out
    assert remote_env.cards[1]["owner"] == "brian@pythontest.com"


def test_owner_typo_declined(remote_env):
    code, out = run("add some task -o brain", input="n\n")
    assert code == 1
    assert remote_env.cards == {}


def test_owner_ambiguous_pick_from_list(remote_env):
    code, out = run("add some task -o ann", input="2\n")
    assert code == 0
    assert "1: Anna Smith (anna@example.com)" in out
    assert "2: Anne Jones (anne@example.com)" in out
    assert remote_env.cards[1]["owner"] == "anne@example.com"


def test_owner_ambiguous_cancel(remote_env):
    code, _ = run("add some task -o ann", input="0\n")
    assert code == 1
    assert remote_env.cards == {}


def test_owner_no_match(remote_env):
    code, out = run("add some task -o zzzz")
    assert code == 1
    assert "doesn't match" in out


def test_update_owner_typo(remote_env):
    run("add some task")
    code, _ = run("update 1 -o brain", input="y\n")
    assert code == 0
    assert remote_env.cards[1]["owner"] == "brian@pythontest.com"


def test_list_owner_typo(remote_env):
    run("add mine -o me")
    code, out = run("list -o brain", input="y\n")
    assert code == 0
    assert "mine" in out


def test_not_allowed(remote_env):
    remote_env.status_override = 403
    code, out = run("count")
    assert code == 1
    assert "Error: Not allowed" in out


@pytest.mark.parametrize("missing", ["CARDS_TEAM", "CARDS_API_KEY"])
def test_needs_team_and_key(remote_env, monkeypatch, missing):
    monkeypatch.delenv(missing)
    code, out = run("list")
    assert code == 1
    assert "CARDS_TEAM and CARDS_API_KEY" in out


def test_block(remote_env):
    run("add work")
    run("block 1")
    assert remote_env.cards[1]["state"] == "blocked"


def test_details_show_and_edit(remote_env, monkeypatch):
    run("add noted")
    assert "(no details)" in run("details 1")[1]
    monkeypatch.setattr("typer.edit", lambda text: "some **markdown**\n")
    run("details 1 --edit")
    assert remote_env.cards[1]["details"] == "some **markdown**"
    code, out = run("list")
    assert "noted *" in out
    assert "some **markdown**" in run("details 1")[1]


def test_later_and_sooner(remote_env):
    run("add soon")
    run("add someday --later")
    assert remote_env.cards[2]["later"] is True
    code, out = run("list")
    assert "soon" in out and "someday" not in out
    assert "1 more on the Later list" in out
    run("later 1")
    assert remote_env.cards[1]["later"] is True
    run("sooner 2")
    assert remote_env.cards[2]["later"] is False
    assert "someday" in run("list")[1]
