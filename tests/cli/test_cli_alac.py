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
from cards.cli import cards_cli


pytestmark = pytest.mark.cli


@pytest.mark.alac
def test_alac_1(db_empty, runner):
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
    runner.invoke(cards_cli, ['add', 'something'])
    runner.invoke(cards_cli, ['add', 'something else', '-o', 'okken'])
    runner.invoke(cards_cli, ['add', 'Foo Bar Baz'])

    # 2. Make sure they show up in the list.
    result = runner.invoke(cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   1                  something\n"
                "   2      okken       something else\n"
                "   3                  Foo Bar Baz\n")
    assert expected == result.output

    # 3. Change the owner on a card. Verify change.
    runner.invoke(cards_cli, ['update', '1', '-o', 'okken'])
    result = runner.invoke(cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   1      okken       something\n"
                "   2      okken       something else\n"
                "   3                  Foo Bar Baz\n")
    assert expected == result.output

    # 4. Change the done state on a card. Verify change.
    runner.invoke(cards_cli, ['update', '2', '-d', 'True'])
    result = runner.invoke(cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   1      okken       something\n"
                "   2      okken    x  something else\n"
                "   3                  Foo Bar Baz\n")
    assert expected == result.output

    # 5. Change the sumary on a card. Verify change.
    runner.invoke(cards_cli, ['update', '3', '-s', 'just sit'])
    result = runner.invoke(cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   1      okken       something\n"
                "   2      okken    x  something else\n"
                "   3                  just sit\n")
    assert expected == result.output

    # 6. Delete the done item. Verify change.
    runner.invoke(cards_cli, ['delete', '2'])
    result = runner.invoke(cards_cli, ['list'])
    expected = ("  ID      owner  done summary\n"
                "  --      -----  ---- -------\n"
                "   1      okken       something\n"
                "   3                  just sit\n")
    assert expected == result.output

    # let's also check the count
    result = runner.invoke(cards_cli, ['count'])
    expected = "2\n"
    assert expected == result.output
