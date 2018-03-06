#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cards import Card

def test_add(db_empty):
    # GIVEN an empty database
    db = db_empty

    # WHEN a new card is added
    new_card = Card('do something')
    new_id = db.add(new_card)

    # THEN The card count is increased to 1
    assert 1 == db.count()
    # AND It's retrievable by the id
    assert new_card == db.get(new_id)

