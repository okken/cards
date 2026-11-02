"""
RemoteCardsDB's HTTP layer, against a tiny local server.
"""
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
from cards.remote import RemoteCardsDB, RemoteError


class Handler(BaseHTTPRequestHandler):
    seen = []

    def _reply(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.seen.append(("GET", self.path, self.headers["Authorization"], None))
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
    httpd = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()


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
