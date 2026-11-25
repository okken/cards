import difflib

import pytest
from cards.remote import RemoteCardsDB

ME = "brian@example.com"
MEMBERS = {
    "brian@example.com": "Brian Okken",
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
        self.projects = ["General"]  # the first is the default

    def _project(self, text):
        """(project name, error) for a project name, "" for the default."""
        if not text:
            return self.projects[0], None
        for name in self.projects:
            if name.lower() == text.lower():
                return name, None
        return None, {"project": [f"No project named '{text}'. Projects: {', '.join(self.projects)}."]}

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
            "priority": card.get("priority", "normal"),
            "project": card.get("project", "General"),
        }

    def _filtered(self, params):
        ranks = {"high": 0, "normal": 1, "low": 2}
        numbers = sorted(self.cards, key=lambda n: (ranks[self.cards[n].get("priority", "normal")], n))
        if params.get("project") != "all":
            project, error = self._project(params.get("project", ""))
            if error:
                return None, error
            numbers = [n for n in numbers if self.cards[n].get("project", "General") == project]
        owner = params.get("owner")
        if owner == "none":
            numbers = [n for n in numbers if self.cards[n]["owner"] is None]
        elif owner:
            email, error = self._resolve(owner)
            if error:
                return None, error
            numbers = [n for n in numbers if self.cards[n]["owner"] == email]
        state = params.get("state", "all")
        if state != "all":
            numbers = [n for n in numbers if self.cards[n]["state"] == state]
        return numbers, None

    def request(self, method, path="", params=None, body=None, resource="cards"):
        self.requests.append((method, path, params, body))
        if self.status_override:
            return self.status_override, {"detail": "nope"}
        params = params or {}
        if resource == "projects":
            if method == "POST":
                if any(n.lower() == body["name"].lower() for n in self.projects):
                    return 400, {"name": [f"There's already a project named '{body['name']}'."]}
                self.projects.append(body["name"])
                return 201, {"name": body["name"]}
            return 200, [
                {
                    "name": name,
                    "is_default": i == 0,
                    "open_cards": sum(
                        1
                        for c in self.cards.values()
                        if c.get("project", "General") == name and c["state"] != "done"
                    ),
                }
                for i, name in enumerate(self.projects)
            ]
        if path == "" and method == "GET":
            numbers, error = self._filtered(params)
            if error:
                return 400, error
            page = int(params.get("page", 1))
            start = (page - 1) * self.page_size
            chunk = numbers[start : start + self.page_size]
            has_next = start + self.page_size < len(numbers)
            listed = None
            if params.get("project") != "all":
                listed = self._project(params.get("project", ""))[0]
            return 200, {
                "count": len(numbers),
                "next": "more" if has_next else None,
                "results": [self._data(n) for n in chunk],
                "project": listed,
            }
        if path == "" and method == "POST":
            if not body.get("summary"):
                return 400, {"summary": ["This field may not be blank."]}
            owner = None
            if body.get("owner"):
                owner, error = self._resolve(body["owner"])
                if error:
                    return 400, error
            project, error = self._project(body.get("project", ""))
            if error:
                return 400, error
            self.last_number += 1
            self.cards[self.last_number] = {
                "project": project,
                "summary": body["summary"],
                "owner": owner,
                "state": body.get("state", "todo"),
                "details": body.get("details", ""),
                "later": body.get("later", False),
                "priority": body.get("priority", "normal"),
            }
            return 201, self._data(self.last_number)
        if path.endswith("/comments/"):
            number = int(path.split("/")[0])
            if number not in self.cards:
                return 404, {"detail": "Not found."}
            comments = self.cards[number].setdefault("comments", [])
            if method == "GET":
                return 200, comments
            if not body.get("text", "").strip():
                return 400, {"text": ["A comment needs some text."]}
            comment = {
                "id": len(comments) + 1,
                "text": body["text"],
                "author": {"id": 1, "email": "brian@example.com", "name": "Brian Okken"},
                "created_at": "2026-11-25T17:03:12.123456Z",
            }
            comments.append(comment)
            return 201, comment
        if path == "count/":
            return 200, {"count": len(self.cards)}

        number_str, _, action = path.rstrip("/").partition("/")
        number = int(number_str)
        if number not in self.cards:
            return 404, {"detail": "Not found."}
        if action in ("start", "pause", "finish") and method == "POST":
            self.cards[number]["state"] = {"start": "in prog", "pause": "paused", "finish": "done"}[action]
            return 200, self._data(number)
        if method == "GET":
            return 200, self._data(number)
        if method == "PATCH":
            if "owner" in body:
                owner, error = self._resolve(body["owner"])
                if error:
                    return 400, error
                body = {**body, "owner": owner}
            if body.get("priority", "normal") not in ("high", "normal", "low"):
                return 400, {"priority": [f"\"{body['priority']}\" is not a valid choice."]}
            if "project" in body:
                project, error = self._project(body["project"])
                if error:
                    return 400, error
                body = {**body, "project": project}
            self.cards[number].update(body)
            return 200, self._data(number)
        if method == "DELETE":
            del self.cards[number]
            return 204, None
        raise AssertionError(f"unexpected request {method} {path}")  # pragma: no cover


@pytest.fixture
def fake_api(monkeypatch):
    """Route every RemoteCardsDB request to an in-memory FakeCardsAPI."""
    api = FakeCardsAPI()

    def fake_request(self, method, path="", params=None, body=None, resource="cards"):
        return api.request(method, path, params, body, resource)

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
