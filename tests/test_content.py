"""Authoring, source-integrity, projection, and public static-input contracts."""

import json
import re
from copy import deepcopy
from xml.etree import ElementTree

import pytest

import app as application
import app.content as content
from app.content import ContentValidationError, build_asset_inventory, prepare_story, validate_story


def test_release_structure_and_exact_snapshots(story_document, snapshots, stat_keys):
    story, game = prepare_story(story_document)
    assert story["schema_version"] == game["schema_version"] == 2
    chapters = story["chapters"]
    cards = [card for chapter in chapters for card in chapter["cards"]]
    assert len(chapters) == 11
    assert [len(chapter["cards"]) for chapter in chapters] == [1] * 8 + [2, 1, 1]
    assert len(cards) == len(game["events"]) == 12
    assert [card["id"] for card in cards] == [state["id"] for state in snapshots[1:]]
    assert [badge["id"] for badge in story["badges"]] == snapshots[-1]["badges"]
    assert [region["id"] for region in story["regions"]] == ["goa", "pune", "san-jose", "bay-area"]
    assert tuple(stat["key"] for stat in story["stat_definitions"]) == stat_keys
    health = story["stat_definitions"][2]
    assert (health["key"], health["label"], health["compact_label"]) == ("vitality", "Health", "HP")
    assert game["initial"]["stats"] == snapshots[0]["stats"]
    assert game["initial"]["badges"] == []
    for card, event, expected in zip(cards, game["events"], snapshots[1:], strict=True):
        assert event["id"] == expected["id"]
        assert event["stats_after"] == expected["stats"]
        assert event["badges_after"] == expected["badges"]
        assert (event["region_id"], event["mood"]) == (expected["region"], expected["mood"])
        assert {stat["key"]: stat["value"] for stat in card["stats"]} == expected["stats"]
        assert [badge["id"] for badge in card["earned_badges"]] == card["event"]["grant_badges"]
    assert game["events"][8]["badges_after"] == game["events"][9]["badges_after"]


def test_projection_is_prose_free_and_does_not_alias_input(story_document):
    original = deepcopy(story_document)
    story, game = prepare_story(story_document)
    assert story_document == original
    assert set(game) == {"schema_version", "initial", "events"}
    assert set(game["initial"]) == {"stats", "badges", "region_id", "position", "mood"}
    regions = {region["id"]: region for region in story["regions"]}
    cards = [card for chapter in story["chapters"] for card in chapter["cards"]]
    for card, event in zip(cards, game["events"], strict=True):
        assert set(event) == {
            "id",
            "chapter_id",
            "region_id",
            "position",
            "mood",
            "stats_after",
            "badges_after",
        }
        assert (
            event["position"]
            == regions[event["region_id"]]["landmarks"][card["event"]["landmark_id"]]
        )
    game["events"][1]["badges_after"].clear()
    game["events"][0]["stats_after"]["coding"] = 10
    game["initial"]["position"]["x"] = 100
    story["chapters"][0]["cards"][0]["body"] = "Synthetic edit"
    assert len(game["events"][2]["badges_after"]) == 3
    assert story_document == original


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("schema_version",), True),
        (("schema_version",), 1),
        (("schema_version",), 3),
        (("sources", "profile", "kind"), "independently-verified"),
        (("stat_definitions", 0, "key"), "health"),
        (("initial", "stats", "coding"), 1),
        (("initial", "badges"), ["first-game"]),
        (("initial", "region_id"), "pune"),
        (("initial", "mood"), "quiet"),
        (("initial", "landmark_id"), "missing"),
        (("badges", 1, "id"), "first-game"),
        (("badges", 0, "art_key"), "unapproved"),
        (("regions", 0, "art_key"), "../private"),
        (("regions", 0, "width"), 320.0),
        (("regions", 0, "height"), True),
        (("regions", 0, "landmarks", "home", "x"), 19),
        (("regions", 0, "landmarks", "home", "x"), 301),
        (("regions", 0, "landmarks", "home", "y"), -1),
        (("regions", 0, "landmarks", "home", "y"), 181),
        (("regions", 0, "landmarks", "home", "y"), True),
        (("regions", 0, "landmarks", "home", "y"), float("nan")),
        (("regions", 0, "landmarks", "home", "y"), float("inf")),
        (("chapters", 1, "id"), "spawn"),
        (("chapters", 0, "region_id"), "unknown"),
        (("chapters", 0, "cards", 0, "id"), "Bad ID"),
        (("chapters", 1, "cards", 0, "id"), "first-script"),
        (("chapters", 0, "cards", 0, "body"), "x" * 601),
        (("chapters", 0, "cards", 0, "body"), " \t "),
        (("chapters", 0, "cards", 0, "body"), "text\x7f"),
        (("chapters", 0, "cards", 0, "heading"), "x" * 101),
        (("chapters", 0, "cards", 0, "facts"), ["x"] * 4),
        (("chapters", 0, "cards", 0, "facts"), ["x" * 221]),
        (("chapters", 0, "cards", 0, "source_refs"), []),
        (("chapters", 0, "cards", 0, "source_refs"), ["private-pdf"]),
        (("chapters", 0, "cards", 0, "source_refs"), ["profile", "profile"]),
        (("chapters", 0, "cards", 0, "event", "mood"), "battle"),
        (("chapters", 0, "cards", 0, "event", "landmark_id"), "hardware-lab"),
        (("chapters", 0, "cards", 0, "event", "grant_badges"), ["unknown"]),
        (("chapters", 0, "cards", 0, "event", "grant_badges"), ["first-game"] * 2),
        (("chapters", 1, "cards", 0, "event", "grant_badges"), ["first-game"]),
    ],
)
def test_invalid_authored_fields_are_rejected(story_document, path, value):
    target = story_document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ContentValidationError):
        validate_story(story_document)


