# -*- coding: utf-8 -*-
"""
Test list filtering in more depth
"""

import pytest
from pytest import param
from cards import Card


@pytest.fixture(scope='module')
def some_cards():
    return [Card(summary='zero', owner='anyone', done=True),
            Card(summary='one', owner='an_owner'),
            Card(summary='two', owner='anyone', done=False),
            Card(summary='three', owner='an_owner', done=True),
            Card(summary='four', done=True),
            # '' owner should be same as no owner because right now the
            # only way to remove an owner from the CLI is is to update it
            # with a blank string
            Card(summary='five', owner='')]


@pytest.fixture()
def db(db_empty, some_cards):
    db = db_empty
    for c in some_cards:
        db.add(c)
    return db


# noowner (None/True)
# owner (None/'an_owner'/'not_an_owner'/'')
# done (None/True/False)

@pytest.mark.parametrize('noowner, owner, done, indices', [
    param(None, None, None, (0, 1, 2, 3, 4, 5), id='no filter'),
    param(None, None, True, (0, 3, 4), id='all done'),
    param(None, None, False, (1, 2, 5), id='all not done'),
    param(None, 'an_owner', None, (1, 3), id='owner is an_owner'),
    param(None, 'an_owner', True, (3,), id='owner is an_owner and done'),
    param(None, 'an_owner', False, (1,), id='owner is an_owner and not done'),
    param(None, 'not_an_owner', None, list(), id='owner is not_an_owner'),
    param(None, '', None, (4, 5), id='blank owner'),
    param(None, '', True, (4,), id='blank owner and done'),
    param(None, '', False, (5,), id='blank owner and not done'),
    param(True, None, None, (4, 5), id='no owner'),
    param(True, None, True, (4,), id='no owner and done'),
    param(True, None, False, (5,), id='no owner and not done'),
    # noowner and an_owner is (either no owner or the set owner)
    param(True, 'an_owner', None, (1, 3, 4, 5), id='no owner or an_owner'),
    param(True, 'an_owner', True, (3, 4), id='(no owner | an_owner) & done'),
    param(True, 'an_owner', False, (1, 5), id='(no owner | an_owner) & !done'),
    # noowner-not_an_owner the same as noowner-None
    param(True, 'not_an_owner', None, (4, 5), id='no owner, not_an_owner'),
    param(True, 'not_an_owner', True, (4,), id='no owner, not_an_owner, done'),
    param(True, 'not_an_owner', False, (5,), id='no owner,not_an_owner,!done'),
])
def test_filter(db, some_cards, noowner, owner, done, indices):
    expected = [some_cards[i] for i in indices]
    output = db.list_cards(noowner=noowner, owner=owner, done=done)
    assert expected == output
