import cards


def test_finish(cards_db, cards_cli):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"finish {i}")
    after = cards_db.get_card(i)
    assert after.state == "done"
