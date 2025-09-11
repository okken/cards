import shlex

from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def cards_cli_out_err(command_string):
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    stderr = result.stderr.rstrip()
    return output, stderr


def cards_cli(command_string):
    output, _ = cards_cli_out_err(command_string)
    return output