@pytest.mark.parametrize("value", [True, False, -1, 11, 1.0, "3", None])
def test_stats_reject_invalid_numbers_without_clamping(story_document, value):
    story_document["chapters"][0]["cards"][0]["event"]["stats_after"]["coding"] = value
    with pytest.raises(ContentValidationError, match="integer from 0 to 10"):
        validate_story(story_document)


@pytest.mark.parametrize(
    "path",
    [
        (),
        ("initial",),
        ("sources", "profile"),
        ("stat_definitions", 0),
        ("badges", 0),
        ("regions", 0),
        ("regions", 0, "landmarks", "home"),
        ("chapters", 0),
        ("chapters", 0, "cards", 0),
        ("chapters", 0, "cards", 0, "event"),
        ("chapters", 0, "cards", 0, "event", "stats_after"),
    ],
)
def test_unknown_and_missing_keys_are_rejected(story_document, path):
    target = story_document
    for key in path:
        target = target[key]
    original = deepcopy(target)
    target["unexpected"] = "synthetic"
    with pytest.raises(ContentValidationError, match="documented fields"):
        validate_story(story_document)
    target.clear()
    target.update(original)
    target.pop(next(iter(target)))
    with pytest.raises(ContentValidationError, match="documented fields"):
        validate_story(story_document)


@pytest.mark.parametrize("key", ["chapters", "badges", "regions", "stat_definitions"])
def test_release_counts_cannot_be_relaxed(story_document, key):
    story_document[key].pop()
    with pytest.raises(ContentValidationError):
        validate_story(story_document)


def test_card_count_and_ledger_order_are_authoritative(story_document):
    invalid = deepcopy(story_document)
    invalid["chapters"][8]["cards"].pop()
    with pytest.raises(ContentValidationError):
        validate_story(invalid)
    story_document["badges"].reverse()
    with pytest.raises(ContentValidationError, match="first grant"):
        validate_story(story_document)


