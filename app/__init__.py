"""A read-only, server-rendered autobiography with local progressive enhancement."""

import os
import sys
from collections.abc import Mapping
from uuid import uuid4

from flask import Flask, abort, jsonify, render_template, request, send_from_directory
from gunicorn.glogging import Logger
from werkzeug.exceptions import HTTPException

from .content import (
    APP_ROOT,
    STATIC_ROOT,
    ContentValidationError,
    build_asset_inventory,
    load_story,
    prepare_story,
)

SECURITY_HEADERS = {
    "Content-Security-Policy": "; ".join(
        (
            "default-src 'none'",
            "script-src 'self'",
            "script-src-attr 'none'",
            "style-src 'self'",
            "style-src-attr 'none'",
            "img-src 'self'",
            "font-src 'self'",
            "connect-src 'none'",
            "object-src 'none'",
            "base-uri 'none'",
            "frame-ancestors 'none'",
            "form-action 'none'",
            "frame-src 'none'",
            "worker-src 'none'",
            "media-src 'none'",
        )
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    "Cross-Origin-Resource-Policy": "same-origin",
}


class SafeGunicornLogger(Logger):
    def exception(self, _message, *_args, **_kwargs) -> None:
        # Gunicorn otherwise includes request URIs and exception text in worker failures.
        self.error_log.error(
            "worker_failure category=%s correlation_id=%s",
            type(sys.exception()).__name__,
            uuid4().hex,
        )


class PortfolioFlask(Flask):
    def log_exception(self, exc_info) -> None:
        # Flask's default traceback includes exception strings and request paths.
        self.logger.error(
            "application_failure category=%s correlation_id=%s",
            type(exc_info[1]).__name__,
            uuid4().hex,
        )


def create_app(test_config: Mapping[str, object] | None = None) -> Flask:
    app = PortfolioFlask(__name__, static_folder=None, template_folder=str(APP_ROOT / "templates"))
    hsts = os.environ.get("PORTFOLIO_HSTS", "0")
    if hsts not in {"0", "1"}:
        raise ValueError(
            "PORTFOLIO_HSTS must be 0 or 1; enable only after public TLS verification."
        )
    app.config.from_mapping(
        PORTFOLIO_ENV=os.environ.get("PORTFOLIO_ENV", "development"),
        PORTFOLIO_HSTS=hsts == "1",
        CANONICAL_URL="https://pranavprem.com/",
        MAX_CONTENT_LENGTH=1024,
        DEBUG=False,
        PROPAGATE_EXCEPTIONS=False,
        PROVIDE_AUTOMATIC_OPTIONS=False,
    )
    if test_config is not None:
        app.config.update(test_config)
    mode = app.config["PORTFOLIO_ENV"]
    if mode not in ("development", "production"):
        raise ValueError("PORTFOLIO_ENV must be development or production.")
    if type(app.config["PORTFOLIO_HSTS"]) is not bool:
        raise ValueError("PORTFOLIO_HSTS test configuration must be a boolean.")
    app.config["TRUSTED_HOSTS"] = ["pranavprem.com", "127.0.0.1"]
    if mode == "development":
        app.config["TRUSTED_HOSTS"].append("localhost")
    app.url_map.merge_slashes = False

    document = load_story()
    assets = build_asset_inventory()
    required_assets = {"story.css", "story.js"} | {
        f"art/{region['art_key']}.svg" for region in document["regions"]
    }
    missing = required_assets - assets
    if missing:
        raise ContentValidationError(
            "static: restore required assets: " + ", ".join(sorted(missing))
        )
    story, game = prepare_story(document)
    for template in ("base.html", "index.html", "error.html"):
        app.jinja_env.get_template(template)
    app.extensions["portfolio"] = {"story": story, "game": game, "assets": assets}

    @app.before_request
    def check_request_size():
        # GET bodies are never read, so Flask's lazy body limit alone is insufficient.
        if (
            request.content_length is not None
            and request.content_length > app.config["MAX_CONTENT_LENGTH"]
        ):
            abort(413)

    @app.after_request
    def secure_response(response):
        response.headers.update(SECURITY_HEADERS)
        response.headers.setdefault("Cache-Control", "no-store")
        if mode == "production" and app.config["PORTFOLIO_HSTS"]:
            response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response

    @app.get("/")
    def index():
        return (
            render_template("index.html", story=story, game=game),
            200,
            {"Cache-Control": "no-cache"},
        )

    @app.get("/healthz")
    def health():
        return jsonify(status="ok"), 200, {"Cache-Control": "no-store"}

    @app.get("/static/<path:filename>", endpoint="static")
    def static_asset(filename):
        if filename not in assets:
            abort(404)
        return send_from_directory(STATIC_ROOT, filename, conditional=True, max_age=3600)

    @app.errorhandler(HTTPException)
    def http_error(error):
        messages = {
            400: ("Request unavailable", "This request could not be accepted."),
            404: (
                "A different trail",
                "That trail is not on this map. The story begins at pranavprem.com.",
            ),
            405: ("Method unavailable", "This page accepts GET and HEAD requests only."),
            413: (
                "Request too large",
                "This request is too large. Request the page without a body.",
            ),
            500: ("A quiet pause", "The story could not load. Try reloading later."),
        }
        title, message = messages.get(
            error.code, ("Request unavailable", "This request could not be accepted.")
        )
        response = error.get_response()
        response.set_data(
            render_template("error.html", status_code=error.code, title=title, message=message)
        )
        response.content_type = "text/html; charset=utf-8"
        response.headers["Cache-Control"] = "no-store"
        return response

    return app
