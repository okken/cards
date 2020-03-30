import cards
import pytest
from cards import Card


@pytest.fixture(scope="module", autouse=True)
def db_module(tmp_path_factory):
    """A db that can be used for all tests"""
    db_dir = tmp_path_factory.mktemp("tmp_db_dir")
    db_location = db_dir / ".cards_db.json"
    cards.set_db_path(db_location)


@pytest.fixture()
def db_empty(db_module):
    cards.delete_all()


def test_add_card(db_empty):
    c = Card(summary="something", owner="okken")
    id = cards.add_card(c)
    assert id is not None
    assert cards.count() == 1


@pytest.fixture()
def db_non_empty(db_empty):
    some_cards = (
        Card(summary="first item"),
        Card(summary="second item"),
        Card(summary="third item"),
    )
    ids = [cards.add_card(c) for c in some_cards]
    return {"initial_cards": some_cards, "ids": ids}


def test_get_card(db_empty):
    c = Card(summary="something", owner="okken")
    id = cards.add_card(c)

    retrieved_card = cards.get_card(id)

    assert retrieved_card == c
    assert retrieved_card.id == id


def test_list(db_empty):
    some_cards = [Card(summary="one"), Card(summary="two")]
    for c in some_cards:
        cards.add_card(c)

    all_cards = cards.list_cards()
    assert all_cards == some_cards


def test_list_filter_by_priority(db_empty):
    some_cards = [
        Card(summary="one", priority=2),
        Card(summary="two"),
        Card(summary="three", priority=1),
    ]
    for c in some_cards:
        cards.add_card(c)

    one_and_above = cards.list_cards(filter={"priority": 1})
    two_and_above = cards.list_cards(filter={"priority": 2})
    one, two, three = some_cards
    assert three in one_and_above

    assert one in two_and_above
    assert three in two_and_above
    assert two not in two_and_above


def test_count(db_empty):
    some_cards = [Card(summary="one"), Card(summary="two")]
    for c in some_cards:
        cards.add_card(c)

    assert cards.count() == 2


@pytest.fixture(scope="module")
def four_items(db_module):
    cards.delete_all()
    cards.add_card(Card(summary="one", owner="brian"))
    cards.add_card(Card(summary="two", owner="brian", done=True))
    cards.add_card(Card(summary="three", owner="okken", done=True))
    cards.add_card(Card(summary="three", owner="okken"))
    cards.add_card(Card(summary="four"))


def test_count_no_owner(four_items):
    assert cards.count(noowner=True) == 1


def test_count_owner(four_items):
    assert cards.count(owner="brian") == 2


def test_count_done(four_items):
    assert cards.count(done=True) == 2


def test_count_not_done(four_items):
    assert cards.count(done=False) == 3


def test_update(db_non_empty):
    # GIVEN a card known to be in the db
    all_cards = cards.list_cards()
    a_card = all_cards[0]

    # WHEN we update() the card with new info
    cards.update_card(a_card.id, Card(owner="okken", done=True))

    # THEN we can retrieve the card with get() and
    # and it has all of our changes
    updated_card = cards.get_card(a_card.id)
    expected = Card(summary=a_card.summary, owner="okken", done=True)
    assert updated_card == expected


def test_delete(db_non_empty):
    # GIVEN a non empty db
    a_card = cards.list_cards()[0]
    id = a_card.id
    count_before = cards.count()

    # WHEN we delete one item
    cards.delete_card(id)
    count_after = cards.count()

    # THEN the card is no longer in the db
    all_cards = cards.list_cards()
    assert a_card not in all_cards
    assert count_after == count_before - 1


def test_delete_all(db_non_empty):
    # GIVEN a non empty db

    # WHEN we delete_all()
    cards.delete_all()

    # THEN the count is 0
    count = cards.count()
    assert count == 0
