def test_config(cards_cli, db_path):
    assert cards_cli("config") == str(db_path)


def test_config_normal_path(db_path, cards_cli_no_redirect):
    cards_cli = cards_cli_no_redirect
    assert cards_cli("config") != str(db_path)