def test_text_and_geometry_limits_are_inclusive(story_document):
    card = story_document["chapters"][0]["cards"][0]
    card.update(body="x" * 600, heading="x" * 100, facts=["x" * 220])
    story_document["stat_definitions"][0]["label"] = "x" * 64
    story_document["regions"][0]["landmarks"]["home"] = {"x": 20, "y": 0}
    story_document["regions"][0]["landmarks"]["school"] = {"x": 300, "y": 180}
    validate_story(story_document)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"schema_version":2,"schema_version":2}',
        b'{"outer":{"x":1,"x":2}}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":-Infinity}',
        b"\xff",
        b"{",
        b"[]",
        b"[" * 2000 + b"]" * 2000,
        b" " * (128 * 1024 + 1),
    ],
    ids=[
        "duplicate-root",
        "duplicate-nested",
        "nan",
        "infinity",
        "negative-infinity",
        "utf8",
        "syntax",
        "root-type",
        "recursion",
        "size",
    ],
)
def test_loader_rejects_bad_json(monkeypatch, tmp_path, raw):
    path = tmp_path / "synthetic.json"
    path.write_bytes(raw)
    monkeypatch.setattr(content, "CONTENT_PATH", path)
    with pytest.raises(ContentValidationError):
        content.load_story()


def test_loader_accepts_exact_byte_limit_and_handles_missing_file(
    story_document, monkeypatch, tmp_path
):
    path = tmp_path / "synthetic.json"
    raw = json.dumps(story_document).encode()
    path.write_bytes(raw + b" " * (content.MAX_CONTENT_BYTES - len(raw)))
    monkeypatch.setattr(content, "CONTENT_PATH", path)
    assert content.load_story() == story_document
    path.unlink()
    with pytest.raises(ContentValidationError, match="restore the readable public content file"):
        content.load_story()


@pytest.mark.parametrize(
    "name", [".hidden.css", ".private/asset.svg", "notes.txt", "source.json", "private.PDF"]
)
def test_inventory_rejects_unapproved_files(tmp_path, name):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("synthetic fixture", encoding="utf-8")
    with pytest.raises(ContentValidationError):
        build_asset_inventory(tmp_path)


@pytest.mark.parametrize("kind", ["file", "directory", "root", "broken"])
def test_inventory_rejects_symlinks(tmp_path, kind):
    root = tmp_path / "static"
    root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "synthetic.svg").write_text("<svg/>", encoding="utf-8")
    if kind == "root":
        link = tmp_path / "linked-static"
        link.symlink_to(root, target_is_directory=True)
        root = link
    else:
        target = outside if kind == "directory" else outside / "synthetic.svg"
        if kind == "broken":
            target = outside / "absent.svg"
        (root / "linked.svg").symlink_to(target, target_is_directory=kind == "directory")
    with pytest.raises(ContentValidationError):
        build_asset_inventory(root)


def test_static_inventory_and_original_svg_safety():
    inventory = build_asset_inventory()
    assert inventory == frozenset(
        {
            "story.css",
            "story.js",
            "art/favicon.svg",
            "art/goa.svg",
            "art/pune.svg",
            "art/san-jose.svg",
            "art/bay-area.svg",
            "art/pla-robot.svg",
        }
    )
    for name in sorted(inventory):
        if not name.endswith(".svg"):
            continue
        root = ElementTree.parse(content.STATIC_ROOT / name).getroot()  # noqa: S314
        assert root.tag.rsplit("}", 1)[-1] == "svg"
        for element in root.iter():
            assert element.tag.rsplit("}", 1)[-1] not in {
                "script",
                "foreignObject",
                "style",
                "animate",
                "set",
            }
            for attribute, value in element.attrib.items():
                attribute = attribute.rsplit("}", 1)[-1].lower()
                assert not attribute.startswith("on")
                assert attribute != "style"
                if attribute in {"href", "src"}:
                    assert value.startswith("#")
                assert not re.search(r"(?:https?:|javascript:|data:|//)", value, re.I)


def test_startup_fails_if_required_asset_is_missing(app, monkeypatch):
    assets = app.extensions["portfolio"]["assets"] - {"story.js"}
    monkeypatch.setattr(application, "build_asset_inventory", lambda: assets)
    with pytest.raises(ContentValidationError, match="restore required assets: story.js"):
        application.create_app()


