import pathlib
import tinydb
from typing import List

from dataclasses import dataclass, field, asdict


__all__ = ["Card", "set_db_path", "get_db_path", "add_card", "get_card",
           "list_cards", "count", "update_card", "delete_card",
           "delete_all"]


@dataclass
class Card:
    summary: str = None
    owner: str = None
    priority: int = None
    done: bool = None
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        return Card(**d)

    def to_dict(self):
        return asdict(self)


_db = None
_db_path = None


def set_db_path(db_path=None):
    global _db
    global _db_path
    if db_path is None:
        _db_path = pathlib.Path().home() / '.cards_db.json'
    else:
        _db_path = db_path
    _db = tinydb.TinyDB(_db_path)


def get_db_path():
    return _db_path


def add_card(card: Card) -> int:
    """Add a card, return the id of card."""
    card.id = _db.insert(card.to_dict())
    _db.update(card.to_dict(), doc_ids=[card.id])
    return card.id


def get_card(card_id: int) -> Card:
    """Return a card with a matching id."""
    return Card.from_dict(_db.get(doc_id=card_id))


def list_cards(filter=None) -> List[Card]:
    """Return a list of all cards."""
    q = tinydb.Query()
    if filter:
        noowner = filter.get('noowner', None)
        owner = filter.get('owner', None)
        priority = filter.get('priority', None)
        done = filter.get('done', None)
    else:
        noowner = None
        owner = None
        priority = None
        done = None
    if noowner and owner:
        results = _db.search(
            (q.owner == owner) |
            (q.owner == None) |  # noqa : "is None" doesn't work for TinyDb
            (q.owner == ''))
    elif noowner or owner == '':
        results = _db.search((q.owner == None) |  (q.owner == '')) # noqa
    elif owner:
        results = _db.search(q.owner == owner)
    elif priority:
        results = _db.search((q.priority != None) &   # noqa
                             (q.priority <= priority))
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


def count(noowner=None, owner=None, priority=None, done=None) -> int:
    """Return the number of cards in db."""
    filter = {'noowner': noowner, 'owner': owner,
              'priority': priority, 'done': done}
    return len(list_cards(filter=filter))


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
