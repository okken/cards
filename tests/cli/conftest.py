import pathlib
import shlex
from collections import namedtuple

import cards.cli
import pytest
from cards.cli import app
from typer.testing import CliRunner


@pytest.fixture()
def db_empty(tmpdir, monkeypatch):
    fake_home = pathlib.Path(str(tmpdir.mkdir("fake_home")))

    class FakePathLibPath:
        def home(self):
            return fake_home

    monkeypatch.setattr(cards.cli.pathlib, "Path", FakePathLibPath)


@pytest.fixture()
def cards_cli():
    runner = CliRunner()

    def _invoke_cards(input_string):
        input_list = shlex.split(input_string)
        return runner.invoke(app, input_list).output.rstrip()

    return _invoke_cards


@pytest.fixture()
def db_non_empty(db_empty, cards_cli):
    cards_cli('add "first item"')
    cards_cli('add "second item"')
    cards_cli('add "third item"')


Item = namedtuple("Item", ["id", "owner", "priority", "done", "summary"])


@pytest.fixture()
def cards_cli_list_items():
    """
    Just like cards_cli fixture, with different output.
    Returns detabulated items.
    """

    runner = CliRunner()

    def _invoke_cards(input_string):
        input_list = shlex.split(input_string)
        input_list.append("--format=jira")  # produces easy to parse |'s
        output = runner.invoke(app, input_list).output.rstrip()
        # Turn a tabulate output into a tuple of headers and rows
        # assuming the output was formatted in the "jira" style
        lines = output.split("\n")
        values = [[item.strip() for item in row.split("|")[1:-1]] for row in lines[1:]]
        items = [Item(*v) for v in values]
        return items

    return _invoke_cards
