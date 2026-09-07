"""Read-only HTTP surface, inert rendering, bounded errors, and privacy checks."""

import json
import logging
import re

import pytest
from flask import render_template

from app import SafeGunicornLogger, create_app
from app.content import prepare_story, validate_story


def assert_security_headers(response):
    policy = dict(
        directive.strip().split(" ", 1)
        for directive in response.headers["Content-Security-Policy"].split(";")
    )
    assert policy == {
        "default-src": "'none'",
        "script-src": "'self'",
        "script-src-attr": "'none'",
        "style-src": "'self'",
        "style-src-attr": "'none'",
        "img-src": "'self'",
        "font-src": "'self'",
        "connect-src": "'none'",
        "object-src": "'none'",
        "base-uri": "'none'",
        "frame-ancestors": "'none'",
        "form-action": "'none'",
        "frame-src": "'none'",
        "worker-src": "'none'",
        "media-src": "'none'",
    }
    for header, value in {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
        "Cross-Origin-Resource-Policy": "same-origin",
    }.items():
        assert response.headers[header] == value
    assert "Set-Cookie" not in response.headers
    assert not any(name.lower().startswith("access-control-") for name in response.headers.keys())


@pytest.mark.parametrize(
    ("path", "mimetype", "cache"),
    [
        ("/", "text/html", "no-cache"),
        ("/healthz", "application/json", "no-store"),
        ("/static/story.css", "text/css", "public, max-age=3600"),
        ("/static/art/goa.svg", "image/svg+xml", "public, max-age=3600"),
    ],
)
def test_get_and_head_contract(client, path, mimetype, cache):
    response = client.get(path)
    head = client.head(path)
    assert response.status_code == head.status_code == 200
    assert response.mimetype == head.mimetype == mimetype
    assert response.headers["Cache-Control"] == head.headers["Cache-Control"] == cache
    assert response.data
    assert head.data == b""
    assert head.content_length == response.content_length
    assert_security_headers(response)
    assert_security_headers(head)
    assert "Strict-Transport-Security" not in response.headers


def test_health_is_minimal_and_assets_have_conditional_caching(client, app):
    assert client.get("/healthz").data == b'{"status":"ok"}\n'
    for name in app.extensions["portfolio"]["assets"]:
        path = f"/static/{name}"
        response = client.get(path)
        assert response.status_code == 200
        assert "immutable" not in response.headers["Cache-Control"]
        assert response.headers["Last-Modified"]
        cached = client.get(path, headers={"If-None-Match": response.headers["ETag"]})
        assert cached.status_code == 304
        assert cached.data == b""
        assert_security_headers(cached)
    assert client.get("/static/story.js").mimetype in {"text/javascript", "application/javascript"}


@pytest.mark.parametrize(
    "method", ["POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE", "CONNECT"]
)
def test_only_get_and_head_are_allowed(client, method):
    for path in ("/", "/healthz", "/static/story.js"):
        response = client.open(path, method=method)
        assert response.status_code == 405
        assert {part.strip() for part in response.headers["Allow"].split(",")} == {"GET", "HEAD"}
        assert response.headers["Cache-Control"] == "no-store"
        assert_security_headers(response)


@pytest.mark.parametrize(
    "path",
    [
        "/unknown",
        "/story.json",
        "/app/content/story.json",
        "/content/story.json",
        "/docs/story.md",
        "/README.md",
        "/.git/config",
        "/.env",
        "/run/secrets/synthetic",
        "/private.PDF",
        "/static/",
        "/static/art/",
        "/static/missing.svg",
        "/static/story.js.map",
        "/static/.env",
        "/static/private.pdf",
        "/static/../content/story.json",
        "/static/%2e%2e/content/story.json",
        "/static/%252e%252e/content/story.json",
        "/static/..%2f..%2fREADME.md",
        "/static/%2e%2e%5ccontent%5cstory.json",
        "/static/story.js%00.svg",
    ],
)
def test_private_sources_and_traversal_are_not_served(client, path):
    response = client.get(path, query_string={"canary": "synthetic-private-marker"})
    assert response.status_code == 404
    assert response.headers["Cache-Control"] == "no-store"
    assert b"synthetic-private-marker" not in response.data
    assert b"That trail is not on this map" in response.data
    assert_security_headers(response)


@pytest.mark.parametrize(
    "host", ["evil.invalid", "pranavprem.com.evil.invalid", "www.pranavprem.com", "app", "[::1]"]
)
def test_invalid_hosts_are_rejected_without_reflection(client, host):
    response = client.get("/", headers={"Host": host})
    assert response.status_code == 400
    assert host.encode() not in response.data
    assert_security_headers(response)


