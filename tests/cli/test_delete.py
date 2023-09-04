import cards


def test_delete(cards_db, cards_cli):
    i = cards_db.add_card(cards.Card("foo"))
    cards_cli(f"delete {i}")
    assert cards_db.count() == 0
