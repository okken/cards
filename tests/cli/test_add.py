import cards


def test_add(cards_db, cards_cli):
    cards_cli("add some task")
    expected = cards.Card("some task", owner="", state="todo")
    all = cards_db.list_cards()
    assert len(all) == 1
    assert all[0] == expected


def test_add_with_owner(cards_db, cards_cli):
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    all = cards_db.list_cards()
    assert len(all) == 1
    assert all[0] == expected
