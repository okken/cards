import cards
from cards import Card

def test_add(tmp_path):
    cards.set_db_path(tmp_path)
    cards.connect()
    a_card = Card('first task', 'brian', False)
    id = cards.add_card(a_card)
    c2 = cards.get_card(id)
    cards.disconnect()
    assert a_card == c2

