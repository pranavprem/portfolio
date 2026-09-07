"""Validate the fixed public story and prepare deterministic presentation data."""

import json
import math
import re
from copy import deepcopy
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
CONTENT_PATH = APP_ROOT / "content" / "story.json"
STATIC_ROOT = APP_ROOT / "static"
MAX_CONTENT_BYTES = 128 * 1024
STAT_KEYS = ("coding", "enthusiasm", "vitality", "charisma", "automancy", "sidequests")
REGION_IDS = ("goa", "pune", "san-jose", "bay-area")
MOODS = frozenset({"bright", "quiet", "fog"})
BADGE_ART_KEYS = frozenset(
    {"spark", "flag", "leaf", "cup", "gear", "cloud", "heart", "bolt", "bot", "star"}
)
ASSET_EXTENSIONS = frozenset({".css", ".js", ".svg", ".png", ".webp", ".ico"})
ID_PATTERN = re.compile(r"[a-z][a-z0-9-]{0,63}\Z")


class ContentValidationError(ValueError):
    """A public build input is invalid; correct it before starting the app."""


def _require(condition: bool, field: str, message: str) -> None:
    if not condition:
        raise ContentValidationError(f"{field}: {message}")


def _object(value: object, keys: set[str], field: str) -> None:
    _require(type(value) is dict, field, "expected an object")
    _require(set(value) == keys, field, "use exactly the documented fields")


def _text(value: object, limit: int, field: str) -> None:
    _require(type(value) is str, field, "expected plain text")
    _require(0 < len(value) <= limit and bool(value.strip()), field, f"use 1-{limit} characters")
    _require(
        all(ord(char) >= 32 and ord(char) != 127 for char in value),
        field,
        "remove control characters",
    )


def _id(value: object, field: str) -> None:
    _text(value, 64, field)
    _require(ID_PATTERN.fullmatch(value) is not None, field, "use a lowercase hyphenated ID")


def _list(value: object, minimum: int, maximum: int, field: str) -> None:
    _require(type(value) is list, field, "expected a list")
    _require(minimum <= len(value) <= maximum, field, f"expected {minimum}-{maximum} entries")


def _stats(value: object, field: str) -> None:
    _object(value, set(STAT_KEYS), field)
    for key in STAT_KEYS:
        _require(
            type(value[key]) is int and 0 <= value[key] <= 10,
            f"{field}.{key}",
            "use an integer from 0 to 10",
        )


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        _require(key not in result, "JSON", "remove duplicate object keys")
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    raise ContentValidationError("JSON: nonfinite numbers are not allowed")


def load_story() -> dict:
    """Read only the checked-in JSON; importing this module does not load assets."""
    try:
        with CONTENT_PATH.open("rb") as source:
            raw = source.read(MAX_CONTENT_BYTES + 1)
    except OSError:
        raise ContentValidationError(
            "story.json: restore the readable public content file"
        ) from None
    _require(len(raw) <= MAX_CONTENT_BYTES, "story.json", "keep the document within 128 KiB")
    try:
        document = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_unique_object, parse_constant=_reject_constant
        )
    except ContentValidationError:
        raise
    except (ValueError, UnicodeError, RecursionError):
        raise ContentValidationError("story.json: correct the UTF-8 JSON syntax") from None
    validate_story(document)
    return document


