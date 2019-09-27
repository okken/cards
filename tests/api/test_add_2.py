import cards
from cards import Card

# @dataclass
# class Card:
#     summary: str = None
#     owner: str = None
#     done: bool = None
#     id: int = field(default=None, compare=False)

def test_add(tmp_path):
    """
    Make sure I can add a card with add_card()
    Then retrieve it with get_card()
    And it's the right card
    """
    cards.set_db_path(tmp_path)
    cards.connect()
    c1 = Card('first task', 'brian', False)
    id = cards.add_card(c1)
    c2 = cards.get_card(id)
    cards.disconnect()
    assert c1 == c2

