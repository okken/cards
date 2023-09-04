import cards


def test_update(cards_db, cards_cli):
    i = cards_db.add_card(cards.Card("foo"))
    cards_cli(f"update {i} -o okken -s something")
    expected = cards.Card("something", owner="okken", state="todo")
    actual = cards_db.get_card(i)
    assert actual == expected
