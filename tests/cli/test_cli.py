# -*- coding: utf-8 -*-
"""
Tests using cards CLI (command line interface).
This file contains tracer bullet tests.
Not in depth tests of functionality.
"""

import pytest
import cards.cli
from . import detabulate_output

pytestmark = pytest.mark.cli


@pytest.mark.smoke
def test_add(db_empty, runner):
    # GIVEN an empty database
    # WHEN a new card is added
    runner.invoke(cards.cli.cards_cli, ['add', 'something'])

    # THEN The listing returns just the new card
    result = runner.invoke(cards.cli.cards_cli, ['list', '--format=jira'])
    headers, items = detabulate_output(result.output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][3] == 'something'


@pytest.mark.smoke
def test_list(db_empty, runner):
    # GIVEN a db with known contents of 2 cards
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # `cards list` returns our 2 cards
    result = runner.invoke(cards.cli.cards_cli, ['list', '--format=jira'])
    headers, items = detabulate_output(result.output)
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
                           ['list', '--noowner', '-o', 'okken',
                            '-d', 'True', '--format=jira'])
    headers, items = detabulate_output(result.output)
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
    result = runner.invoke(cards.cli.cards_cli, ['list', '--format=jira'])

    _, orig_items = detabulate_output(result.output)

    # WHEN we `cards update` the card with new info
    runner.invoke(cards.cli.cards_cli,
                  ['update', '-o', 'okken', '-d', 'True', orig_items[1][0]])

    # THEN `cards list` will show the changes
    result = runner.invoke(cards.cli.cards_cli, ['list', '--format=jira'])
    _, new_items = detabulate_output(result.output)
    assert orig_items[1][0] == new_items[1][0]
    assert new_items[1][1] == 'okken'
    assert new_items[1][2] == 'x'
    assert orig_items[1][3] == new_items[1][3]


@pytest.mark.smoke
def test_delete(db_empty, runner):
    # GIVEN a db with 2 items
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # WHEN we delete one item
    # hoping ids always start with 1
    runner.invoke(cards.cli.cards_cli, ['delete', '1'])

    # THEN the other card remains in the db
    result = runner.invoke(cards.cli.cards_cli, ['list', '--format=jira'])
    headers, items = detabulate_output(result.output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][0] == '2'
    assert items[0][3] == 'two'
