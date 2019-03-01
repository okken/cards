import click.testing
import pytest
import pathlib
import cards.cli
import shlex
from collections import namedtuple


@pytest.fixture()
def db_empty(tmpdir, monkeypatch):
    fake_home = pathlib.Path(str(tmpdir.mkdir('fake_home')))

    class FakePathLibPath():
        def home(self):
            return fake_home

    monkeypatch.setattr(cards.cli.pathlib, 'Path', FakePathLibPath)


@pytest.fixture()
def runner():
    return click.testing.CliRunner()


@pytest.fixture()
def cards_cli():
    runner = click.testing.CliRunner()

    def _invoke_cards(input_string):
        input_list = shlex.split(input_string)
        return runner.invoke(cards.cli.cards_cli, input_list).output.rstrip()

    return _invoke_cards


@pytest.fixture()
def db_non_empty(db_empty, cards_cli):
    cards_cli('add "first item"')
    cards_cli('add "second item"')
    cards_cli('add "third item"')


Item = namedtuple('Item', ['id', 'owner', 'done', 'summary'])


def items_from_output(output):
    """
    Turn a tabulate output into a tuple of headers and rows
    assuming the output was formatted in the "jira" style
    """
    lines = output.split('\n')
    values = [[item.strip()
               for item in row.split('|')[1:-1]] for row in lines[1:]]
    items = [Item(*v) for v in values]
    return items


@pytest.fixture()
def cards_cli_list_items():
    '''
    Just like cards_cli fixture, with different output.
    Returns detabulated items.
    '''

    runner = click.testing.CliRunner()

    def _invoke_cards(input_string):
        input_list = shlex.split(input_string)
        if 'list' in input_list:
            input_list.append('--format=jira')
        output = runner.invoke(cards.cli.cards_cli, input_list).output.rstrip()
        if 'list' in input_list:
            return items_from_output(output)
        else:
            return output

    return _invoke_cards