@pytest.mark.parametrize("size", [0, 1024, 1025, 100_000])
def test_declared_body_limit_is_enforced_even_for_unread_get(client, size):
    for path in ("/", "/healthz", "/static/story.css"):
        response = client.get(path, environ_overrides={"CONTENT_LENGTH": str(size)})
        assert response.status_code == (413 if size > 1024 else 200)
        assert_security_headers(response)
    response = client.head("/", environ_overrides={"CONTENT_LENGTH": str(size)})
    assert response.status_code == (413 if size > 1024 else 200)
    assert response.data == b""


def test_queries_and_forwarded_headers_cannot_customize_output(client, parse_html, caplog):
    plain = client.get("/")
    response = client.get(
        "/",
        query_string={
            "template": "<script>synthetic-marker</script>",
            "url": "https://evil.invalid",
        },
        headers={
            "Forwarded": 'host="evil.invalid";proto=https;for=192.0.2.5',
            "X-Forwarded-Host": "evil.invalid",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-For": "192.0.2.5",
            "Origin": "https://evil.invalid",
            "Referer": "https://evil.invalid/synthetic-marker",
        },
    )
    assert response.status_code == 200
    assert response.data == plain.data
    assert "Location" not in response.headers
    document = parse_html(response.get_data(as_text=True))
    assert document.select("link", rel="canonical") == [
        {"rel": "canonical", "href": "https://pranavprem.com/"}
    ]
    assert "synthetic-marker" not in caplog.text
    assert "evil.invalid" not in caplog.text
    assert (
        client.get(
            "/", headers={"Host": "evil.invalid", "X-Forwarded-Host": "pranavprem.com"}
        ).status_code
        == 400
    )


@pytest.mark.parametrize(
    ("mode", "hsts", "expected"),
    [
        ("development", False, None),
        ("development", True, None),
        ("production", False, None),
        ("production", True, "max-age=31536000"),
    ],
)
def test_production_hosts_and_opt_in_hsts(app, mode, hsts, expected):
    client = create_app({"PORTFOLIO_ENV": mode, "PORTFOLIO_HSTS": hsts}).test_client()
    for path in ("/", "/healthz", "/static/story.js", "/missing"):
        response = client.get(path, base_url="http://pranavprem.com")
        assert response.status_code == (404 if path == "/missing" else 200)
        assert response.headers.get("Strict-Transport-Security") == expected
        assert "Location" not in response.headers
        assert_security_headers(response)
    assert client.get("/", base_url="http://127.0.0.1").status_code == 200
    assert client.get("/", base_url="http://localhost").status_code == (
        200 if mode == "development" else 400
    )


