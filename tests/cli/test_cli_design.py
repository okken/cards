# -*- coding: utf-8 -*-
"""
Tests using cards CLI (command line interface).
This file contains tests related to design changes.
"""

import json
import pytest
import cards.cli


pytestmark = pytest.mark.cli


def test_list_format(db_non_empty, runner):
    """Check the format of list"""
    expected_output = ("  ID  owner    done    summary\n"
                       "----  -------  ------  -----------\n"
                       "   1                   first item\n"
                       "   2                   second item\n"
                       "   3                   third item\n")
    output = runner.invoke(cards.cli.cards_cli, ['list']).output
    assert expected_output == output


def test_cards_no_list_arg(db_non_empty, runner):
    """Does `cards` behave just like `cards list`?"""
    expected_output = ("  ID  owner    done    summary\n"
                       "----  -------  ------  -----------\n"
                       "   1                   first item\n"
                       "   2                   second item\n"
                       "   3                   third item\n")
    output = runner.invoke(cards.cli.cards_cli).output
    assert expected_output == output


def test_list_json(db_non_empty, runner):
    expected_json = {"cards": [
        {"done": None, "id": 1, "owner": None, "summary": "first item"},
        {"done": None, "id": 2, "owner": None, "summary": "second item"},
        {"done": None, "id": 3, "owner": None, "summary": "third item"}]}
    output_json_str = runner.invoke(cards.cli.cards_cli,
                                    ['list', '--format', 'json']).output
    output_json = json.loads(output_json_str)
    assert expected_json == output_json


def test_list_markdown(db_non_empty, runner):
    """Check the format of list --format markdown"""
    expected_output = ("|   ID | owner   | done   | summary     |\n"
                       "|-----:|:--------|:-------|:------------|\n"
                       "|    1 |         |        | first item  |\n"
                       "|    2 |         |        | second item |\n"
                       "|    3 |         |        | third item  |\n")
    output = runner.invoke(cards.cli.cards_cli,
                           ['list', '-f', 'markdown']).output
    assert expected_output == output
