"""
Act Like A Customer Tests.

These tests are specifically designed to test lots of the system in
not many tests.

Pros:
- Can test lots of the system quickly.

Cons:
- Bail at first failure without testing all actions
- Don't follow arrange-act-assert or given-when-then style and
  are therefore terrible examples of how to write a test
"""

import pytest
from textwrap import dedent


@pytest.mark.alac
def test_alac_1(db_empty, cards_cli):
    """
    Starting from an empty list.
    1. Add 3 items
    2. Make sure they show up in the list.
    3. Change the owner on a card. Verify change.
    4. Change the done state on a card. Verify change.
    5. Change the sumary on a card. Verify change.
    6. Delete the done item. Verify change.
    """

    # Starting from an empty list.

    # 1. Add 3 items
    cards_cli('add something')
    cards_cli('add "something else" -o okken')
    cards_cli('add "Foo Bar Baz"')

    # 2. Make sure they show up in the list.
    output = cards_cli('list --format=packed')
    expected = dedent("""\
    1 unassigned o something
    2 okken o something else
    3 unassigned o Foo Bar Baz""")
    assert expected == output

    # 3. Change the owner on a card. Verify change.
    cards_cli('update 1 -o okken')
    output = cards_cli('list --format=packed')
    expected = dedent("""\
    1 okken o something
    2 okken o something else
    3 unassigned o Foo Bar Baz""")
    assert expected == output

    # 4. Change the done state on a card. Verify change.
    cards_cli('update 2 -d True')
    output = cards_cli('list --format=packed')
    expected = dedent("""\
    1 okken o something
    2 okken x something else
    3 unassigned o Foo Bar Baz""")
    assert expected == output

    # 5. Change the sumary on a card. Verify change.
    cards_cli('update 3 -s "just sit"')
    output = cards_cli('list --format=packed')
    expected = dedent("""\
    1 okken o something
    2 okken x something else
    3 unassigned o just sit""")
    assert expected == output

    # 6. Delete the done item. Verify change.
    cards_cli('delete 2')
    output = cards_cli('list --format=packed')
    expected = dedent("""\
    1 okken o something
    3 unassigned o just sit""")
    assert expected == output

    # let's also check the counts
    assert '2' == cards_cli('count')
    assert '1' == cards_cli('count -o okken')
    assert '1' == cards_cli('count --noowner')
