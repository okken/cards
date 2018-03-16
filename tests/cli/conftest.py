from click.testing import CliRunner
import pytest
import pathlib
import cards.cli


@pytest.fixture()
def mock_cards_db(tmpdir, monkeypatch):
    fake_home = pathlib.Path(str(tmpdir.mkdir('fake_home')))

    class FakePathLibPath():
        def home(self):
            return fake_home

    monkeypatch.setattr(cards.cli.pathlib, 'Path', FakePathLibPath)


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def non_empty_db(mock_cards_db, runner):
    runner.invoke(cards.cli.cards_cli, ['add', 'one item'])
    runner.invoke(cards.cli.cards_cli, ['add', 'second item'])
    runner.invoke(cards.cli.cards_cli, ['add', 'third item'])
