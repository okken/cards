#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
import cards.cli


def test_add(mock_cards_db):
    runner = CliRunner()
    # GIVEN an empty database
    # WHEN a new card is added
    runner.invoke(cards.cli.cards_cli, ['add', 'something'])

    # THEN The listing returns just the new card
    result = runner.invoke(cards.cli.cards_cli, ['list'])
    expected_output = ("  ID      owner  done summary\n"
                       "  --      -----  ---- -------\n"
                       "   1                  something\n")
    assert result.output == expected_output


def test_list_on_no_command(non_empty_db, runner):
    output_with_list = runner.invoke(cards.cli.cards_cli, ['list']).output
    output_without_list = runner.invoke(cards.cli.cards_cli).output

    expected_output = ("  ID      owner  done summary\n"
                       "  --      -----  ---- -------\n"
                       "   1                  one item\n"
                       "   2                  second item\n"
                       "   3                  third item\n")
    assert expected_output == output_with_list
    assert expected_output == output_without_list
    assert output_with_list == output_without_list
