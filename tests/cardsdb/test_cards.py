# -*- coding: utf-8 -*-
"""
Tests using cards API.
This file contains tracer bullet tests.
Not in depth tests of functionality.
"""

from cards import Card


def test_add(db_empty):
    # GIVEN an empty database
    db = db_empty

    # WHEN a new card is added
    new_card = Card('do something')
    db.add(new_card)

    # THEN The listing returns just the new card
    all_cards = db.list_cards()
    assert 1 == len(all_cards)
    assert new_card == all_cards[0]


def test_get(db_non_empty):
    # GIVEN a card we know is in the db
    db = db_non_empty
    all_cards = db.list_cards()
    a_card = all_cards[0]

    # WHEN we call get() with the id of the known card
    retrieved_card = db.get(a_card.id)

    # THEN the retrieved card is identical
    # AND has the same id
    assert a_card == retrieved_card
    assert a_card.id == retrieved_card.id


def test_list(db_empty):
    # GIVEN a db with known contents of 2 cards
    db = db_empty
    db.add(Card(summary='one'))
    db.add(Card(summary='two'))

    # list_cards() returns our 2 cards
    all_cards = db.list_cards()
    expected = [Card(summary='one'), Card(summary='two')]
    assert expected == all_cards


def test_count(db_empty):
    # GIVEN a db with 2 cards
    db = db_empty
    db.add(Card(summary='one'))
    db.add(Card(summary='two'))

    # count() returns 2
    count = db.count()
    assert 2 == count


def test_update(db_non_empty):
    # GIVEN a card known to be in the db
    db = db_non_empty
    all_cards = db.list_cards()
    a_card = all_cards[0]

    # WHEN we update() the card with new info
    db.update(a_card.id, Card(owner='okken', done=True))

    # THEN we can retrieve the card with get() and
    # and it has all of our changes
    updated_card = db.get(a_card.id)
    expected = Card(summary=a_card.summary, owner='okken', done=True)
    assert expected == updated_card


def test_delete(db_empty):
    # GIVEN a db with 2 items
    db = db_empty
    id_1 = db.add(Card(summary='one'))
    db.add(Card(summary='two'))

    # WHEN we delete one item
    db.delete(id_1)

    # THEN the other card remains in the db
    all_cards = db.list_cards()
    expected = [Card(summary='two')]
    assert expected == all_cards


def test_delete_all(db_non_empty):
    # GIVEN a non empty db
    db = db_non_empty

    # WHEN we delete_all()
    db.delete_all()

    # THEN the count is 0
    count = db.count()
    assert 0 == count