def test_claim_provenance_and_full_source_ledger(story_document, project_root):
    cards = {
        card["id"]: card for chapter in story_document["chapters"] for card in chapter["cards"]
    }
    assert story_document["sources"] == {
        "owner-brief": {"kind": "owner-supplied"},
        "profile": {"kind": "supplied-document"},
        "resume": {"kind": "supplied-document"},
        "supplied-documents": {"kind": "supplied-document"},
        "github": {"kind": "public-repository"},
    }
    assert "profile" in cards["school-unlocked"]["source_refs"]
    assert "owner-brief" in cards["sjsu-unlocked"]["source_refs"]
    assert cards["fog-arrives"]["source_refs"] == ["owner-brief"]
    assert "owner-brief" in cards["bots-unlocked"]["source_refs"]
    ledger = (project_root / "docs/story.md").read_text(encoding="utf-8")
    # The full public ledger must survive curation into the shorter website story.
    for subject in (
        "DragonstonePizzeria",
        "Spartanbot",
        "CUSR",
        "karmamining",
        "CyanogenMod",
        "Coldplay",
        "mixology",
        "Rising Star",
        "SPOT",
        "TMP All Star",
    ):
        assert subject in ledger
    assert re.search(r"Profile.*January 2019.*resume.*March 2019", ledger, re.I)
    assert re.search(r"Profile.*rank 7.*resume.*rank 8", ledger, re.I)
    for name in ("AGENTS.md", "README.md", "docs/architecture.md", "docs/handoff.md"):
        assert (project_root / name).is_file()


def test_full_achievement_inventory_and_project_evidence(story_document):
    expected = {
        "agentic-team-tools",
        "home-automation",
        "three-d-printing",
        "principal",
        "einstein-bots-platform",
        "public-cloud",
        "masters",
        "google-internship",
        "paul-110",
        "spartanbot",
        "tasking",
        "java-training",
        "college-degree",
        "seven-hackathons",
        "zuari",
        "cyanogenmod",
        "school-cs",
        "early-games",
        "ai-workflows",
        "coldplay",
        "tmp-all-star",
    }
    assert {item["id"] for item in story_document["achievements"]} == expected
    links = {url for item in story_document["achievements"] for url in item["links"].values()}
    assert "https://github.com/pranavprem/Cpp-Snake" in links
    assert "https://github.com/pranavprem/Parks-RecSanJose" in links
    assert "https://github.com/pranavprem/morpheus" in links
    assert "https://github.com/pranavprem/openmemory-local" in links
    assert "https://github.com/pranavprem/qdrant-nas" in links
    assert "https://github.com/pranavprem/neo-services" in links
    assert "https://youtu.be/ogItgrO9GSg?t=221" in links
    assert not any(
        repo in link
        for repo in (
            "/claudette",
            "/bitwarden-",
            "/CUSR",
            "/DragonstonePizzeria",
            "/karmamining",
            "/ReactCalculator",
            "/Muricize",
        )
        for link in links
    )
    text = " ".join(item["body"] for item in story_document["achievements"])
    for milestone in (
        "110%",
        "Green Belt",
        "2,000+",
        "25%",
        "SPOT",
        "PEARL",
        "Above and Beyond",
        "AppSprint",
        "Rising Star",
        "top 1%",
        "October 2020",
        "August 2023",
        "February 2025",
    ):
        assert milestone in text
    prepared, _ = prepare_story(story_document)
    eras = [content.ACHIEVEMENT_ERAS.index(item["era"]) for item in prepared["achievements"]]
    assert eras == sorted(eras)
    assert prepared["achievements"][0]["era"] == "current"
    assert prepared["achievements"][-1]["era"] == "undated"


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "data:text/html,hello",
        "//evil.invalid",
        "https://github.com.evil.invalid/x",
        "https://github.com/other/private",
        "https://github.com/pranavprem/x?redirect=evil",
        "https://github.com/pranavprem/%2e%2e",
        "http://github.com/pranavprem/TasKing",
        "https://youtu.be/ogItgrO9GSg?t=222",
        "https://youtu.be/unapproved?t=221",
    ],
)
def test_achievement_links_reject_unreviewed_destinations(story_document, url):
    story_document["achievements"][0]["links"] = {"Unsafe destination": url}
    with pytest.raises(ContentValidationError, match="public owner GitHub"):
        validate_story(story_document)


