# -*- coding: utf-8 -*-

"""
cardsdb :  The API
"""

import attr
import tinydb
from typing import List


@attr.s
class Card(object):
    summary: str = attr.ib(default=None)
    owner: str = attr.ib(default=None)
    done: bool = attr.ib(default=None)
    id: int = attr.ib(default=None, cmp=False)

    @classmethod
    def from_dict(cls, d):
        return Card(**d)  # dictionary unpacking as of Python 3.5, PEP 448

    def to_dict(self):
        return attr.asdict(self)

# --- actions on db


class CardsDB():

    def __init__(self, db_path):
        self._db = tinydb.TinyDB(db_path)

    def add(self, card: Card) -> int:
        """Add a card to the db."""
        card.id = self._db.insert(card.to_dict())
        self._db.update(card.to_dict(), doc_ids=[card.id])
        return card.id

    def get(self, card_id: int) -> Card:
        """Return a card with a matching id."""
        return Card.from_dict(self._db.get(doc_id=card_id))

    def list_cards(self) -> List[Card]:
        """Return a list of all cards."""
        return [Card.from_dict(t) for t in self._db]

    def count(self) -> int:
        """Return the number of cards in db."""
        return len(self._db)

    def update(self, card_id: int, card_mods: Card) -> None:
        """Update a card with modifications."""
        d = card_mods.to_dict()
        changes = {k: v for k, v in d.items() if v is not None}
        self._db.update(changes, doc_ids=[card_id])

    def delete(self, card_id: int) -> None:
        """Remove a card from db with given card_id."""
        self._db.remove(doc_ids=[card_id])

    def delete_all(self) -> None:
        """Remove all tasks from db."""
        self._db.purge()
