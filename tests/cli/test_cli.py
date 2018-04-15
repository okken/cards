# -*- coding: utf-8 -*-
"""
Tests using cards CLI (command line interface).
This file contains tracer bullet tests.
Not in depth tests of functionality.
"""

import pytest
import cards.cli


pytestmark = pytest.mark.cli


def _detabulate_output(output):
    """
    Turn a tabulate output into a tuple of headers and rows
    assuming the output was formatted in the "jira" style
    """
    lines = output.split('\n')
    headers = lines[0].split('||')
    headers = [header.strip() for header in headers[1:-1]]
    values = [[item.strip() for item in row.split('|')[1:-1]] for row in lines[1:]]
    return headers, values


@pytest.mark.smoke
def test_add(db_empty, runner):
    # GIVEN an empty database
    # WHEN a new card is added
    runner.invoke(cards.cli.cards_cli, ['add', 'something'])

    # THEN The listing returns just the new card
    result = runner.invoke(cards.cli.cards_cli, ['list', '--tableformat=jira'])
    headers, items = _detabulate_output(result.output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][3] == 'something'


@pytest.mark.smoke
def test_list(db_empty, runner):
    # GIVEN a db with known contents of 2 cards
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # `cards list` returns our 2 cards
    result = runner.invoke(cards.cli.cards_cli, ['list', '--tableformat=jira'])
    headers, items = _detabulate_output(result.output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][0] == '1'
    assert items[0][3] == 'one'
    assert items[1][0] == '2'
    assert items[1][3] == 'two'


@pytest.mark.smoke
def test_list_filter(db_empty, runner):
    # GIVEN
    #  two items owned by okken, one that is done
    #  two items with no owner, one that is done
    runner.invoke(cards.cli.cards_cli, ['add', '-o', 'okken', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', '-o', 'anyone', 'two'])
    runner.invoke(cards.cli.cards_cli, ['add', '-o', 'okken', 'three'])
    runner.invoke(cards.cli.cards_cli, ['add', 'four'])
    runner.invoke(cards.cli.cards_cli, ['add', 'five'])

    runner.invoke(cards.cli.cards_cli, ['update', '3', '-d', 'True'])
    runner.invoke(cards.cli.cards_cli, ['update', '4', '-d', 'True'])

    # `cards --noowner -o okken -d True` should return two items
    result = runner.invoke(cards.cli.cards_cli,
                           ['list', '--noowner', '-o', 'okken', '-d', 'True', '--tableformat=jira'])
    headers, items = _detabulate_output(result.output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][0] == '3'
    assert items[0][3] == 'three'
    assert items[1][0] == '4'
    assert items[1][3] == 'four'


@pytest.mark.smoke
def test_count(db_empty, runner):
    # GIVEN a db with 2 cards
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # `cards count` returns 2
    result = runner.invoke(cards.cli.cards_cli, ['count'])
    expected = "2\n"
    assert expected == result.output


# this test was annoying to write. parsing list output is yucky
@pytest.mark.smoke
def test_update(db_non_empty, runner):
    # GIVEN a card known to be in the db
    result = runner.invoke(cards.cli.cards_cli, ['list', '--tableformat=ijra'])

    # this is kinda tricky
    last_item_as_list = result.output.split('\n')[-2].split()
    orig_id = last_item_as_list[0]
    orig_summary = ' '.join(last_item_as_list[1:])

    # WHEN we `cards update` the card with new info
    runner.invoke(cards.cli.cards_cli,
                  ['update', '-o', 'okken', '-d', 'True', orig_id])

    # THEN `cards list` will show the changes
    result = runner.invoke(cards.cli.cards_cli, ['list', '--tableformat=jira'])
    last_item_as_list = result.output.split('\n')[-2].split()
    id = last_item_as_list[0]
    owner = last_item_as_list[1]
    done = last_item_as_list[2]
    summary = ' '.join(last_item_as_list[3:])
    assert orig_id == id
    assert owner == 'okken'
    assert done == 'x'
    assert orig_summary == summary


@pytest.mark.smoke
def test_delete(db_empty, runner):
    # GIVEN a db with 2 items
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # WHEN we delete one item
    # hoping ids always start with 1
    runner.invoke(cards.cli.cards_cli, ['delete', '1'])

    # THEN the other card remains in the db
    result = runner.invoke(cards.cli.cards_cli, ['list', '--tableformat=jira'])
    headers, items = _detabulate_output(result.output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][0] == '2'
    assert items[0][3] == 'two'
