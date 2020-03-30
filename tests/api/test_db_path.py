import pathlib

import cards


def test_db_path_specified(tmp_path):
    db_location = tmp_path / ".cards_db.json"
    cards.set_db_path(db_location)
    assert cards.get_db_path() == db_location


def test_db_path_default():
    cards.set_db_path()
    expected = pathlib.Path().home() / ".cards_db.json"
    assert cards.get_db_path() == expected
