from typer.testing import CliRunner
import cards
import pytest
import shlex

runner = CliRunner()

@pytest.fixture()
def cards_cli_no_redirect():
    def run_cli(command_string):
        command_list = shlex.split(command_string)
        result = runner.invoke(cards.cli.app, command_list)
        output = result.stdout.rstrip()
        return output
    return run_cli

@pytest.fixture()
def cards_cli(cards_cli_no_redirect, db_path, monkeypatch, cards_db):
    monkeypatch.setenv("CARDS_DB_DIR", db_path.as_posix())
    return cards_cli_no_redirect
