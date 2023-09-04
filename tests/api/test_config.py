"""
Test Cases
* `config` returns the correct database path
"""


def test_config(cards_db, db_path):
    assert cards_db.path() == db_path
