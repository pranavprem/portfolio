"""Public-only fixtures; browser traffic stays on an ephemeral loopback origin."""

from html.parser import HTMLParser
from pathlib import Path
from threading import Thread

import pytest
from werkzeug.serving import WSGIRequestHandler, make_server

from app import create_app
from app.content import load_story, prepare_story

ROOT = Path(__file__).resolve().parents[1]
STAT_KEYS = ("coding", "enthusiasm", "vitality", "charisma", "automancy", "sidequests")
BADGE_IDS = (
    "first-script",
    "cpp-unlocked",
    "house-captain",
    "python-passport",
    "java-topper",
    "time-returned",
    "cloud-scholar",
    "developer-ally",
    "chat-alchemist",
    "bot-builder",
    "principal",
)
# Independent oracle from the approved state table, not computed from runtime JSON.
CHECKPOINTS = (
    (None, (0, 1, 1, 1, 0, 1), 0, "goa", "bright"),
    ("first-script", (1, 6, 8, 2, 0, 4), 1, "goa", "bright"),
    ("school-unlocked", (3, 8, 8, 6, 1, 6), 3, "goa", "bright"),
    ("unexpected-detour", (3, 4, 4, 4, 1, 3), 3, "goa", "quiet"),
    ("college-unlocked", (6, 9, 7, 8, 4, 8), 4, "goa", "bright"),
    ("java-unlocked", (7, 7, 7, 7, 4, 5), 5, "pune", "bright"),
    ("automation-unlocked", (4, 2, 6, 7, 8, 6), 6, "pune", "quiet"),
    ("sjsu-unlocked", (10, 9, 7, 8, 9, 7), 7, "san-jose", "bright"),
    ("developer-ally-unlocked", (10, 10, 7, 8, 9, 7), 8, "san-jose", "bright"),
    ("cloud-unlocked", (10, 8, 7, 8, 10, 6), 9, "bay-area", "bright"),
    ("fog-arrives", (9, 3, 3, 6, 9, 2), 9, "bay-area", "fog"),
    ("bots-unlocked", (10, 8, 6, 8, 10, 6), 10, "bay-area", "bright"),
    ("continuing-unlocked", (10, 10, 7, 9, 10, 8), 11, "bay-area", "bright"),
)


class HTMLDocument(HTMLParser):
    """Inspect server HTML without adding a DOM/parser dependency to the project."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.chunks = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.chunks.append(data)

    @property
    def text(self):
        return " ".join(" ".join(self.chunks).split())

    def select(self, tag=None, **attributes):
        return [
            attrs
            for name, attrs in self.elements
            if (tag is None or name == tag)
            and all(
                value in attrs.get("class", "").split()
                if key == "class_"
                else attrs.get(key) == value
                for key, value in attributes.items()
            )
        ]


@pytest.fixture(scope="session")
def project_root():
    return ROOT


@pytest.fixture(scope="session")
def stat_keys():
    return STAT_KEYS


@pytest.fixture(scope="session")
def snapshots():
    return [
        {
            "index": index - 1,
            "id": checkpoint,
            "stats": dict(zip(STAT_KEYS, values, strict=True)),
            "badges": list(BADGE_IDS[:count]),
            "region": region,
            "mood": mood,
        }
        for index, (checkpoint, values, count, region, mood) in enumerate(CHECKPOINTS)
    ]


@pytest.fixture
def story_document():
    return load_story()


@pytest.fixture(scope="session")
def game():
    return prepare_story(load_story())[1]


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("PORTFOLIO_ENV", "development")
    monkeypatch.setenv("PORTFOLIO_HSTS", "0")
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def parse_html():
    return HTMLDocument


class SilentRequestHandler(WSGIRequestHandler):
    def log(self, _type, _message, *_args):
        # Even failed synthetic requests must not create request-bearing access logs.
        pass


@pytest.fixture(scope="session")
def live_server():
    with pytest.MonkeyPatch.context() as environment:
        environment.setenv("PORTFOLIO_ENV", "development")
        environment.setenv("PORTFOLIO_HSTS", "0")
        application = create_app({"TESTING": True})
    server = make_server(
        "127.0.0.1", 0, application, threaded=True, request_handler=SilentRequestHandler
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive(), "The loopback browser server did not shut down"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1440, "height": 1000}}
