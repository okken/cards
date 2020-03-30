"""
Tests using cards CLI (command line interface).
This file contains tests related to design changes.
"""
import json
from textwrap import dedent

expected_output_default = """\
  ID  owner    priority    done    summary
----  -------  ----------  ------  -----------
   1                               first item
   2                               second item
   3                               third item"""


def test_list_format(db_non_empty, cards_cli):
    """Check the format of list"""
    output = cards_cli("list")
    print(output)
    assert expected_output_default == output


def test_cards_no_list_arg(db_non_empty, cards_cli):
    """Does `cards` behave just like `cards list`?"""
    output = cards_cli("")
    assert expected_output_default == output


def test_list_json(db_non_empty, cards_cli):
    expected_json = {
        "cards": [
            {
                "done": None,
                "id": 1,
                "owner": None,
                "priority": None,
                "summary": "first item",
            },
            {
                "done": None,
                "id": 2,
                "owner": None,
                "priority": None,
                "summary": "second item",
            },
            {
                "done": None,
                "id": 3,
                "owner": None,
                "priority": None,
                "summary": "third item",
            },
        ],
    }
    output_json_str = cards_cli("list --format=json")
    output_json = json.loads(output_json_str)
    assert expected_json == output_json


def test_list_markdown(db_non_empty, cards_cli):
    """Check the format of list --format markdown (and pipe)"""
    expected_output = dedent(
        """\
    |   ID | owner   | priority   | done   | summary     |
    |-----:|:--------|:-----------|:-------|:------------|
    |    1 |         |            |        | first item  |
    |    2 |         |            |        | second item |
    |    3 |         |            |        | third item  |""",
    )
    output = cards_cli("list -f markdown")
    assert expected_output == output

    output = cards_cli("list -f pipe")
    assert expected_output == output


def test_list_packed(db_non_empty, cards_cli):
    """Check the format of list --format packed"""
    expected_output = dedent(
        """\
    1 unassigned None o first item
    2 unassigned None o second item
    3 unassigned None o third item""",
    )
    output = cards_cli("list -f packed")
    assert expected_output == output


def test_list_grid(db_non_empty, cards_cli):
    """Check the format of list --format grid"""
    expected_output = dedent(
        """\
    +------+---------+------------+--------+-------------+
    |   ID | owner   | priority   | done   | summary     |
    +======+=========+============+========+=============+
    |    1 |         |            |        | first item  |
    +------+---------+------------+--------+-------------+
    |    2 |         |            |        | second item |
    +------+---------+------------+--------+-------------+
    |    3 |         |            |        | third item  |
    +------+---------+------------+--------+-------------+""",
    )
    output = cards_cli("list -f grid")
    assert expected_output == output
