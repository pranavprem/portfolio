"""Public-only fixtures; browser traffic stays on an ephemeral loopback origin."""

from html.parser import HTMLParser
from pathlib import Path
from threading import Thread

import pytest
from werkzeug.serving import WSGIRequestHandler, make_server

from app import create_app
from app.content import load_story, prepare_story

ROOT = Path(__file__).resolve().parents[1]
STAT_KEYS = ("coding", "enthusiasm", "vitality", "charisma", "experience")
BADGE_IDS = (
    "first-game",
    "house-captain",
    "cs-percentile",
    "hackathon-wins",
    "java-training",
    "green-belt",
    "teaching-assistant",
    "google-internship",
    "release-automation",
    "bots-reliability",
    "principal",
)
# Independent oracle from the approved state table, not computed from runtime JSON.
CHECKPOINTS = (
    (None, (0, 1, 1, 1, 0), 0, "goa", "bright"),
    ("first-script", (1, 6, 8, 2, 1), 1, "goa", "bright"),
    ("school-unlocked", (3, 8, 8, 5, 2), 2, "goa", "bright"),
    ("unexpected-detour", (3, 5, 3, 5, 2), 3, "goa", "quiet"),
    ("college-unlocked", (6, 9, 7, 6, 3), 4, "goa", "bright"),
    ("java-unlocked", (7, 8, 7, 6, 4), 5, "pune", "bright"),
    ("automation-unlocked", (6, 3, 7, 6, 4), 6, "pune", "quiet"),
    ("sjsu-unlocked", (10, 9, 8, 7, 5), 7, "san-jose", "bright"),
    ("developer-ally-unlocked", (8, 10, 8, 7, 5), 8, "san-jose", "bright"),
    ("cloud-unlocked", (8, 9, 8, 7, 6), 9, "bay-area", "bright"),
    ("fog-arrives", (8, 7, 6, 7, 6), 9, "bay-area", "quiet"),
    ("bots-unlocked", (8, 9, 7, 7, 6), 10, "bay-area", "bright"),
    ("continuing-unlocked", (8, 10, 8, 7, 7), 11, "bay-area", "bright"),
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
        if tag == "br":
            self.chunks.append(" ")

    def handle_endtag(self, tag):
        if tag in {"p", "div", "li", "dt", "dd", "h1", "h2", "h3", "section", "article"}:
            self.chunks.append(" ")

    def handle_data(self, data):
        self.chunks.append(data)

    @property
    def text(self):
        return " ".join("".join(self.chunks).split())

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
def quest_targets():
    # Independent narrative order and destinations, not derived from prepared content.
    return {
        "first-script": ("story", 1),
        "school-unlocked": ("story", 2),
        "unexpected-detour": ("story", 3),
        "college-unlocked": ("story", 4),
        "gec-extras": ("discovery", 4),
        "early-projects": ("discovery", 4),
        "java-unlocked": ("story", 5),
        "automation-unlocked": ("story", 6),
        "green-belt": ("discovery", 6),
        "coldplay": ("discovery", 6),
        "sjsu-unlocked": ("story", 7),
        "opportunity-hack": ("discovery", 7),
        "developer-ally-unlocked": ("story", 8),
        "masters": ("discovery", 8),
        "google-tools": ("discovery", 8),
        "cloud-unlocked": ("story", 9),
        "fog-arrives": ("story", 10),
        "bots-unlocked": ("story", 11),
        "continuing-unlocked": ("story", 12),
        "career-titles": ("discovery", 12),
        "awards": ("discovery", 12),
        "epilogue": ("story", 13),
        "off-clock": ("discovery", 13),
        "hobbies": ("discovery", 13),
    }


@pytest.fixture(scope="session")
def discovery_positions():
    return {
        "gec-extras": (249, 99),
        "early-projects": (114.5, 96.5),
        "green-belt": (217, 102.5),
        "coldplay": (70, 84.5),
        "opportunity-hack": (52.5, 96),
        "masters": (52.5, 96),
        "google-tools": (208, 95.5),
        "career-titles": (69, 74),
        "awards": (158, 106.5),
        "off-clock": (77, 100),
        "hobbies": (264, 113),
    }


@pytest.fixture(scope="session")
def home_positions():
    return [(119, 165), (236, 165), (161, 165), (161, 165), (161, 165)]


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