@pytest.mark.parametrize(
    "change", ["duplicate", "unknown-source", "unknown-era", "long-body", "missing", "too-many"]
)
def test_achievement_catalog_fails_closed(story_document, change):
    entries = story_document["achievements"]
    if change == "duplicate":
        entries[1]["id"] = entries[0]["id"]
    elif change == "unknown-source":
        entries[0]["source_refs"] = ["made-up"]
    elif change == "unknown-era":
        entries[0]["era"] = "guessed-date"
    elif change == "long-body":
        entries[0]["body"] = "x" * 601
    elif change == "missing":
        entries[0].pop("links")
    else:
        entries *= 4
    with pytest.raises(ContentValidationError):
        validate_story(story_document)


def test_buildings_carry_the_requested_labels():
    for name, expected in {
        "goa": {"NCS", "GEC"},
        "pune": {"HSBC"},
        "san-jose": {"SJSU", "GOOGLE / NEST"},
        "bay-area": {"SALESFORCE"},
    }.items():
        root = ElementTree.parse(content.STATIC_ROOT / "art" / f"{name}.svg").getroot()  # noqa: S314
        assert {node.text for node in root.iter() if node.tag.endswith("}text")} == expected

    for name, identifiers in {
        "goa": {"ncs-elephant", "gec-campus", "gec-west", "gec-east", "gec-courtyard"},
        "bay-area": {"salesforce-tower"},
    }.items():
        root = ElementTree.parse(content.STATIC_ROOT / "art" / f"{name}.svg").getroot()  # noqa: S314
        assert identifiers <= {node.get("id") for node in root.iter()}


@pytest.mark.parametrize(
    "body", ["One\nline", "One\n\n\nTwo", "One\n\n\n\nTwo", "\n\n".join(["A"] * 9), None]
)
def test_mini_paragraph_boundary_rejects_invalid_breaks(story_document, body):
    story_document["chapters"][0]["cards"][0]["body"] = body
    with pytest.raises(ContentValidationError):
        validate_story(story_document)


def test_mini_paragraphs_preserve_plain_text_and_snapshots(story_document):
    body = "First small paragraph.\n\nSecond small paragraph."
    story_document["chapters"][0]["cards"][0]["body"] = body
    validate_story(story_document)
    prepared, _ = prepare_story(story_document)
    card = prepared["chapters"][0]["cards"][0]
    assert card["body"] == body
    assert card["paragraphs"] == body.split("\n\n")


def test_five_stats_accumulate_experience_and_use_real_milestones(story_document):
    assert [stat["label"] for stat in story_document["stat_definitions"]] == [
        "Coding",
        "Enthusiasm",
        "Health",
        "Charisma",
        "Experience",
    ]
    assert [badge["id"] for badge in story_document["badges"]] == [
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
    ]
    document, game = prepare_story(story_document)
    xp = [game["initial"]["stats"]["experience"]] + [
        event["stats_after"]["experience"] for event in game["events"]
    ]
    assert xp == sorted(xp)
    assert game["events"][6]["stats_after"]["coding"] == 10
    assert game["events"][9]["stats_after"]["coding"] == game["events"][8]["stats_after"]["coding"]
    assert game["events"][9]["stats_after"]["vitality"] == 6
    final_stats = game["events"][-1]["stats_after"]
    assert {key for key, value in final_stats.items() if value == 10} == {"enthusiasm"}
    assert all(value <= 8 for key, value in final_stats.items() if key != "enthusiasm")
    assert document["chapters"][2]["cards"][0]["event"]["grant_badges"] == ["cs-percentile"]
    story_document["chapters"][2]["cards"][0]["event"]["stats_after"]["experience"] = 1
    with pytest.raises(ContentValidationError, match="experience accumulates"):
        validate_story(story_document)


