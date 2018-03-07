#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cards import Card

def test_add(db_empty):
    # GIVEN an empty database
    db = db_empty

    # WHEN a new card is added
    new_card = Card('do something')
    new_id = db.add(new_card)

    # THEN The listing returns just the new card
    all_cards = db.list_cards()
    assert 1 == len(all_cards)
    assert new_card == all_cards[0]

