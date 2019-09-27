import click.testing
import pytest
import pathlib
import cards.cards_cli
import shlex


@pytest.fixture()
def db_empty(tmpdir, monkeypatch):
    fake_home = pathlib.Path(str(tmpdir.mkdir('fake_home')))

    class FakePathLibPath():
        def home(self):
            return fake_home

    monkeypatch.setattr(cards.cards_db.pathlib, 'Path', FakePathLibPath)


@pytest.fixture()
def cards_cli():
    runner = click.testing.CliRunner()
    def _invoke_cards(input_string):
        input_list = shlex.split(input_string)
        return runner.invoke(cards.cards_cli.cards_cli, input_list).output.rstrip()
    return _invoke_cards


@pytest.fixture()
def db_non_empty(db_empty, cards_cli):
    cards_cli('add "first item"')
    cards_cli('add "second item"')
    cards_cli('add "third item"')