@pytest.mark.parametrize(
    ("name", "value"), [("PORTFOLIO_ENV", "local"), ("PORTFOLIO_HSTS", "true")]
)
def test_invalid_environment_fails_startup(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(ValueError, match=name):
        create_app()


def test_unexpected_error_is_generic_and_logs_are_sanitized(app, caplog, parse_html):
    def fail():
        raise RuntimeError("synthetic-sensitive-marker /run/secrets/synthetic")

    app.view_functions["index"] = fail
    with caplog.at_level(logging.ERROR):
        response = app.test_client().get(
            "/?synthetic-query", headers={"X-Canary": "synthetic-header"}
        )
    assert response.status_code == 500
    assert (
        "The story could not load. Try reloading later."
        in parse_html(response.get_data(as_text=True)).text
    )
    assert_security_headers(response)
    assert re.search(
        r"application_failure category=RuntimeError correlation_id=[a-f0-9]{32}", caplog.text
    )
    for canary in (
        "synthetic-sensitive-marker",
        "synthetic-query",
        "synthetic-header",
        "/run/secrets",
        "Traceback",
    ):
        assert canary not in caplog.text
        assert canary.encode() not in response.data
    assert all(record.exc_info is None for record in caplog.records)


def test_gunicorn_exception_logger_does_not_expand_request_or_exception(caplog):
    logger = object.__new__(SafeGunicornLogger)
    logger.error_log = logging.getLogger("synthetic-gunicorn")
    try:
        raise RuntimeError("synthetic-sensitive-marker")
    except RuntimeError:
        logger.exception("Failure on /synthetic-request: %s", "synthetic-header")
    assert re.search(
        r"worker_failure category=RuntimeError correlation_id=[a-f0-9]{32}", caplog.text
    )
    for canary in ("synthetic-sensitive-marker", "synthetic-request", "synthetic-header"):
        assert canary not in caplog.text
    assert all(record.exc_info is None for record in caplog.records)


def test_server_html_is_complete_semantic_and_noninteractive(
    client, story_document, game, parse_html
):
    document = parse_html(client.get("/").get_data(as_text=True))
    assert document.select("html")[0]["lang"] == "en"
    assert len(document.select("h1")) == len(document.select("main")) == 1
    assert len(document.select("section", class_="chapter")) == 11
    assert len(document.select("article", class_="story-card")) == 12
    assert len(document.select(class_="chapter-snapshot")) == 12
    assert len(document.select("h3")) == 12
    assert len(document.select(class_="loot")) == 10
    assert json.loads(document.select(id="journey")[0]["data-game"]) == game
    for chapter in story_document["chapters"]:
        assert chapter["heading"] in document.text
        assert chapter["period_label"] in document.text
        for card in chapter["cards"]:
            assert card["body"] in document.text
            assert all(fact in document.text for fact in card["facts"])
    for badge in story_document["badges"]:
        assert badge["description"] in document.text
    slots = [attrs for _, attrs in document.elements if "data-badge" in attrs]
    assert len(slots) == 11
    assert all(attrs.get("aria-hidden") == "true" and "aria-label" not in attrs for attrs in slots)
    assert all("earned" not in attrs.get("class", "").split() for attrs in slots)
    assert document.select(id="character-sheet")[0]["aria-live"] == "off"
    assert "Opening stats; chapter snapshots follow." in document.text
    for tag, attrs in document.elements:
        assert tag not in {
            "a",
            "button",
            "input",
            "select",
            "textarea",
            "form",
            "iframe",
            "object",
            "embed",
            "style",
            "base",
        }
        assert not any(name.startswith("on") for name in attrs)
        assert "tabindex" not in attrs and "style" not in attrs
        assert attrs.get("role") not in {"button", "link", "application", "slider", "menu"}
        for name in ("src", "href"):
            if name in attrs and attrs.get("rel") != "canonical":
                assert attrs[name].startswith("/static/")
    assert document.select("script") == [{"type": "module", "src": "/static/story.js"}]


def test_hostile_text_and_projection_remain_inert(app, story_document, parse_html):
    payload = '"><img src=x onerror=alert(1)></script><script>alert(2)</script>&{{7*7}}'
    card = story_document["chapters"][0]["cards"][0]
    card.update(body=payload, heading=payload, facts=[payload])
    validate_story(story_document)
    story, game = prepare_story(story_document)
    # Even impossible authored IDs must be safely serialized by the template boundary.
    game["events"][0]["id"] = payload
    with app.test_request_context("/"):
        source = render_template("index.html", story=story, game=game)
    document = parse_html(source)
    assert payload in document.text
    assert payload not in source
    assert json.loads(document.select(id="journey")[0]["data-game"]) == game
    assert document.select("script") == [{"type": "module", "src": "/static/story.js"}]
    assert not document.select("img", src="x")
    assert not any(name.startswith("on") for _, attrs in document.elements for name in attrs)


def test_rendered_source_claims_keep_authorized_scope(client, parse_html):
    text = parse_html(client.get("/").get_data(as_text=True)).text
    assert re.search(r"I scored 110%, the maximum possible.*I.*only student", text)
    assert re.search(r"top 0\.01% nationally in Class 12 computer science", text)
    assert re.search(r"IEEE Xtreme national top[- ]ten", text)
    assert "I joined Salesforce in 2019" in text
    assert re.search(r"Jun-Aug 2018.*Google Hardware/Nest, during my MS", text)
    for invention in (
        r"extra[- ]credit",
        r"out of 100",
        r"all-time university record",
        r"IEEE Xtreme.{0,30}(?:seventh|eighth|7th|8th)",
        r"(?:Jan(?:uary)?|Mar(?:ch)?) 2019",
        r"(?:GRE|TOEFL)\s+(?:score[: ]*)?\d{2,3}",
    ):
        assert not re.search(invention, text, re.I), invention
    document = parse_html(client.get("/").get_data(as_text=True))
    # Include template callouts and badge descriptions, not just JSON fact lines.
    for match in re.finditer(r"2,?000\s*\+", document.text):
        context = document.text[max(0, match.start() - 90) : match.end() + 100]
        assert "Green Belt" in context
        assert "TasKing" not in context
    for phrase in (
        "enthusiasm, drive, knowledge",
        "understanding of my team",
        "all-time high",
        "not a medical chart or a skills assessment",
    ):
        assert phrase in text
