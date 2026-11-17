"""
Projects (web app only): CARDS_PROJECT, -p, and `cards projects`.
"""
import shlex

import pytest
from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def run(command, input=None):
    result = runner.invoke(app, shlex.split(command), input=input)
    return result.exit_code, result.stdout


@pytest.fixture
def two_projects(remote_env):
    remote_env.projects.append("Website")
    run("add general card")
    run("add web card -p website")
    return remote_env


def test_list_shows_default_project(two_projects):
    code, out = run("list")
    assert "Project: General" in out
    assert "general card" in out and "web card" not in out


def test_list_by_flag_and_env(two_projects, monkeypatch):
    out = run("list -p Website")[1]
    assert "Project: Website" in out and "web card" in out and "general card" not in out
    monkeypatch.setenv("CARDS_PROJECT", "website")
    out = run("list")[1]
    assert "web card" in out and "general card" not in out
    # -p beats CARDS_PROJECT
    assert "general card" in run("list -p general")[1]


def test_list_all_projects_has_project_column(two_projects):
    out = run("list -p all")[1]
    assert "Project:" not in out
    assert "project" in out and "Website" in out and "General" in out
    assert "general card" in out and "web card" in out


def test_add_goes_to_env_project(two_projects, monkeypatch):
    monkeypatch.setenv("CARDS_PROJECT", "Website")
    run("add another")
    assert two_projects.cards[3]["project"] == "Website"


def test_card_commands_work_across_projects(two_projects):
    # card 2 is in Website, but needs no project to start it
    run("start 2")
    assert two_projects.cards[2]["state"] == "in prog"


def test_move_card(two_projects):
    run("update 1 -p website")
    assert two_projects.cards[1]["project"] == "Website"


def test_unknown_project(two_projects):
    code, out = run("list -p nope")
    assert code == 1
    assert "No project named 'nope'. Projects: General, Website." in out


def test_projects_list_and_add(two_projects, monkeypatch):
    monkeypatch.setenv("CARDS_PROJECT", "Website")
    run("projects add Docs")
    out = run("projects")[1]
    assert "General" in out and "default" in out
    assert "Website" in out and "CARDS_PROJECT" in out
    assert "Docs" in out
    code, out = run("projects add docs")
    assert code == 1 and "already a project named" in out
