import cards


def test_start(cards_db, cards_cli):
    i = cards_db.add_card(cards.Card("some task"))
    cards_cli(f"start {i}")
    after = cards_db.get_card(i)
    assert after.state == "in prog"
