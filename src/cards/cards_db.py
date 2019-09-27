import pathlib
import tinydb
from typing import List, Union
from .cards_data import Card, Filter
from .cards_exceptions import UninitializedDB
from dataclasses import asdict

_db = None
_db_path = None


def set_db_path(db_path=None):
    global _db_path
    _db_path = db_path

def get_db_path():
    if _db_path is None:
        return pathlib.Path().home() / '.cards_db.json'
    else:
        return _db_path / '.cards_db.json'

def connect():
    global _db
    if _db is None:
        _db = tinydb.TinyDB(get_db_path())

def disconnect():
    global _db
    if _db is not None:
        _db.close()
        _db = None


def create(card: Card) -> int:
    if _db is None:
        raise UninitializedDB()
    card.id = _db.insert(asdict(card))
    _db.update(asdict(card), doc_ids=[card.id])
    return card.id


def read(card_id: int) -> Card:
    if _db is None:
        raise UninitializedDB()
    card_as_dict = _db.get(doc_id=card_id)
    return Card(**card_as_dict)


def read_many(filter: Union[Filter, None] = None) -> List[Card]:
    # this is admittedly ugly code.
    # TinyDB search syntax is wonderful, but quirky
    if _db is None:
        raise UninitializedDB()

    if ((filter is None) or  # no filter
        (filter == Filter(None, None, None))): # same as no filter
        # return everything
        return [Card(**t) for t in _db]


    # build query
    q = tinydb.Query()
    f = filter  # shorten

    # probably could roll done into above searches,
    # but brute force works for now, with small-ish databases

    if f.done is None: # no filter on done
        if f.owner and f.no_owner: # read items with matching owner or no owner
            results = _db.search(
                (q.owner == f.owner) |
                (q.owner == None) |  # noqa: "is None" doesn't work for TinyDb
                (q.owner == ''))
        elif f.no_owner or f.owner == '':
            results = _db.search((q.owner == None) | (q.owner == ''))
        elif f.owner:
            results = _db.search(q.owner == f.owner)
        else:
            results = _db
    else: # include done in filter
        if f.owner and f.no_owner: # read items with matching owner or no owner
            results = _db.search(
                ((q.owner == f.owner) |
                 (q.owner == None) |  # noqa: "is None" doesn't work for TinyDb
                 (q.owner == '')) & (q.done == f.done))
        elif f.no_owner or f.owner == '':
            results = _db.search(((q.owner == None) | (q.owner == ''))
                                 & (q.done == f.done))
        elif f.owner:
            results = _db.search((q.owner == f.owner) & (q.done == f.done))
        else:
            results = _db.search(q.done == f.done)

    return [Card(**t) for t in results if not t['done']]



def update(card_id: int, card_mods: Card) -> None:
    if _db is None:
        raise UninitializedDB()
    d = asdict(card_mods)
    changes = {k: v for k, v in d.items() if v is not None}
    _db.update(changes, doc_ids=[card_id])


def delete(card_id: int) -> None:
    if _db is None:
        raise UninitializedDB()
    _db.remove(doc_ids=[card_id])


def delete_all() -> None:
    if _db is None:
        raise UninitializedDB()
    _db.purge()