def validate_story(document: object) -> None:
    """Check this release's small authoring schema without executing any content."""
    _object(
        document,
        {
            "schema_version",
            "sources",
            "stat_definitions",
            "initial",
            "badges",
            "regions",
            "chapters",
        },
        "story",
    )
    _require(
        type(document["schema_version"]) is int and document["schema_version"] == 1,
        "schema_version",
        "only version 1 is supported",
    )

    sources = document["sources"]
    _object(sources, {"owner-brief", "resume", "profile", "supplied-documents"}, "sources")
    for source_id, source in sources.items():
        _object(source, {"kind"}, f"sources.{source_id}")
        expected = "owner-supplied" if source_id == "owner-brief" else "supplied-document"
        _require(
            source["kind"] == expected,
            f"sources.{source_id}",
            "retain the documented source classification",
        )

    definitions = document["stat_definitions"]
    _list(definitions, 6, 6, "stat_definitions")
    for index, definition in enumerate(definitions):
        field = f"stat_definitions[{index}]"
        _object(definition, {"key", "label", "compact_label", "description"}, field)
        _require(definition["key"] == STAT_KEYS[index], field, "retain the six-stat display order")
        _text(definition["label"], 64, field + ".label")
        _text(definition["compact_label"], 64, field + ".compact_label")
        _text(definition["description"], 220, field + ".description")

    badges = document["badges"]
    _list(badges, 11, 11, "badges")
    badge_ids = set()
    for index, badge in enumerate(badges):
        field = f"badges[{index}]"
        _object(badge, {"id", "label", "description", "art_key"}, field)
        _id(badge["id"], field + ".id")
        _require(badge["id"] not in badge_ids, field, "badge IDs must be unique")
        badge_ids.add(badge["id"])
        _text(badge["label"], 64, field + ".label")
        _text(badge["description"], 220, field + ".description")
        _id(badge["art_key"], field + ".art_key")
        _require(badge["art_key"] in BADGE_ART_KEYS, field, "choose an approved badge icon key")

    regions = document["regions"]
    _list(regions, 4, 4, "regions")
    region_map = {}
    for index, region in enumerate(regions):
        field = f"regions[{index}]"
        _object(region, {"id", "label", "art_key", "width", "height", "landmarks"}, field)
        _require(region["id"] == REGION_IDS[index], field, "retain the four-region order")
        _require(region["art_key"] == region["id"], field, "region art keys must match region IDs")
        _text(region["label"], 64, field + ".label")
        for dimension, expected in (("width", 320), ("height", 180)):
            _require(
                type(region[dimension]) is int and region[dimension] == expected,
                field,
                "region art uses a 320 by 180 viewBox",
            )
        landmarks = region["landmarks"]
        _require(
            type(landmarks) is dict and 1 <= len(landmarks) <= 12, field, "provide 1-12 landmarks"
        )
        for landmark_id, position in landmarks.items():
            _id(landmark_id, field + ".landmark_id")
            _object(position, {"x", "y"}, field + ".position")
            for axis in ("x", "y"):
                coordinate = position[axis]
                limit = region["width" if axis == "x" else "height"]
                _require(
                    type(coordinate) in (int, float)
                    and 0 <= coordinate <= limit
                    and math.isfinite(coordinate),
                    field,
                    "landmarks must be finite coordinates inside the viewBox",
                )
            _require(
                20 <= position["x"] <= 300,
                field,
                "leave room for the traveler and companion at both edges",
            )
        region_map[region["id"]] = region

    initial = document["initial"]
    _object(initial, {"stats", "badges", "region_id", "landmark_id", "mood"}, "initial")
    _stats(initial["stats"], "initial.stats")
    _require(
        tuple(initial["stats"][key] for key in STAT_KEYS) == (0, 1, 1, 1, 0, 1),
        "initial.stats",
        "retain the low opening snapshot: 0, 1, 1, 1, 0, 1",
    )
    _require(initial["badges"] == [], "initial.badges", "the opening has no badges")
    _require(
        initial["region_id"] == "goa" and initial["mood"] == "bright",
        "initial",
        "open in bright Goa",
    )
    _id(initial["landmark_id"], "initial.landmark_id")
    _require(
        initial["landmark_id"] in region_map["goa"]["landmarks"], "initial", "choose a Goa landmark"
    )

    chapters = document["chapters"]
    _list(chapters, 11, 11, "chapters")
    chapter_ids, card_ids, granted = set(), set(), set()
    ordered_grants = []
    for index, chapter in enumerate(chapters):
        field = f"chapters[{index}]"
        _object(chapter, {"id", "region_id", "period_label", "heading", "cards"}, field)
        _id(chapter["id"], field + ".id")
        _require(chapter["id"] not in chapter_ids, field, "chapter IDs must be unique")
        chapter_ids.add(chapter["id"])
        _id(chapter["region_id"], field + ".region_id")
        _require(chapter["region_id"] in region_map, field, "choose a known region")
        _text(chapter["period_label"], 64, field + ".period_label")
        _text(chapter["heading"], 100, field + ".heading")
        count = 2 if index == 8 else 1
        _list(chapter["cards"], count, count, field + ".cards")
        for card_index, card in enumerate(chapter["cards"]):
            card_field = f"{field}.cards[{card_index}]"
            _object(card, {"id", "heading", "body", "facts", "source_refs", "event"}, card_field)
            _id(card["id"], card_field + ".id")
            _require(card["id"] not in card_ids, card_field, "card IDs must be unique")
            card_ids.add(card["id"])
            _text(card["heading"], 100, card_field + ".heading")
            _text(card["body"], 600, card_field + ".body")
            _list(card["facts"], 0, 3, card_field + ".facts")
            for fact in card["facts"]:
                _text(fact, 220, card_field + ".facts")
            _list(card["source_refs"], 1, 4, card_field + ".source_refs")
            for source_id in card["source_refs"]:
                _id(source_id, card_field + ".source_refs")
                _require(source_id in sources, card_field, "reference a documented source")
            _require(
                len(set(card["source_refs"])) == len(card["source_refs"]),
                card_field,
                "source references must be unique",
            )
            event = card["event"]
            _object(
                event, {"stats_after", "grant_badges", "landmark_id", "mood"}, card_field + ".event"
            )
            _stats(event["stats_after"], card_field + ".stats_after")
            _id(event["mood"], card_field + ".mood")
            _require(event["mood"] in MOODS, card_field, "choose an approved scene mood")
            _id(event["landmark_id"], card_field + ".landmark_id")
            _require(
                event["landmark_id"] in region_map[chapter["region_id"]]["landmarks"],
                card_field,
                "choose a landmark in this chapter's region",
            )
            _list(event["grant_badges"], 0, 11, card_field + ".grant_badges")
            for badge_id in event["grant_badges"]:
                _id(badge_id, card_field + ".grant_badges")
                _require(
                    badge_id in badge_ids and badge_id not in granted,
                    card_field,
                    "grant each known badge only once",
                )
                granted.add(badge_id)
                ordered_grants.append(badge_id)
    _require(
        ordered_grants == [badge["id"] for badge in badges],
        "badges",
        "order the ledger by first grant and grant every badge",
    )


