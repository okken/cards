"""
RemoteCardsDB has the same interface as CardsDB, backed by the web app's API.
"""
import pytest
from cards import Card, InvalidCardId, MissingSummary
from cards.remote import OwnerNotFound, RemoteError


def test_add_and_get(remote_db):
    i = remote_db.add_card(Card("something", owner="anna"))
    assert i == 1
    assert remote_db.get_card(i) == Card("something", owner="Anna Smith", state="todo")
    assert remote_db.get_card(i).id == 1


def test_add_without_owner(remote_db):
    i = remote_db.add_card(Card("something"))
    assert remote_db.get_card(i).owner == ""


def test_add_missing_summary(remote_db):
    with pytest.raises(MissingSummary):
        remote_db.add_card(Card())


def test_server_rejects_blank_summary(remote_db):
    status, payload = remote_db._request("POST", body={"summary": ""})
    assert status == 400
    with pytest.raises(MissingSummary):
        remote_db._check(status, payload)


def test_get_invalid_id(remote_db):
    with pytest.raises(InvalidCardId):
        remote_db.get_card(42)


def test_list_follows_pagination(remote_db, fake_api):
    for summary in ["one", "two", "three"]:
        remote_db.add_card(Card(summary))
    assert fake_api.page_size < 3
    assert [c.summary for c in remote_db.list_cards()] == ["one", "two", "three"]


def test_list_filters(remote_db):
    remote_db.add_card(Card("mine", owner="me"))
    remote_db.add_card(Card("annas", owner="anna"))
    remote_db.add_card(Card("nobody"))
    remote_db.finish(1)
    assert [c.summary for c in remote_db.list_cards(owner="anna")] == ["annas"]
    assert [c.summary for c in remote_db.list_cards(state="done")] == ["mine"]
    assert [c.summary for c in remote_db.list_cards(owner="none")] == ["nobody"]


def test_count(remote_db):
    remote_db.add_card(Card("one"))
    remote_db.add_card(Card("two"))
    assert remote_db.count() == 2


def test_update(remote_db, fake_api):
    i = remote_db.add_card(Card("old"))
    remote_db.update_card(i, Card(summary="new", owner=None, state=None))
    assert remote_db.get_card(i).summary == "new"
    # only the changed field is sent
    assert fake_api.requests[-2] == ("PATCH", "1/", None, {"summary": "new"})


def test_update_invalid_id(remote_db):
    with pytest.raises(InvalidCardId):
        remote_db.update_card(42, Card(summary="x", state=None))


def test_start_finish(remote_db):
    i = remote_db.add_card(Card("work"))
    remote_db.start(i)
    assert remote_db.get_card(i).state == "in prog"
    remote_db.finish(i)
    assert remote_db.get_card(i).state == "done"


def test_delete(remote_db):
    i = remote_db.add_card(Card("gone"))
    remote_db.delete_card(i)
    with pytest.raises(InvalidCardId):
        remote_db.delete_card(i)


def test_owner_not_found_has_suggestions(remote_db):
    with pytest.raises(OwnerNotFound) as exc_info:
        remote_db.add_card(Card("x", owner="brain"))
    assert exc_info.value.owner == "brain"
    assert exc_info.value.suggestions == [("brian@example.com", "Brian Okken")]


def test_list_owner_not_found(remote_db):
    with pytest.raises(OwnerNotFound):
        remote_db.list_cards(owner="brain")


def test_not_allowed(remote_db, fake_api):
    fake_api.status_override = 403
    with pytest.raises(RemoteError, match="CARDS_API_KEY"):
        remote_db.count()


def test_delete_all_not_supported(remote_db):
    with pytest.raises(RemoteError):
        remote_db.delete_all()


def test_path(remote_db):
    assert remote_db.path() == "http://cards.test (team: sox)"


def test_later_round_trip(remote_db):
    i = remote_db.add_card(Card("parked", later=True))
    assert remote_db.get_card(i).later is True
    remote_db.sooner(i)
    assert remote_db.get_card(i).later is None


def test_priority_round_trip(remote_db):
    i = remote_db.add_card(Card("urgent", priority="high"))
    assert remote_db.get_card(i).priority == "high"
    remote_db.update_card(i, Card(state=None, priority="normal"))
    assert remote_db.get_card(i).priority is None


def test_list_sorted_by_priority(remote_db):
    remote_db.add_card(Card("low", priority="low"))
    remote_db.add_card(Card("normal"))
    remote_db.add_card(Card("high", priority="high"))
    assert [c.summary for c in remote_db.list_cards()] == ["high", "normal", "low"]


def test_bad_priority_error(remote_db):
    i = remote_db.add_card(Card("x"))
    with pytest.raises(RemoteError, match="not a valid choice"):
        remote_db.update_card(i, Card(state=None, priority="urgent"))
