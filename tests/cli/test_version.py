import cards


def test_version(cards_cli):
    assert cards_cli("version") == cards.__version__
