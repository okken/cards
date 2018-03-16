# -*- coding: utf-8 -*-
"""
Tests using cards CLI (command line interface).
This file contains tests related to design changes.
"""

import cards.cli


def test_list_on_no_command(db_non_empty, runner):
    """Does `cards` behave just like `cards list`?"""
    output_with_list = runner.invoke(cards.cli.cards_cli, ['list']).output
    output_without_list = runner.invoke(cards.cli.cards_cli).output

    expected_output = ("  ID      owner  done summary\n"
                       "  --      -----  ---- -------\n"
                       "   1                  first item\n"
                       "   2                  second item\n"
                       "   3                  third item\n")
    assert expected_output == output_with_list
    assert expected_output == output_without_list
    assert output_with_list == output_without_list
