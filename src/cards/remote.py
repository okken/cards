"""
CardsDB stand-in that uses the Cards web app's API instead of a local file.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

from .api import Card, CardsException, InvalidCardId, MissingSummary

__all__ = [
    "RemoteCardsDB",
    "RemoteError",
    "OwnerNotFound",
]


class RemoteError(CardsException):
    """The web app couldn't be reached, or refused the request."""


class OwnerNotFound(CardsException):
    """The owner didn't match exactly one team member.

    `suggestions` is a list of (email, name) pairs the web app thinks were meant.
    """

    def __init__(self, owner: str, message: str, suggestions: list[tuple[str, str]]):
        super().__init__(message)
        self.owner = owner
        self.message = message
        self.suggestions = suggestions


class RemoteCardsDB:
    """Same interface as CardsDB, backed by /a/<team>/api/cards/ on the Cards web app."""

    def __init__(self, url: str, team: str, api_key: str, project: str | None = None):
        """`project` is a project's name, "all", or None for the team's default project."""
        self._url = url.rstrip("/")
        self._team = team
        self._api_key = api_key
        self._project = project or None
        self._base = f"{self._url}/a/{urllib.parse.quote(team)}/api/"
        # The project the last list_cards() showed, as named by the web app (None for "all").
        self.listed_project: str | None = None

    # --- HTTP ---------------------------------------------------------------------

    def _request(self, method: str, path: str = "", params=None, body=None, resource: str = "cards"):
        """Send a request to /api/<resource>/<path>; return (status, parsed JSON body or None)."""
        url = f"{self._base}{resource}/{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(url, data=data, method=method)
        request.add_header("Authorization", f"Api-Key {self._api_key}")
        request.add_header("Accept", "application/json")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status, _parse(response.read())
        except urllib.error.HTTPError as error:
            with error:
                return error.code, _parse(error.read())
        except urllib.error.URLError as error:
            raise RemoteError(f"Can't reach {self._url}: {error.reason}") from error

    def _check(self, status: int, payload, card_id: int | None = None, owner: str = ""):
        """Turn error responses into exceptions."""
        if status < 400:
            return
        if status == 404 and card_id is not None:
            raise InvalidCardId(card_id)
        if status in (401, 403):
            raise RemoteError(
                f"Not allowed: check CARDS_API_KEY, and that you're a member of team '{self._team}'."
            )
        if status == 404:
            raise RemoteError(f"Team '{self._team}' not found at {self._url}.")
        if status == 400 and isinstance(payload, dict) and isinstance(payload.get("owner"), dict):
            owner_error = payload["owner"]
            raise OwnerNotFound(
                owner=owner,
                message=owner_error.get("detail", "Owner not found."),
                suggestions=[(s["email"], s["name"]) for s in owner_error.get("suggestions", [])],
            )
        if status == 400 and isinstance(payload, dict) and "summary" in payload:
            raise MissingSummary
        if status == 400 and isinstance(payload, dict) and "project" in payload:
            raise RemoteError(_message(payload["project"]))
        if status == 400 and isinstance(payload, dict) and "name" in payload:
            raise RemoteError(_message(payload["name"]))
        raise RemoteError(f"Request failed ({status}): {payload}")

    # --- conversion ---------------------------------------------------------------

    @staticmethod
    def _to_card(data: dict) -> Card:
        owner = data.get("owner")
        return Card(
            summary=data["summary"],
            owner=owner["name"] if owner else "",
            state=data["state"],
            details=data.get("details") or None,
            later=data.get("later") or None,
            id=data["id"],
            project=data.get("project"),
        )

    # --- CardsDB interface ----------------------------------------------------------

    def add_card(self, card: Card) -> int:
        """Add a card, return the id of card."""
        if not card.summary:
            raise MissingSummary
        body = {"summary": card.summary, "state": card.state or "todo"}
        if card.owner:
            body["owner"] = card.owner
        if card.details:
            body["details"] = card.details
        if card.later:
            body["later"] = True
        project = card.project or (self._project if self._project != "all" else None)
        if project:
            body["project"] = project
        status, payload = self._request("POST", body=body)
        self._check(status, payload, owner=card.owner)
        return payload["id"]

    def get_card(self, card_id: int) -> Card:
        """Return a card with a matching id."""
        status, payload = self._request("GET", f"{card_id}/")
        self._check(status, payload, card_id)
        return self._to_card(payload)

    def list_cards(self, owner=None, state=None):
        """Return a list of cards, following pagination."""
        params = {}
        if self._project:
            params["project"] = self._project
        if owner is not None:
            params["owner"] = owner
        if state is not None:
            params["state"] = state
        status, payload = self._request("GET", params=params)
        self._check(status, payload, owner=owner or "")
        self.listed_project = payload.get("project")
        cards = [self._to_card(c) for c in payload["results"]]
        page = 1
        while payload.get("next"):
            page += 1
            status, payload = self._request("GET", params={**params, "page": page})
            self._check(status, payload)
            cards.extend(self._to_card(c) for c in payload["results"])
        return cards

    def count(self) -> int:
        """Return the number of cards in db."""
        params = {"project": self._project} if self._project else None
        status, payload = self._request("GET", "count/", params=params)
        self._check(status, payload)
        return payload["count"]

    def update_card(self, card_id: int, card_mods: Card) -> None:
        """Update a card with modifications."""
        body = {k: v for k, v in card_mods.to_dict().items() if v is not None and k != "id"}
        status, payload = self._request("PATCH", f"{card_id}/", body=body)
        self._check(status, payload, card_id, owner=body.get("owner", ""))

    def start(self, card_id: int):
        """Set a card state to 'in prog'."""
        status, payload = self._request("POST", f"{card_id}/start/")
        self._check(status, payload, card_id)

    def block(self, card_id: int):
        """Set a card state to 'blocked'."""
        status, payload = self._request("POST", f"{card_id}/block/")
        self._check(status, payload, card_id)

    def finish(self, card_id: int):
        """Set a card state to 'done'."""
        status, payload = self._request("POST", f"{card_id}/finish/")
        self._check(status, payload, card_id)

    def later(self, card_id: int):
        """Move a card to the Later list."""
        self.update_card(card_id, Card(state=None, later=True))

    def sooner(self, card_id: int):
        """Move a card back to the Sooner list."""
        self.update_card(card_id, Card(state=None, later=False))

    def delete_card(self, card_id: int) -> None:
        """Remove a card from db with given card_id."""
        status, payload = self._request("DELETE", f"{card_id}/")
        self._check(status, payload, card_id)

    def list_projects(self) -> list[dict]:
        """The team's projects (default first): dicts with name, is_default and open_cards."""
        status, payload = self._request("GET", resource="projects")
        self._check(status, payload)
        return payload

    def add_project(self, name: str) -> None:
        status, payload = self._request("POST", body={"name": name}, resource="projects")
        self._check(status, payload)

    def delete_all(self) -> None:
        """Not supported: too risky on a shared team."""
        raise RemoteError("delete_all isn't available for the web app.")

    def close(self):
        pass

    def path(self):
        return f"{self._url} (team: {self._team})"


def _message(errors) -> str:
    """A DRF field error (a string or list of strings) as one message."""
    return " ".join(errors) if isinstance(errors, list) else str(errors)


def _parse(raw: bytes):
    if not raw:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return raw.decode(errors="replace")
