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
from cards import Card


@pytest.mark.alac
def test_alac_1(db_empty):
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
    db = db_empty

    # 1. Add 3 items
    input = ({'summary': 'something'},
             {'summary': 'something else', 'owner': 'okken'},
             {'summary': 'Foo Bar Baz'})
    ids = []
    for i in input:
        ids.append(db.add(Card(**i)))  # ** is dictionary unpacking

    # 2. Make sure they show up in the list.
    all_cards = db.list_cards()

    # extra checks, not specifically called out in description but logical
    assert len(input) == db.count()
    assert len(input) == len(all_cards)

    # now compare list with input
    expected_cards = tuple(Card(**i) for i in input)
    for expected, card in zip(expected_cards, all_cards):  # pairwise
        assert expected == card
    # assert expected_cards == all_cards # this doesn't work, not sure why

    # 3. Change the owner on a card. Verify change.
    a_valid_id = ids[0]
    card_before = db.get(a_valid_id)
    db.update(a_valid_id, Card(owner='okken'))
    card_after = db.get(a_valid_id)

    assert card_before != card_after  # make sure a change happened
    assert card_after.owner == 'okken'

    # 4. Change the done state on a card. Verify change.
    a_valid_id = ids[1]
    card_before = db.get(a_valid_id)
    db.update(a_valid_id, Card(done=True))
    card_after = db.get(a_valid_id)

    assert card_before != card_after  # make sure a change happened
    assert card_after.done

    # 5. Change the sumary on a card. Verify change.
    a_valid_id = ids[2]
    card_before = db.get(a_valid_id)
    db.update(a_valid_id, Card(summary='just sit'))
    card_after = db.get(a_valid_id)

    assert card_before != card_after  # make sure a change happened
    assert card_after.summary == 'just sit'

    # 6. Delete the done item. Verify change.

    # delete all done items, there should be just one
    # maybe this should be a utility API function?
    for c in db.list_cards():
        if c.done:
            db.delete(c.id)

    expected_cards = (Card(summary='something', owner='okken'),
                      Card(summary='just sit'))
    all_cards = db.list_cards()
    for expected, card in zip(expected_cards, all_cards):
        assert expected == card
