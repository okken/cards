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
            Card(summary='one', owner='okken'),
            Card(summary='two', owner='anyone', done=False),
            Card(summary='three', owner='okken', done=True),
            Card(summary='four', done=True),
            # '' owner should be same as no owner
            Card(summary='five', owner='')]
    return


@pytest.fixture()
def db(db_empty, some_cards):
    db = db_empty
    for c in some_cards:
        db.add(c)
    return db


# noowner (None/True)
# owner (None/'okken'/'')
# done (None/True/False)

@pytest.mark.parametrize('noowner, owner, done, indices', [
    param(None, None, None, (0, 1, 2, 3, 4, 5), id='no filter'),
    param(None, None, True, (0, 3, 4), id='all done'),
    param(None, None, False, (1, 2, 5), id='all not done'),
    param(None, 'okken', None, (1, 3), id='owner is okken'),
    param(None, 'okken', True, (3,), id='owner is okken and done'),
    param(None, 'okken', False, (1,), id='owner is okken and not done'),
    param(True, None, None, (4, 5), id='no owner'),
    param(True, None, True, (4,), id='no owner and done'),
    param(True, None, False, (5,), id='no owner and not done'),
    param(None, '', None, (4, 5), id='blank owner'),
    param(None, '', True, (4,), id='blank owner and done'),
    param(None, '', False, (5,), id='blank owner and not done'),
    param(True, 'okken', None, (1, 3, 4, 5), id='no owner or owner is okken'),
    param(True, 'okken', True, (3, 4), id='(no owner or okken) and done'),
    param(True, 'okken', False, (1, 5), id='(no owner or okken) and not done'),
])
def test_filter(db, some_cards, noowner, owner, done, indices):
    expected = [some_cards[i] for i in indices]
    output = db.list_cards(noowner=noowner, owner=owner, done=done)
    assert expected == output
