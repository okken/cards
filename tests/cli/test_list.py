import cards


expected_output = """\

  ID   state   owner   summary    
 ──────────────────────────────── 
  1    todo            some task  
  2    todo            another
"""

def test_list(cards_db, cards_cli):
    cards_db.add_card(cards.Card("some task"))
    cards_db.add_card(cards.Card("another"))
    output = cards_cli("list")
    assert output.strip() == expected_output.strip()

def test_main(cards_db, cards_cli):
    cards_db.add_card(cards.Card("some task"))
    cards_db.add_card(cards.Card("another"))
    output = cards_cli("")
    assert output.strip() == expected_output.strip()

