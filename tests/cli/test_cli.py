# -*- coding: utf-8 -*-
"""
Tests using cards CLI (command line interface).
This file contains tracer bullet tests.
Not in depth tests of functionality.
"""

import pytest
import cards.cli
from cards import Card
from . import detabulate_output

pytestmark = [pytest.mark.cli, pytest.mark.smoke]


def test_add(db_empty, cards_cli):
    # GIVEN an empty database
    # WHEN a new card is added
    cards_cli('add something')

    # THEN The listing returns just the new card
    output = cards_cli('list --format=jira')
    headers, items = detabulate_output(output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][3] == 'something'


def test_list(db_empty, cards_cli):
    # GIVEN a db with known contents of 2 cards
    cards_cli('add one')
    cards_cli('add two')

    # `cards list` returns our 2 cards
    output = cards_cli('list --format=jira')
    headers, items = detabulate_output(output)
    assert headers == ['ID', 'owner', 'done', 'summary']
    assert items[0][0] == '1'
    assert items[0][3] == 'one'
    assert items[1][0] == '2'
    assert items[1][3] == 'two'


def test_list_filter(db_empty, cards_cli):
    # GIVEN
    #  two items owned by okken, one that is done
    #  two items with no owner, one that is done
    cards_cli('add -o okken one')
    cards_cli('add -o anyone two')
    cards_cli('add -o okken three')
    cards_cli('add four')
    cards_cli('add five')
    cards_cli('update 3 -d True')
    cards_cli('update 4 -d True')

    # `cards --noowner -o okken -d True` should return two items
    output = cards_cli('list --noowner -o okken -d True --format=jira')
    headers, items = detabulate_output(output)
    assert [['3', 'okken', 'x', 'three'],
            ['4', ''     , 'x', 'four' ]] == items  # noqa:E202,E203


def test_count(db_empty, runner):
    # GIVEN a db with 2 cards
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # `cards count` returns 2
    result = runner.invoke(cards.cli.cards_cli, ['count'])
    expected = "2\n"
    assert expected == result.output


def packed_line_to_card(line):
    card_id, owner, done, summary = line.split(maxsplit=3)
    return Card(summary, owner, done == 'x', int(card_id))


def packed_output_to_cards(list_output):
    return [packed_line_to_card(line) for line in list_output.split('\n')]


@pytest.fixture()
def db_non_empty_no_okken_no_done(db_non_empty, cards_cli):
    output = cards_cli('list --format=packed')
    for card in packed_output_to_cards(output):
        assert card.owner != 'okken'
        assert not card.done


# this test would be easier if we add an id search parameter to list
def test_update(db_non_empty_no_okken_no_done, cards_cli):
    # GIVEN a card known to be in the db
    output = cards_cli('list --format=packed')
    old_cards = packed_output_to_cards(output)

    # WHEN we `cards update` the card with new info
    cards_cli(f'update -o okken -d True {old_cards[1].id}')

    # THEN `cards list` will show the changes
    new_output = cards_cli('list --format=packed')
    new_cards = packed_output_to_cards(new_output)

    assert old_cards[1].id == new_cards[1].id
    assert 'okken' == new_cards[1].owner
    assert new_cards[1].done


def test_delete(db_empty, cards_cli):
    # GIVEN a db with 2 items
    cards_cli('add one')
    cards_cli('add two')

    # WHEN we delete one item
    # hoping ids always start with 1
    cards_cli('delete 1')

    # THEN the other card remains in the db
    output = cards_cli('list --format=packed')
    assert '2 unassigned o two' == output