@pytest.mark.parametrize("retired", ["automancy", "sidequests"])
def test_retired_stat_keys_are_rejected(story_document, retired):
    story_document["initial"]["stats"][retired] = 0
    with pytest.raises(ContentValidationError, match="documented fields"):
        validate_story(story_document)


def test_independent_story_beats_are_not_collated(story_document):
    cards = {
        card["id"]: card for chapter in story_document["chapters"] for card in chapter["cards"]
    }
    college = cards["college-unlocked"]["body"].split("\n\n")
    assert "first time living on my own" in college[0]
    beats = [
        "general secretary",
        "PyCon",
        "Zuari",
        "paper on securing",
        "Hackathons",
        "top of my class",
    ]
    positions = [
        next(i for i, paragraph in enumerate(college) if beat in paragraph) for beat in beats
    ]
    assert len(set(positions)) == len(beats)
    banking = cards["automation-unlocked"]["body"].split("\n\n")
    assert "TasKing" in banking[0] and "Green Belt" not in banking[0]
    assert "Green Belt" in banking[1] and "2,000" in banking[1]
    detour = cards["unexpected-detour"]
    assert detour["heading"] == "Dengue, right before finals"
    assert "A few weeks before my Class 12 final exams" in detour["body"]
    assert "hospital for a month" in detour["body"]
    assert "first sworn enemy" not in detour["body"]
    assert detour["body"].split("\n\n")[-1] == "Mosquitoes and I have not reconciled."
    assert (
        "found" in cards["school-unlocked"]["body"]
        or "finding out early" in cards["school-unlocked"]["body"]
        or "finding my thing early" in cards["school-unlocked"]["body"]
    )


def test_owner_voice_and_corrected_hsdi_details(story_document):
    bot_chapter = next(
        chapter for chapter in story_document["chapters"] if chapter["id"] == "bot-workshop"
    )
    assert bot_chapter["period_label"] == "Salesforce Bots / Copilot by 2023"
    cards = {
        card["id"]: card for chapter in story_document["chapters"] for card in chapter["cards"]
    }
    achievements = {item["id"]: item for item in story_document["achievements"]}
    assert (
        "irrespective of how many people wanted to hear my opinions"
        in cards["school-unlocked"]["body"]
    )
    assert "This was becoming a bit of a trend" in cards["college-unlocked"]["body"]
    assert "you guessed it" in cards["java-unlocked"]["body"]
    assert "HSDI (HSBC Software Development India)" in cards["java-unlocked"]["body"]
    assert "tools and infrastructure for developers" in cards["developer-ally-unlocked"]["body"]
    assert "This was the work I wanted" in cards["developer-ally-unlocked"]["body"]
    assert achievements["cyanogenmod"]["body"].startswith("From 18 to 20, I worked on")
    assert "Stock firmware was apparently insufficient" not in achievements["cyanogenmod"]["body"]
    hsdi = achievements["java-training"]
    assert hsdi["period_label"] == "2014-2017 / HSDI, Pune"
    assert "HSBC Software Development India" in hsdi["body"]
    assert "youngest Rising Star nominee at 20" in hsdi["body"]

    bots = cards["bots-unlocked"]["body"]
    for phrase in (
        "Argo CD",
        "99.99% availability",
        "public API",
        "100% of customer traffic",
        "from Heroku to multisubstrate",
        "multisubstrate public-cloud instances",
        "public Slack connector",
        "Einstein Copilot",
        "configurable AI agent",
    ):
        assert phrase in bots
    assert "from AWS to multisubstrate" not in bots

    current = cards["continuing-unlocked"]["body"]
    for phrase in (
        "Salesforce customers could build their own agents",
        "Atlas Reasoning Engine",
        "AgentScript",
        "more deterministic in an LLM world",
        "voice, MCP, native context, memory",
        "agentic runtime",
        "async processing",
        "long-running turns, actions, and sessions",
        "Salesforce CRM data",
        "work assistant and coding harness",
    ):
        assert phrase in current

    home = achievements["home-automation"]
    assert "OpenClaw and Hermes agents maintain each other" in home["body"]
    assert home["links"]["Morpheus credential gatekeeper"].endswith("/morpheus")
