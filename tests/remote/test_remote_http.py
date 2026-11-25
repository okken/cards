"""
RemoteCardsDB's HTTP layer, against a tiny local server.
"""
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
import cards
from cards import MissingSummary
from cards.remote import RemoteCardsDB, RemoteError, _parse


class Handler(BaseHTTPRequestHandler):
    seen = []
    user_agents = []

    def _reply(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.seen.append(("GET", self.path, self.headers["Authorization"], None))
        self.user_agents.append(self.headers["User-Agent"])
        self._reply(200, {"count": 7})

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        self.seen.append(("POST", self.path, self.headers["Authorization"], body))
        self._reply(400, {"summary": ["This field may not be blank."]})

    def log_message(self, *args):
        pass


@pytest.fixture
def server():
    Handler.seen = []
    Handler.user_agents = []
    httpd = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


def test_request_url_and_auth(server):
    db = RemoteCardsDB(server + "/", "sox", "secret-key")
    assert db.count() == 7
    assert Handler.seen == [("GET", "/a/sox/api/cards/count/", "Api-Key secret-key", None)]


def test_json_body_and_error_status(server):
    db = RemoteCardsDB(server, "sox", "secret-key")
    status, payload = db._request("POST", body={"summary": ""})
    assert status == 400
    assert payload == {"summary": ["This field may not be blank."]}
    assert Handler.seen[0][3] == {"summary": ""}


def test_cannot_connect():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]  # nothing listens here once the socket closes
    db = RemoteCardsDB(f"http://127.0.0.1:{port}", "sox", "secret-key")
    with pytest.raises(RemoteError, match="Can't reach"):
        db.count()


def test_query_params_are_encoded(server):
    db = RemoteCardsDB(server, "sox", "secret-key")
    db._request("GET", params={"state": "open", "owner": "a b"})
    assert Handler.seen[0][1] == "/a/sox/api/cards/?state=open&owner=a+b"


@pytest.mark.parametrize(
    "status, payload, error, match",
    [
        (404, None, RemoteError, "Team 'sox' not found"),
        (400, {"summary": ["required"]}, MissingSummary, None),
        (500, "oops", RemoteError, r"Request failed \(500\): oops"),
    ],
)
def test_check_errors(status, payload, error, match):
    db = RemoteCardsDB("http://cards.test", "sox", "secret-key")
    with pytest.raises(error, match=match):
        db._check(status, payload)


def test_parse_empty_and_non_json():
    assert _parse(b"") is None
    assert _parse(b"<html>Bad Gateway</html>") == "<html>Bad Gateway</html>"


def test_user_agent_names_the_cli_version(server):
    RemoteCardsDB(server, "sox", "secret-key").count()
    assert Handler.user_agents == [f"cards/{cards.__version__}"]
