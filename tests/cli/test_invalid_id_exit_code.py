"""Invalid card id must exit nonzero, not just print an error."""

import shlex

import pytest
from typer.testing import CliRunner

from cards.cli import app

runner = CliRunner()


@pytest.mark.parametrize(
    "command",
    ["delete 25", "start 25", "finish 25", "update 25 -s foo -o brian"],
)
def test_invalid_card_id_exits_nonzero(tmp_path, monkeypatch, command):
    monkeypatch.setenv("CARDS_DB_DIR", str(tmp_path))
    result = runner.invoke(app, shlex.split(command))
    assert "Error: Invalid card id 25" in result.stdout
    assert result.exit_code == 1
