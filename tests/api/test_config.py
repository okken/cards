"""
Test Cases
* `config` returns the correct database path
"""


def test_config(cards_db, tmp_db_path):
    assert cards_db.path() == tmp_db_path
