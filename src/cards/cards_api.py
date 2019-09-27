from typing import List, Union
from .cards_data import Card, Filter
from . import cards_db


__all__ = ["Card", "add_card", "get_card",
           "list_cards", "finish", "count", "update_card", "delete_card",
           "delete_all"]


def add_card(card: Card) -> int:
    return cards_db.create(card)


def get_card(card_id: int) -> Card:
    return cards_db.read(card_id)


def list_cards(filter: Union[Filter, None] = None) -> List[Card]:
    return cards_db.read_many(filter)


def count(filter: Union[Filter, None] = None) -> int:
    return len(list_cards(filter=filter))


def finish(card_id: int):
    cards_db.update(card_id, Card(done=True))


def update_card(card_id: int, card_mods: Card) -> None:
    cards_db.update(card_id, card_mods)


def delete_card(card_id: int) -> None:
    cards_db.delete(card_id)


def delete_all() -> None:
    cards_db.delete_all()
