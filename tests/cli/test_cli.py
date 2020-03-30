"""
Tests using cards CLI (command line interface).
"""


def test_add(db_empty, cards_cli, cards_cli_list_items):
    # GIVEN an empty database
    # WHEN a new card is added
    cards_cli("add something -o okken")

    # THEN The listing returns just the new card
    items = cards_cli_list_items("list")
    assert len(items) == 1
    assert items[0].summary == "something"
    assert items[0].owner == "okken"


def test_list_filter(db_empty, cards_cli, cards_cli_list_items):
    """
    Also kinda tests update
    """
    # GIVEN
    #  two items owned by okken, one that is done
    #  two items with no owner, one that is done
    cards_cli("add -o okken one")
    cards_cli("add -o anyone two")
    cards_cli("add -o okken three")
    cards_cli("add four")
    cards_cli("add five")

    # get the ids for a couple of them
    items = cards_cli_list_items("list")
    for i in items:
        if i.summary in ("three", "four"):
            cards_cli(f"update {i.id} -d")

    # `cards --noowner -o okken -d` should return two items
    items = cards_cli_list_items("list --noowner -o okken -d")
    assert len(items) == 2
    for i in items:
        assert i.summary in ("three", "four")
        assert i.done == "x"
        assert i.owner in ("okken", "")


def test_count(db_empty, cards_cli):
    cards_cli("add one")
    cards_cli("add two")

    assert cards_cli("count") == "2"


def test_delete(db_empty, cards_cli, cards_cli_list_items):
    # GIVEN a db with 2 items
    cards_cli("add one")
    cards_cli("add two")

    an_id = cards_cli_list_items("list")[0].id

    # WHEN we delete one item
    cards_cli(f"delete {an_id}")

    # THEN the other card remains
    assert cards_cli("count") == "1"


def test_version(cards_cli):
    """
    Should return 3 digits separated by a dot
    """
    version = cards_cli("version").split(".")
    assert len(version) == 3
    assert all([d.isdigit() for d in version])
