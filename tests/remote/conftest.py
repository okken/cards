import difflib

import pytest
from cards.remote import RemoteCardsDB

ME = "brian@pythontest.com"
MEMBERS = {
    "brian@pythontest.com": "Brian Okken",
    "anna@example.com": "Anna Smith",
    "anne@example.com": "Anne Jones",
}


class FakeCardsAPI:
    """In-memory stand-in for the web app's /a/<team>/api/cards/ endpoints.

    Mimics the responses RemoteCardsDB relies on, including owner
    "did you mean" errors and pagination.
    """

    page_size = 2

    def __init__(self):
        self.cards = {}
        self.last_number = 0
        self.status_override = None
        self.requests = []

    # owner matching, roughly like the web app
    def _names(self, email):
        name = MEMBERS[email]
        return {email, email.split("@")[0], name.lower(), name.split()[0].lower()}

    def _resolve(self, text):
        text = text.strip().lower()
        if text == "me":
            return ME, None
        exact = [e for e in MEMBERS if text in self._names(e)]
        if len(exact) == 1:
            return exact[0], None
        close = exact or [
            e
            for e in MEMBERS
            if max(difflib.SequenceMatcher(None, text, n).ratio() for n in self._names(e))
            >= 0.6
        ]
        error = {
            "owner": {
                "detail": f"'{text}' doesn't match exactly one team member.",
                "suggestions": [{"email": e, "name": MEMBERS[e]} for e in close],
            }
        }
        return None, error

    def _data(self, number):
        card = self.cards[number]
        owner = card["owner"]
        return {
            "id": number,
            "summary": card["summary"],
            "owner": {"id": 1, "email": owner, "name": MEMBERS[owner]} if owner else None,
            "state": card["state"],
            "details": card.get("details", ""),
            "later": card.get("later", False),
        }

    def _filtered(self, params):
        numbers = sorted(self.cards)
        owner = params.get("owner")
        if owner == "none":
            numbers = [n for n in numbers if self.cards[n]["owner"] is None]
        elif owner:
            email, error = self._resolve(owner)
            if error:
                return None, error
            numbers = [n for n in numbers if self.cards[n]["owner"] == email]
        state = params.get("state", "all")
        if state == "open":
            numbers = [n for n in numbers if self.cards[n]["state"] != "done"]
        elif state != "all":
            numbers = [n for n in numbers if self.cards[n]["state"] == state]
        return numbers, None

    def request(self, method, path="", params=None, body=None):
        self.requests.append((method, path, params, body))
        if self.status_override:
            return self.status_override, {"detail": "nope"}
        params = params or {}
        if path == "" and method == "GET":
            numbers, error = self._filtered(params)
            if error:
                return 400, error
            page = int(params.get("page", 1))
            start = (page - 1) * self.page_size
            chunk = numbers[start : start + self.page_size]
            has_next = start + self.page_size < len(numbers)
            return 200, {
                "count": len(numbers),
                "next": "more" if has_next else None,
                "results": [self._data(n) for n in chunk],
            }
        if path == "" and method == "POST":
            if not body.get("summary"):
                return 400, {"summary": ["This field may not be blank."]}
            owner = None
            if body.get("owner"):
                owner, error = self._resolve(body["owner"])
                if error:
                    return 400, error
            self.last_number += 1
            self.cards[self.last_number] = {
                "summary": body["summary"],
                "owner": owner,
                "state": body.get("state", "todo"),
                "details": body.get("details", ""),
                "later": body.get("later", False),
            }
            return 201, self._data(self.last_number)
        if path == "count/":
            return 200, {"count": len(self.cards)}

        number_str, _, action = path.rstrip("/").partition("/")
        number = int(number_str)
        if number not in self.cards:
            return 404, {"detail": "Not found."}
        if action in ("start", "block", "finish") and method == "POST":
            self.cards[number]["state"] = {"start": "in prog", "block": "blocked", "finish": "done"}[action]
            return 200, self._data(number)
        if method == "GET":
            return 200, self._data(number)
        if method == "PATCH":
            if "owner" in body:
                owner, error = self._resolve(body["owner"])
                if error:
                    return 400, error
                body = {**body, "owner": owner}
            self.cards[number].update(body)
            return 200, self._data(number)
        if method == "DELETE":
            del self.cards[number]
            return 204, None
        raise AssertionError(f"unexpected request {method} {path}")


@pytest.fixture
def fake_api(monkeypatch):
    """Route every RemoteCardsDB request to an in-memory FakeCardsAPI."""
    api = FakeCardsAPI()

    def fake_request(self, method, path="", params=None, body=None):
        return api.request(method, path, params, body)

    monkeypatch.setattr(RemoteCardsDB, "_request", fake_request)
    return api


@pytest.fixture
def remote_db(fake_api):
    return RemoteCardsDB("http://cards.test", "sox", "secret-key")


@pytest.fixture
def remote_env(fake_api, monkeypatch):
    """Point the CLI at the (fake) web app."""
    monkeypatch.setenv("CARDS_URL", "http://cards.test")
    monkeypatch.setenv("CARDS_TEAM", "sox")
    monkeypatch.setenv("CARDS_API_KEY", "secret-key")
    return fake_api