def prepare_story(document: dict) -> tuple[dict, dict]:
    """Preserve authored fields; add accessible snapshots and a prose-free game projection."""
    story = deepcopy(document)
    regions = {region["id"]: region for region in story["regions"]}
    badges = {badge["id"]: badge for badge in story["badges"]}
    initial = story["initial"]
    game = {
        "schema_version": story["schema_version"],
        "initial": {
            "stats": dict(initial["stats"]),
            "badges": [],
            "region_id": initial["region_id"],
            "position": dict(regions[initial["region_id"]]["landmarks"][initial["landmark_id"]]),
            "mood": initial["mood"],
        },
        "events": [],
    }
    earned = []
    for chapter in story["chapters"]:
        for card in chapter["cards"]:
            event = card["event"]
            earned.extend(event["grant_badges"])
            card["stats"] = [
                {
                    "key": stat["key"],
                    "label": stat["label"],
                    "value": event["stats_after"][stat["key"]],
                }
                for stat in story["stat_definitions"]
            ]
            card["earned_badges"] = [dict(badges[badge_id]) for badge_id in event["grant_badges"]]
            game["events"].append(
                {
                    "id": card["id"],
                    "chapter_id": chapter["id"],
                    "region_id": chapter["region_id"],
                    "position": dict(
                        regions[chapter["region_id"]]["landmarks"][event["landmark_id"]]
                    ),
                    "mood": event["mood"],
                    "stats_after": dict(event["stats_after"]),
                    "badges_after": list(earned),
                }
            )
    return story, game


def build_asset_inventory(static_root: Path = STATIC_ROOT) -> frozenset[str]:
    """Reject unsafe build inputs rather than making the static tree a catch-all."""
    _require(
        not static_root.is_symlink() and static_root.is_dir(),
        "static",
        "restore the original static directory",
    )
    root = static_root.resolve()
    inventory = set()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        _require(not path.is_symlink(), "static", "remove symlink assets")
        _require(
            not any(part.startswith(".") for part in relative.parts),
            "static",
            "remove hidden files and directories",
        )
        _require(
            path.resolve().is_relative_to(root),
            "static",
            "assets must remain inside the static directory",
        )
        if path.is_dir():
            continue
        _require(
            path.is_file() and path.suffix.lower() in ASSET_EXTENSIONS,
            "static",
            "use only approved regular CSS, JS, SVG, PNG, WebP, or ICO files",
        )
        inventory.add(relative.as_posix())
    return frozenset(inventory)
