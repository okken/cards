from click.testing import CliRunner
import pytest
import pathlib
import cards.cli


@pytest.fixture()
def db_empty(tmpdir, monkeypatch):
    fake_home = pathlib.Path(str(tmpdir.mkdir('fake_home')))

    class FakePathLibPath():
        def home(self):
            return fake_home

    monkeypatch.setattr(cards.cli.pathlib, 'Path', FakePathLibPath)


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def db_non_empty(db_empty, runner):
    runner.invoke(cards.cli.cards_cli, ['add', 'first item'])
    runner.invoke(cards.cli.cards_cli, ['add', 'second item'])
    runner.invoke(cards.cli.cards_cli, ['add', 'third item'])
