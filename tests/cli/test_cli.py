# -*- coding: utf-8 -*-
"""
Tests using cards CLI (command line interface).
This file contains tracer bullet tests.
Not in depth tests of functionality.
"""

import cards.cli


def test_add(db_empty, runner):
    # GIVEN an empty database
    # WHEN a new card is added
    runner.invoke(cards.cli.cards_cli, ['add', 'something'])

    # THEN The listing returns just the new card
    result = runner.invoke(cards.cli.cards_cli, ['list'])
    expected_output = ("  ID      owner  done summary\n"
                       "  --      -----  ---- -------\n"
                       "   1                  something\n")
    assert expected_output == result.output


def test_list(db_empty, runner):
    # GIVEN a db with known contents of 2 cards
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # `cards list` returns our 2 cards
    result = runner.invoke(cards.cli.cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   1                  one\n"
                "   2                  two\n")
    assert expected == result.output


def test_count(db_empty, runner):
    # GIVEN a db with 2 cards
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # `cards count` returns 2
    result = runner.invoke(cards.cli.cards_cli, ['count'])
    expected = "2\n"
    assert expected == result.output


# this test was annoying to write. parsing list output is yucky
def test_update(db_non_empty, runner):
    # GIVEN a card known to be in the db
    result = runner.invoke(cards.cli.cards_cli, ['list'])

    # this is kinda tricky
    last_item_as_list = result.output.split('\n')[-2].split()
    orig_id = last_item_as_list[0]
    orig_summary = ' '.join(last_item_as_list[1:])

    # WHEN we `cards update` the card with new info
    runner.invoke(cards.cli.cards_cli,
                  ['update', '-o', 'okken', '-d', 'True', orig_id])

    # THEN `cards list` will show the changes
    result = runner.invoke(cards.cli.cards_cli, ['list'])
    last_item_as_list = result.output.split('\n')[-2].split()
    id = last_item_as_list[0]
    owner = last_item_as_list[1]
    done = last_item_as_list[2]
    summary = ' '.join(last_item_as_list[3:])
    assert orig_id == id
    assert owner == 'okken'
    assert done == 'x'
    assert orig_summary == summary


def test_delete(db_empty, runner):
    # GIVEN a db with 2 items
    runner.invoke(cards.cli.cards_cli, ['add', 'one'])
    runner.invoke(cards.cli.cards_cli, ['add', 'two'])

    # WHEN we delete one item
    # hoping ids always start with 1
    runner.invoke(cards.cli.cards_cli, ['delete', '1'])

    # THEN the other card remains in the db
    result = runner.invoke(cards.cli.cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   2                  two\n")
    assert expected == result.output
