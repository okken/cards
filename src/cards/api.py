import pathlib
import tinydb
from typing import List

from dataclasses import dataclass, field, asdict


__all__ = ["Card", "set_db_path", "add_card", "get_card",
           "list_cards", "count", "update_card", "delete_card",
           "delete_all"]


@dataclass
class Card:
    summary: str = None
    owner: str = None
    done: bool = None
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        return Card(**d)

    def to_dict(self):
        return asdict(self)


_db = None


def set_db_path(db_path=None):
    global _db
    if db_path is None:
        db_path = pathlib.Path().home() / '.cards_db.json'
    _db = tinydb.TinyDB(db_path)


def add_card(card: Card) -> int:
    """Add a card, return the id of card."""
    card.id = _db.insert(card.to_dict())
    _db.update(card.to_dict(), doc_ids=[card.id])
    return card.id


def get_card(card_id: int) -> Card:
    """Return a card with a matching id."""
    return Card.from_dict(_db.get(doc_id=card_id))


def list_cards(noowner=None, owner=None, done=None) -> List[Card]:
    """Return a list of all cards."""
    q = tinydb.Query()
    if noowner and owner:
        results = _db.search(
            (q.owner == owner) |
            (q.owner == None) |  # noqa : "is None" doesn't work for TinyDb
            (q.owner == ''))
    elif noowner or owner == '':
        results = _db.search((q.owner == None) |  (q.owner == '')) # noqa
    elif owner:
        results = _db.search(q.owner == owner)
    else:
        results = _db

    if done is None:
        # return all cards
        return [Card.from_dict(t) for t in results]
    elif done:
        # only done cards
        return [Card.from_dict(t) for t in results if t['done']]
    else:
        # only not done cards
        return [Card.from_dict(t) for t in results if not t['done']]


def count(noowner=None, owner=None, done=None) -> int:
    """Return the number of cards in db."""
    return len(list_cards(noowner, owner, done))


def update_card(card_id: int, card_mods: Card) -> None:
    """Update a card with modifications."""
    d = card_mods.to_dict()
    changes = {k: v for k, v in d.items() if v is not None}
    _db.update(changes, doc_ids=[card_id])


def delete_card(card_id: int) -> None:
    """Remove a card from db with given card_id."""
    _db.remove(doc_ids=[card_id])


def delete_all() -> None:
    """Remove all tasks from db."""
    _db.purge()
