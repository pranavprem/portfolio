"""Real-engine checks under the application's enforced CSP, without a shell server."""

import html
import json
import math
import random
import re
from copy import deepcopy
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.browser

GEOMETRY = """() => {
  const html = document.documentElement;
  const hud = document.getElementById('character-sheet').getBoundingClientRect();
  const height = html.clientHeight;
  const docked = html.dataset.hudDocked === 'true';
  const top = docked ? hud.bottom + 12 : 16;
  return {
    height, docked, top, offset: top + .35 * (height - top),
    maxScroll: Math.max(0, document.scrollingElement.scrollHeight - height),
    scroll: window.scrollY, hudHeight: hud.height, hudBottom: hud.bottom,
    anchors: [...document.querySelectorAll('.story-card[data-checkpoint]')]
      .map(node => node.getBoundingClientRect().top + window.scrollY)
  };
}"""

HUD = """() => ({
  index: Number(document.getElementById('journey').dataset.checkpointIndex),
  stats: Object.fromEntries([...document.querySelectorAll('[data-stat]')]
    .map(row => [row.dataset.stat, Number(row.querySelector('.stat-value').textContent)])),
  pips: Object.fromEntries([...document.querySelectorAll('[data-stat]')]
    .map(row => [row.dataset.stat, row.querySelectorAll('.stat-pips > .filled').length])),
  badges: [...document.querySelectorAll('li[data-badge].earned')].map(node => node.dataset.badge),
  region: document.querySelector('[data-region-art].current').dataset.regionArt,
  mood: document.getElementById('overworld').dataset.mood,
  frame: Number(document.getElementById('traveler').dataset.frame),
  transform: document.getElementById('travelers').getAttribute('transform')
})"""


def settle_layout(page):
    page.evaluate("""async () => {
      await document.fonts.ready;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    }""")


def settle_scroll(page, edge=None):
    # Playwright's string-predicate polling uses eval; keep the real CSP enforced.
    page.evaluate(
        """async edge => {
          const deadline = performance.now() + 5000;
          let settled = 0;
          let previous = window.scrollY;
          while (performance.now() < deadline) {
            await new Promise(resolve => requestAnimationFrame(resolve));
            const target = edge === 'bottom' ? document.scrollingElement.scrollHeight
                - document.documentElement.clientHeight : edge === 'top' ? 0 : previous;
            settled = Math.abs(window.scrollY - target) <= 1 ? settled + 1 : 0;
            previous = window.scrollY;
            if (settled === 3) return;
          }
          throw new Error('Native scrolling did not settle at the requested position');
        }""",
        edge,
    )


def open_journey(page, live_server):
    response = page.goto(live_server + "/")
    assert response.status == 200
    expect(page.locator("html")).to_have_class("enhanced")
    settle_layout(page)


def scroll_to_checkpoint(page, index, fraction=0):
    geometry = page.evaluate(GEOMETRY)
    if index < 0:
        target = 0
    else:
        anchor = geometry["anchors"][index]
        following = geometry["anchors"][index + 1] if index < 11 else anchor + 100
        target = anchor - geometry["offset"] + 2 + fraction * (following - anchor)
    page.evaluate("y => window.scrollTo(0, y)", target)
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", str(index))
    settle_layout(page)


def assert_hud(page, expected):
    actual = page.evaluate(HUD)
    for key in ("index", "stats", "badges", "region", "mood"):
        assert actual[key] == expected[key], (key, actual, expected)
    assert actual["pips"] == expected["stats"]
    expect(page.locator("#badge-count")).to_have_text(f"{len(expected['badges']):02d}")
    slots = page.locator("li[data-badge]")
    assert slots.count() == 11
    for index in range(11):
        slot = slots.nth(index)
        if index < len(expected["badges"]):
            assert slot.get_attribute("aria-hidden") is None
            assert slot.get_attribute("aria-label")
        else:
            expect(slot).to_have_attribute("aria-hidden", "true")
            assert slot.get_attribute("aria-label") is None
    return actual


def assert_matches_geometry(page, snapshots):
    geometry = page.evaluate(GEOMETRY)
    cursor = min(max(geometry["scroll"], 0), geometry["maxScroll"]) + geometry["offset"]
    index = max((i for i, anchor in enumerate(geometry["anchors"]) if anchor <= cursor), default=-1)
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", str(index))
    assert_hud(page, snapshots[index + 1])


def assert_complete_story(page, story_document, snapshots):
    expect(page.locator(".chapter")).to_have_count(11)
    cards = page.locator(".story-card[data-checkpoint]")
    expect(cards).to_have_count(12)
    for card in [card for chapter in story_document["chapters"] for card in chapter["cards"]]:
        node = page.locator(f'[data-checkpoint="{card["id"]}"]')
        expect(node.locator(".story-prose")).to_have_text(card["body"].split("\n\n"))
        for paragraph in node.locator(".story-prose").all():
            expect(paragraph).to_be_visible()
        expect(page.locator(f'[data-bonus-for="{card["id"]}"] .field-notes li')).to_have_text(
            card["facts"]
        )
    for index, expected in enumerate(snapshots[1:]):
        expect(cards.nth(index).locator(".chapter-stats dd")).to_have_text(
            [f"{value}/10" for value in expected["stats"].values()]
        )
    expect(page.locator(".achievement-note")).to_have_count(len(story_document["achievements"]))
    for achievement in story_document["achievements"]:
        node = page.locator(f"#achievement-{achievement['id']}")
        expect(node.locator("h3")).to_have_text(achievement["heading"])
        expect(node.locator("p:not(.eyebrow)")).to_have_text(achievement["body"])
        expect(node.locator("a")).to_have_text(list(achievement["links"]))
    expect(page.locator(".loot .milestone-label")).to_have_text(
        [badge["label"] for badge in story_document["badges"]]
    )
    for badge in story_document["badges"]:
        expect(page.locator(f'[data-achievement="story-{badge["id"]}"]')).to_contain_text(
            badge["description"]
        )
    expect(page.locator(".inventory-ledger")).to_have_count(0)
    expect(page.locator("button, input, form, [tabindex], [role=application]")).to_have_count(0)


@pytest.fixture
def observations(page):
    result = {"requests": [], "pageerrors": [], "console": []}
    page.on("request", lambda request: result["requests"].append(request))
    page.on("pageerror", lambda error: result["pageerrors"].append(str(error)))
    page.on("console", lambda message: result["console"].append((message.type, message.text)))
    page.add_init_script("""window.testCspViolations = [];
      document.addEventListener('securitypolicyviolation', event => {
        window.testCspViolations.push({
          directive: event.violatedDirective, blocked: event.blockedURI
        });
      });""")
    return result


def test_pure_selector_thresholds_equality_and_random_rewinds(page, live_server, game, snapshots):
    open_journey(page, live_server)
    anchors = [700, 1220.5, 1890, 2520, 3340, 3790, 4801, 5590, 6430, 7200, 7711, 8690]
    positions = [-100_000, 0, 100_000]
    positions += [anchor + delta for anchor in anchors for delta in (-0.001, 0, 0.001)]
    positions += [
        start + (end - start) * 0.21 for start, end in zip(anchors[:-1], anchors[1:], strict=True)
    ]
    randomized = positions * 3
    random.Random(20260906).shuffle(randomized)  # noqa: S311 - reproducible test order, not security
    result = page.evaluate(
        """async ({game, anchors, positions}) => {
      const {deriveState} = await import('/static/story.js');
      const before = JSON.stringify(game);
      const states = positions.map(position => deriveState(game, anchors, position));
      return {states, unchanged: JSON.stringify(game) === before,
        opening: deriveState(game, [], 0),
        reduced: positions.map(position => deriveState(game, anchors, position, true))};
    }""",
        {"game": game, "anchors": anchors, "positions": randomized},
    )
    assert result["unchanged"]
    assert result["opening"]["index"] == -1
    seen = {}
    for cursor, state, reduced in zip(randomized, result["states"], result["reduced"], strict=True):
        index = max((i for i, anchor in enumerate(anchors) if anchor <= cursor), default=-1)
        expected = snapshots[index + 1]
        for key in ("index", "stats", "badges", "region", "mood"):
            assert state[key] == reduced[key] == expected[key]
        event = game["initial"] if index < 0 else game["events"][index]
        next_event = game["events"][index + 1] if index < 11 else None
        position, frame = event["position"], 0
        if index >= 0 and next_event and next_event["region_id"] == event["region_id"]:
            fraction = (cursor - anchors[index]) / (anchors[index + 1] - anchors[index])
            position = {
                axis: math.floor(value + (next_event["position"][axis] - value) * fraction + 0.5)
                for axis, value in event["position"].items()
            }
            frame = math.floor(fraction * 12) % 4
        assert state["position"] == position
        assert state["frame"] == frame
        assert reduced["position"] == event["position"] and reduced["frame"] == 0
        assert 20 <= state["position"]["x"] <= 300 and 0 <= state["position"]["y"] <= 180
        if cursor in seen:
            assert state == seen[cursor]
        seen[cursor] = state


def test_real_scroll_all_snapshots_rewind_and_jump(page, live_server, snapshots, observations):
    open_journey(page, live_server)
    assert_hud(page, snapshots[0])
    before = page.evaluate(GEOMETRY)
    order = [*range(12), *range(11, -2, -1), 11, -1, 9, 8, 9, 1, 0, 6, 11, -1]
    seen = {}
    for index in order:
        scroll_to_checkpoint(page, index, 0.21)
        actual = assert_hud(page, snapshots[index + 1])
        if index in seen:
            assert actual == seen[index]
        seen[index] = actual
    after = page.evaluate(GEOMETRY)
    assert after["anchors"] == pytest.approx(before["anchors"], abs=1)
    assert after["hudHeight"] == pytest.approx(before["hudHeight"], abs=1)
    assert observations["pageerrors"] == []
    assert page.evaluate("window.testCspViolations") == []


@pytest.mark.parametrize("width", [320, 375, 390, 768, 1024, 1440])
def test_responsive_clearance_and_endpoint_reachability(page, live_server, snapshots, width):
    page.set_viewport_size({"width": width, "height": 1000})
    open_journey(page, live_server)
    initial = page.evaluate(GEOMETRY)
    assert initial["anchors"][0] > initial["offset"]
    assert initial["anchors"][-1] <= initial["maxScroll"] + initial["offset"]
    assert initial["docked"] == (width < 1024)
    for index in (0, 8, 9, 11):
        scroll_to_checkpoint(page, index)
        assert_hud(page, snapshots[index + 1])
        geometry = page.evaluate(GEOMETRY)
        heading = (
            page.locator(".story-card").nth(index).locator(".story-prose").first.bounding_box()
        )
        assert heading["y"] >= geometry["top"]
        assert heading["y"] + 32 < geometry["height"]
        if width >= 1024:
            hud = page.locator("#character-sheet").bounding_box()
            scene = page.locator(".scene-panel").bounding_box()
            track = page.locator(".story-track").bounding_box()
            assert track["x"] + track["width"] <= hud["x"]
            assert scene["y"] >= hud["y"] + hud["height"]
            assert 0 <= hud["y"] < hud["y"] + hud["height"] <= 1000
        else:
            assert geometry["hudBottom"] <= 250
            expect(page.locator(".scene-panel")).to_be_hidden()
            expect(page.locator(".mobile-landscape")).to_have_count(4)
    layout = page.evaluate("""() => ({
      width: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      clipped: [...document.querySelectorAll('html, body, .journey, .story-track')]
        .filter(node => ['hidden', 'clip'].includes(getComputedStyle(node).overflowX) ||
          ['hidden', 'clip'].includes(getComputedStyle(node).overflowY)).map(node => node.tagName),
      outside: [...document.querySelectorAll(
        'h1, h2, h3:not(.sr-only), .story-prose, .field-notes li, ' +
        '.stat-value, .stat-max, .achievement-note > p:not(.eyebrow)')]
        .filter(node => { const box = node.getBoundingClientRect();
          return box.left < -1 || box.right > document.documentElement.clientWidth + 1;
        }).map(node => node.className)
    })""")
    assert layout["scrollWidth"] <= layout["width"] + 1
    assert layout["clipped"] == layout["outside"] == []
    assert page.evaluate(GEOMETRY)["anchors"] == pytest.approx(initial["anchors"], abs=1)
    page.evaluate("window.scrollTo(0, document.scrollingElement.scrollHeight)")
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "11")
    scroll_to_checkpoint(page, -1)
    assert_hud(page, snapshots[0])


def test_visible_card_subheadings_have_clear_hierarchy(page, live_server):
    open_journey(page, live_server)
    card = page.locator('[data-checkpoint="fog-arrives"]')
    heading = card.locator("h3")
    prose = card.locator(".story-prose")
    styles = page.evaluate(
        """([heading, prose]) => ({
          headingSize: parseFloat(getComputedStyle(heading).fontSize),
          proseSize: parseFloat(getComputedStyle(prose).fontSize),
          headingFamily: getComputedStyle(heading).fontFamily,
          proseFamily: getComputedStyle(prose).fontFamily,
        })""",
        [heading.element_handle(), prose.element_handle()],
    )
    assert styles["headingSize"] > styles["proseSize"]
    assert styles["headingFamily"] != styles["proseFamily"]


def test_short_mobile_uses_normal_flow_and_resize_remeasures(page, live_server, snapshots):
    page.set_viewport_size({"width": 390, "height": 300})
    open_journey(page, live_server)
    expect(page.locator("html")).to_have_attribute("data-hud-docked", "false")
    assert (
        page.locator("#character-sheet").evaluate("node => getComputedStyle(node).position")
        == "static"
    )
    for index in (7, 11, -1):
        scroll_to_checkpoint(page, index)
        assert_hud(page, snapshots[index + 1])
    page.set_viewport_size({"width": 390, "height": 1000})
    expect(page.locator("html")).to_have_attribute("data-hud-docked", "true")
    settle_layout(page)
    assert_matches_geometry(page, snapshots)
    scroll_to_checkpoint(page, 6)
    for width in (1440, 320, 1024, 768):
        page.set_viewport_size({"width": width, "height": 1000})
        settle_layout(page)
        assert_matches_geometry(page, snapshots)


def test_short_desktop_does_not_pin_an_unreadable_sheet(page, live_server, snapshots):
    open_journey(page, live_server)
    for height, flow in ((200, True), (400, False), (200, True)):
        page.set_viewport_size({"width": 1440, "height": height})
        expect(page.locator("html")).to_have_attribute("data-theater-flow", str(flow).lower())
        settle_layout(page)
        scroll_to_checkpoint(page, 6)
        assert_hud(page, snapshots[7])
        theater = page.locator(".theater")
        position = theater.evaluate("node => getComputedStyle(node).position")
        # Clearance includes the whole panel's padding and sticky inset, not just its HUD.
        if flow:
            assert theater.bounding_box()["height"] + 24 > height
            assert position == "static"
        else:
            assert position == "sticky"
            hud = page.locator("#character-sheet").bounding_box()
            assert 0 <= hud["y"] < hud["y"] + hud["height"] <= height


def test_no_javascript_has_the_complete_story(new_context, live_server, story_document, snapshots):
    page = new_context(java_script_enabled=False).new_page()
    page.goto(live_server + "/")
    assert_complete_story(page, story_document, snapshots)
    expect(page.locator("html")).not_to_have_class("enhanced")
    expect(page.locator("#sheet-status")).to_have_text(
        "Starting stats. Later stats are beside the story."
    )
    expect(page.locator(".chapter-stats").first).to_be_visible()
    expect(page.locator(".stat-value")).to_have_text(
        [str(value) for value in snapshots[0]["stats"].values()]
    )
    expect(page.locator("li[data-badge].earned")).to_have_count(0)


@pytest.mark.parametrize("resource", ["story.js", "story.css", "art/goa.svg"])
def test_failed_local_resource_never_hides_prose(
    page, live_server, story_document, snapshots, resource
):
    page.route(f"**/static/{resource}", lambda route: route.abort())
    page.goto(live_server + "/")
    assert_complete_story(page, story_document, snapshots)
    if resource == "story.js":
        expect(page.locator("html")).not_to_have_class("enhanced")
        expect(page.locator("#sheet-status")).to_have_text(
            "Starting stats. Later stats are beside the story."
        )
        expect(page.locator("li[data-badge].earned")).to_have_count(0)


@pytest.mark.parametrize(
    "failure",
    [
        "json",
        "version",
        "boolean-stat",
        "position",
        "empty-events",
        "duplicate-badge",
        "future-badge",
        "lost-experience",
        "marker-id",
        "chapter-id",
    ],
)
def test_invalid_projection_falls_back(page, live_server, game, story_document, snapshots, failure):
    projection = deepcopy(game)
    if failure == "version":
        projection["schema_version"] = 1
    elif failure == "boolean-stat":
        projection["events"][0]["stats_after"]["coding"] = True
    elif failure == "position":
        projection["events"][0]["position"]["x"] = 301
    elif failure == "empty-events":
        projection["events"] = []
    elif failure == "duplicate-badge":
        projection["events"][0]["badges_after"] *= 2
    elif failure == "future-badge":
        projection["events"][0]["badges_after"] = [projection["events"][-1]["badges_after"][-1]]
    elif failure == "lost-experience":
        projection["events"][2]["stats_after"]["experience"] = 0
    elif failure == "marker-id":
        projection["events"][0]["id"] = "wrong-card"
    elif failure == "chapter-id":
        projection["events"][0]["chapter_id"] = "wrong-chapter"
    serialized = "{" if failure == "json" else json.dumps(projection)

    def replace_projection(route):
        response = route.fetch()
        source = re.sub(
            r'data-game="[^"]*"',
            lambda _: f'data-game="{html.escape(serialized, quote=True)}"',
            response.text(),
            count=1,
        )
        route.fulfill(response=response, body=source)

    page.route(live_server + "/", replace_projection)
    page.goto(live_server + "/")
    expect(page.locator("#sheet-status")).to_have_text(
        "Paper edition. The stats are beside the story."
    )
    expect(page.locator("html")).not_to_have_class("enhanced")
    expect(page.locator("#character-sheet")).to_be_hidden()
    expect(page.locator("li[data-badge].earned")).to_have_count(0)
    assert_complete_story(page, story_document, snapshots)


def test_geometry_failure_resets_a_live_hud(page, live_server, story_document, snapshots):
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 9)
    assert_hud(page, snapshots[10])
    page.evaluate("""() => {
      const markers = document.querySelectorAll('[data-checkpoint]');
      markers[1].getBoundingClientRect = () => markers[0].getBoundingClientRect();
      window.dispatchEvent(new Event('resize'));
    }""")
    expect(page.locator("html")).not_to_have_class("enhanced")
    expect(page.locator("#sheet-status")).to_have_text(
        "Paper edition. The stats are beside the story."
    )
    expect(page.locator(".stat-value")).to_have_text(
        [str(value) for value in snapshots[0]["stats"].values()]
    )
    expect(page.locator("li[data-badge].earned")).to_have_count(0)
    assert_complete_story(page, story_document, snapshots)


def test_reduced_motion_load_and_mid_story_toggle(page, live_server, game, snapshots):
    page.emulate_media(reduced_motion="reduce")
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 0, 0.12)
    reduced = assert_hud(page, snapshots[1])
    assert reduced["frame"] == 0
    position = game["events"][0]["position"]
    assert reduced["transform"] == f"translate({position['x']} {position['y']})"
    page.emulate_media(reduced_motion="no-preference")
    expect(page.locator("#traveler")).not_to_have_attribute("data-frame", "0")
    moving = assert_hud(page, snapshots[1])
    assert moving["transform"] != reduced["transform"]
    expect(page.locator("#companion")).not_to_have_attribute("transform", "translate(-18 -1)")
    assert (
        page.locator(".step-effects").evaluate("node => getComputedStyle(node).visibility")
        == "visible"
    )
    page.emulate_media(reduced_motion="reduce")
    expect(page.locator("#traveler")).to_have_attribute("data-frame", "0")
    expect(page.locator("#companion")).to_have_attribute("transform", "translate(-18 -1)")
    assert (
        page.locator(".step-effects").evaluate("node => getComputedStyle(node).visibility")
        == "hidden"
    )
    assert assert_hud(page, snapshots[1]) == reduced
    scroll_to_checkpoint(page, 9, 0.4)
    assert assert_hud(page, snapshots[10])["frame"] == 0
    assert page.locator(".leg").first.evaluate("node => getComputedStyle(node).transform") == "none"


def test_reload_history_fragments_and_native_keyboard(page, live_server, snapshots):
    page.add_init_script("""window.testScrollWrites = [];
      for (const name of ['scroll', 'scrollTo', 'scrollBy']) {
        const original = window[name].bind(window);
        window[name] = (...args) => {
          window.testScrollWrites.push(name); return original(...args);
        };
      }
    """)
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 6, 0.2)
    before = page.evaluate(HUD)
    scroll = page.evaluate("window.scrollY")
    page.reload()
    settle_layout(page)
    assert_matches_geometry(page, snapshots)
    assert page.evaluate("window.testScrollWrites") == []
    # A fast WebKit automation reload can return to top even with the module blocked.
    # Test state at the native position rather than require application scroll writes.
    restored = page.evaluate("window.scrollY")
    assert restored == 0 or restored == pytest.approx(scroll, abs=2)
    if restored:
        assert page.evaluate(HUD) == before
    scroll_to_checkpoint(page, 6, 0.2)
    before = page.evaluate(HUD)
    page.evaluate("window.testScrollWrites = []")
    page.goto(live_server + "/healthz")
    page.go_back()
    settle_layout(page)
    assert_matches_geometry(page, snapshots)
    assert page.evaluate("window.testScrollWrites") == []
    assert page.evaluate("window.scrollY") == pytest.approx(scroll, abs=2)
    assert page.evaluate(HUD) == before
    assert page.evaluate("history.scrollRestoration") == "auto"
    page.goto(live_server + "/#continuing")
    settle_layout(page)
    assert_matches_geometry(page, snapshots)
    assert page.evaluate("window.scrollY") > 0
    page.keyboard.press("End")
    # A checkpoint can change before the browser's native key-scroll finishes.
    settle_scroll(page, "bottom")
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "11")
    page.keyboard.press("Home")
    settle_scroll(page, "top")
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "-1")
    page.keyboard.press("PageDown")
    expect(page.locator(".masthead")).not_to_be_in_viewport()
    settle_scroll(page)
    page.keyboard.press("Home")
    settle_scroll(page, "top")
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "-1")
    page.mouse.move(200, 300)
    page.mouse.wheel(0, 500)
    expect(page.locator(".masthead")).not_to_be_in_viewport()
    settle_scroll(page)
    assert_matches_geometry(page, snapshots)
    assert page.evaluate("window.testScrollWrites") == []


def test_side_arrows_move_the_page_and_sprite_without_intercepting_input(page, live_server):
    page.add_init_script("""window.testScrollWrites = [];
      const original = window.scrollBy.bind(window);
      window.scrollBy = (...args) => {
        window.testScrollWrites.push(args); return original(...args);
      };
    """)
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 0, 0.1)
    page.evaluate("window.testScrollWrites = []")
    before = page.evaluate("""() => ({
      scrollY: window.scrollY,
      position: document.getElementById('travelers').getAttribute('transform'),
    })""")
    page.keyboard.press("ArrowRight")
    page.wait_for_function("before => window.scrollY > before", arg=before["scrollY"])
    page.wait_for_timeout(500)
    settle_layout(page)
    page.wait_for_function(
        "before => document.getElementById('travelers').getAttribute('transform') !== before",
        arg=before["position"],
    )
    after_right = page.evaluate("""() => ({
      scrollY: window.scrollY,
      position: document.getElementById('travelers').getAttribute('transform'),
    })""")
    assert page.evaluate("window.testScrollWrites[0][0]") == {
        "top": 40,
        "behavior": "smooth",
    }
    assert after_right["position"] != before["position"]
    assert len(page.evaluate("window.testScrollWrites")) == 1

    page.keyboard.press("ArrowLeft")
    page.wait_for_function("before => window.scrollY < before", arg=after_right["scrollY"])
    page.wait_for_timeout(500)
    settle_layout(page)
    assert page.evaluate("window.scrollY") == pytest.approx(before["scrollY"], abs=2)
    assert len(page.evaluate("window.testScrollWrites")) == 2
    assert (
        page.evaluate("""() => {
      const event = new KeyboardEvent('keydown', {key: 'ArrowRight', cancelable: true});
      document.dispatchEvent(event);
      return event.defaultPrevented;
    }""")
        is False
    )

    page.evaluate("""() => {
      window.testScrollWrites = [];
      const overflow = document.createElement('div');
      overflow.id = 'horizontal-overflow-probe';
      overflow.style.width = '200vw';
      overflow.style.height = '1px';
      document.body.append(overflow);
    }""")
    assert page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
    )
    page.keyboard.press("ArrowRight")
    assert page.evaluate("window.testScrollWrites") == []
    page.evaluate("document.getElementById('horizontal-overflow-probe').remove()")

    page.evaluate("""() => {
      const editable = document.createElement('div');
      editable.id = 'editable-probe';
      editable.contentEditable = 'true';
      document.body.append(editable);
      editable.focus();
    }""")
    page.keyboard.press("ArrowRight")
    assert page.evaluate("window.testScrollWrites") == []

    page.locator("#editable-probe").evaluate("node => node.remove()")
    page.emulate_media(reduced_motion="reduce")
    page.evaluate("window.testScrollWrites = []")
    page.keyboard.press("ArrowRight")
    assert page.evaluate("window.testScrollWrites[0][0]") == {"top": 40, "behavior": "auto"}


def test_resize_observer_remeasures_text_reflow(page, live_server, snapshots):
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 6)
    before = page.evaluate(GEOMETRY)
    page.locator(".story-prose").first.evaluate("node => { node.style.fontSize = '40px'; }")
    settle_layout(page)
    after = page.evaluate(GEOMETRY)
    assert after["anchors"][2] > before["anchors"][2]
    assert_matches_geometry(page, snapshots)


def test_reflow_font_notifications_and_observer_fallback(page, live_server, snapshots):
    page.add_init_script("delete window.ResizeObserver")
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 7, 0.2)
    page.evaluate("""() => {
      document.querySelector('.story-prose').style.fontSize = '32px';
      window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted: true}));
      document.dispatchEvent(new Event('visibilitychange'));
    }""")
    settle_layout(page)
    assert_matches_geometry(page, snapshots)
    page.set_viewport_size({"width": 390, "height": 1000})
    settle_layout(page)
    assert_matches_geometry(page, snapshots)


def test_csp_privacy_and_no_idle_animation(page, live_server, observations, snapshots):
    page.add_init_script("""window.testRafCalls = 0;
      const original = window.requestAnimationFrame.bind(window);
      window.testOriginalRaf = original;
      window.requestAnimationFrame = callback => {
        window.testRafCalls++; return original(callback);
      };
    """)
    open_journey(page, live_server)
    for index in (0, 4, 6, 8, 9, 11, -1):
        scroll_to_checkpoint(page, index, 0.2)
        assert_hud(page, snapshots[index + 1])
    scheduled = page.evaluate("""() => {
      const before = window.testRafCalls;
      for (let i = 0; i < 100; i++) document.dispatchEvent(new Event('scroll'));
      return window.testRafCalls - before;
    }""")
    assert scheduled == 1
    # Observe a number of paints, not a wall-clock sleep or the instrumented scheduler.
    idle = page.evaluate("""async () => {
      const frames = count => new Promise(resolve => {
        const next = () => --count ? window.testOriginalRaf(next) : resolve();
        window.testOriginalRaf(next);
      });
      await frames(5);
      const calls = window.testRafCalls;
      const transform = document.getElementById('travelers').getAttribute('transform');
      await frames(12);
      return {extraCalls: window.testRafCalls - calls,
        unchanged: transform === document.getElementById('travelers').getAttribute('transform'),
        animations: document.getAnimations().length,
        local: localStorage.length, session: sessionStorage.length, cookies: document.cookie};
    }""")
    assert idle == {
        "extraCalls": 0,
        "unchanged": True,
        "animations": 0,
        "local": 0,
        "session": 0,
        "cookies": "",
    }
    assert page.context.cookies() == []
    assert observations["pageerrors"] == []
    assert not [message for kind, message in observations["console"] if kind == "error"]
    assert page.evaluate("window.testCspViolations") == []
    origin = urlsplit(live_server)
    for request in observations["requests"]:
        url = urlsplit(request.url)
        assert (url.scheme, url.netloc) == (origin.scheme, origin.netloc)
        assert request.resource_type in {"document", "stylesheet", "script", "image"}
        assert request.method == "GET"


@pytest.mark.parametrize("width", [390, 1440])
@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_local_axe_accessibility(page, live_server, project_root, width, scheme):
    page.emulate_media(color_scheme=scheme)
    page.set_viewport_size({"width": width, "height": 1000})
    open_journey(page, live_server)
    axe_path = project_root / "node_modules/axe-core/axe.min.js"
    assert axe_path.is_file(), "Run npm ci to install the pinned local axe-core test dependency"
    # Playwright evaluation is test instrumentation; the response CSP stays enforced.
    page.evaluate(axe_path.read_text(encoding="utf-8"))
    for index in (-1, 9, 11):
        scroll_to_checkpoint(page, index)
        violations = page.evaluate("""async () => {
          const result = await axe.run(document, {runOnly: {
            type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
          }});
          return result.violations.map(({id, impact, nodes}) => ({id, impact,
            nodes: nodes.map(({target, failureSummary}) => ({target, failureSummary}))}));
        }""")
        assert violations == [], json.dumps(violations, indent=2)


def test_text_enlargement_and_narrow_reflow(page, live_server, snapshots, tmp_path):
    page.set_viewport_size({"width": 320, "height": 1000})
    open_journey(page, live_server)
    # 320 CSS pixels models 1280px desktop at 400% reflow, not native browser zoom.
    page.evaluate("""() => {
      const nodes = [...document.querySelectorAll('body *:not(svg):not(svg *)')];
      const sizes = nodes.map(node => parseFloat(getComputedStyle(node).fontSize));
      nodes.forEach((node, index) => node.style.fontSize = `${sizes[index] * 2}px`);
      window.dispatchEvent(new Event('resize'));
    }""")
    settle_layout(page)
    assert_matches_geometry(page, snapshots)
    layout = page.evaluate("""() => ({
      width: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      overflowing: [...document.querySelectorAll(
        '.wordmark, h1, h2, h3, .milestone, .character-sheet, .stat, .field-notes li')]
        .filter(node => node.scrollWidth > node.clientWidth + 1)
        .map(node => ({tag: node.tagName, class: node.className,
          width: node.clientWidth, scrollWidth: node.scrollWidth})),
      overlappingStats: [...document.querySelectorAll('[data-stat]')].filter(row => {
        const label = row.querySelector('.stat-compact').getBoundingClientRect();
        const value = row.querySelector('.stat-value').getBoundingClientRect();
        return label.width && label.right > value.left && label.left < value.right
          && label.bottom > value.top && label.top < value.bottom;
      }).map(row => row.dataset.stat)
    })""")
    if layout["scrollWidth"] > layout["width"] + 1:
        screenshot = tmp_path / "text-enlargement.png"
        page.screenshot(path=str(screenshot))
        layout["screenshot"] = str(screenshot)
    assert layout["scrollWidth"] <= layout["width"] + 1, json.dumps(layout, indent=2)
    assert layout["overlappingStats"] == [], layout
    if page.evaluate(GEOMETRY)["docked"]:
        assert page.evaluate(GEOMETRY)["hudBottom"] <= 250
    scroll_to_checkpoint(page, 11)
    assert_hud(page, snapshots[12])


def test_print_preserves_prose_and_semantic_snapshots(page, live_server, story_document, snapshots):
    open_journey(page, live_server)
    page.emulate_media(media="print")
    assert_complete_story(page, story_document, snapshots)
    expect(page.locator(".theater")).to_be_hidden()
    assert page.locator(".journey").evaluate("node => getComputedStyle(node).display") == "block"
    expect(page.locator(".ending")).to_be_visible()


def test_forced_colors_and_native_text_selection(page, live_server, snapshots):
    page.emulate_media(forced_colors="active")
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 9)
    assert_hud(page, snapshots[10])
    expect(page.locator(".chapter-stats").nth(9)).to_contain_text("Health")
    selected = page.evaluate("""() => {
      const range = document.createRange();
      const paragraph = document.querySelector('[data-checkpoint="fog-arrives"] .story-prose');
      range.selectNodeContents(paragraph);
      const selection = window.getSelection();
      selection.removeAllRanges(); selection.addRange(range);
      return selection.toString();
    }""")
    assert "new cadence of contribution" in selected


def test_main_story_reading_budget_and_optional_inventory(page, live_server, story_document):
    open_journey(page, live_server)
    words = page.locator("#main-story").evaluate(r"""node => {
      const copy = node.cloneNode(true);
      copy.querySelectorAll('.sr-only, .chapter-stats, noscript, [aria-hidden=true]')
        .forEach(element => element.remove());
      return copy.textContent.trim().split(/\s+/).length;
    }""")
    assert words <= 900, f"Main story is {words} words; keep it under five minutes at 180 wpm"
    assert page.locator("#main-story .achievement-note").count() == 0
    assert page.locator("#bonus .achievement-note").count() == len(story_document["achievements"])
    assert page.locator(".chapter-snapshot, .meter-disclaimer").count() == 0
    expect(page.locator("[data-stat]")).to_have_count(5)
    expect(page.locator('[data-stat="experience"] .stat-full')).to_have_text("Experience")
    expect(
        page.locator(".inventory-ledger, .milestone, [data-stat=automancy], [data-stat=sidequests]")
    ).to_have_count(0)
    assert page.locator("#bonus .achievement-catalog").evaluate("node => node.tagName") == "UL"
    assert page.locator("#bonus .achievement-note").evaluate_all(
        "nodes => nodes.every(n => n.tagName === 'LI')"
    )
    stats = page.locator(".chapter-stats").first
    assert stats.evaluate("node => getComputedStyle(node).position") == "absolute"
    assert stats.get_attribute("aria-hidden") is None
    assert "Coding" in stats.aria_snapshot()
    assert page.locator('a[href="mailto:pranavprem93@gmail.com"]').count() == 1
    assert page.locator('#main-story a[href*="einstein-bot-channel-connector"]').count() == 1
    assert page.locator('#bot-workshop a[href*="einstein-bot-channel-connector"]').count() == 1
    expect(page.locator("#automation .story-prose a")).to_have_text("TasKing")
    expect(page.locator("#sjsu .story-prose a")).to_have_text("SpartanBot")
    expect(page.locator(".ending > .story-prose")).to_have_count(3)
    expect(page.locator(".ending > .story-prose").nth(2)).to_have_text(
        "I've also got into 3D printing."
    )
    expect(page.locator(".route-track li").last).to_have_text("San Francisco")
    expect(page.locator("#achievement-tmp-all-star h3")).to_have_text(
        "Corporate awards are meaningless"
    )
    expect(page.locator(".pla-meme")).to_have_text("Bender voice: I'm 40% PLA.")
    expect(page.locator('.pla-meme img[src="/static/art/pla-robot.svg"]')).to_be_visible()
    assert page.locator("iframe, video").count() == 0


def test_every_achievement_has_a_reversible_sprite_reaction(page, live_server):
    open_journey(page, live_server)
    geometry = page.evaluate(GEOMETRY)
    anchors = page.locator("[data-achievement]").evaluate_all(
        "nodes => nodes.map(node => node.getBoundingClientRect().top + scrollY)"
    )
    assert len(anchors) == 32  # Eleven story badges plus 21 grouped highlights.
    positions = [
        anchor + min(180, anchors[i + 1] - anchor if i + 1 < len(anchors) else 180) / 2
        for i, anchor in enumerate(anchors)
    ]
    for anchor, cursor in zip(anchors, positions, strict=True):
        page.evaluate("y => window.scrollTo(0, y)", anchor - geometry["offset"])
        settle_layout(page)
        assert page.locator("#traveler").get_attribute("transform") in {
            "translate(0 0)",
            "translate(0 -1)",
        }
        page.evaluate("y => window.scrollTo(0, y)", cursor - geometry["offset"])
        settle_layout(page)
        expect(page.locator("#traveler")).to_have_attribute("transform", "translate(0 -8)")
        expect(page.locator("#traveler")).to_have_attribute("data-celebrating", "true")
        expect(page.locator("#portrait-sprite")).to_have_attribute("transform", "translate(0 -3)")
        companion = page.locator("#companion").get_attribute("transform")
        match = re.fullmatch(r"translate\(-18 (-?\d+)\)", companion)
        assert match and int(match.group(1)) <= -5
    for cursor in (positions[8], positions[0], positions[-1], positions[0]):
        page.evaluate("y => window.scrollTo(0, y)", cursor - geometry["offset"])
        settle_layout(page)
        expect(page.locator("#traveler")).to_have_attribute("transform", "translate(0 -8)")
    before = page.evaluate(HUD)
    page.emulate_media(reduced_motion="reduce")
    expect(page.locator("#traveler")).to_have_attribute("transform", "translate(0 0)")
    expect(page.locator("#traveler")).to_have_attribute("data-celebrating", "false")
    expect(page.locator("#companion")).to_have_attribute("transform", "translate(-18 -1)")
    after = page.evaluate(HUD)
    assert after["stats"] == before["stats"] and after["badges"] == before["badges"]
    pure = page.evaluate("""async () => {
      const {deriveCelebration} = await import('/static/story.js');
      return [-1, 0, 45, 90, 1000, 45, 90].map(y => deriveCelebration([0, 90], y));
    }""")
    assert pure[0] == pure[4] == {"lift": 0, "active": False}
    assert pure[1] == pure[3] == pure[6] == {"lift": 0, "active": True}
    assert pure[2] == pure[5] == {"lift": 8, "active": True}


@pytest.mark.parametrize("width", [390, 1440])
def test_dark_mode_follows_device_without_resetting_story(page, live_server, snapshots, width):
    page.set_viewport_size({"width": width, "height": 1000})
    page.emulate_media(color_scheme="light")
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 8)
    before = page.evaluate(HUD)
    page.emulate_media(color_scheme="dark")
    settle_layout(page)
    assert (
        page.locator("html").evaluate("node => getComputedStyle(node).backgroundColor")
        == "rgb(20, 35, 31)"
    )
    assert page.evaluate(HUD) == before
    assert_hud(page, snapshots[9])
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    page.emulate_media(color_scheme="light")
    settle_layout(page)
    assert (
        page.locator("html").evaluate("node => getComputedStyle(node).backgroundColor")
        == "rgb(245, 241, 231)"
    )


def test_quiet_reading_hierarchy_preserves_story_and_city_context(page, live_server, snapshots):
    open_journey(page, live_server)
    expect(
        page.locator(
            ".edition, .wordmark-sub, .intro-deck, .cartridge-details, .region-heading, "
            ".chapter-index, .sheet-topline, .player-class, .identity-star, .scene-topline, "
            ".scene-coordinates, .theater-footnote"
        )
    ).to_have_count(0)
    expect(page.locator("#college .story-beats > li")).to_have_count(6)
    assert "first time living on my own" in page.locator("#college .story-prose").first.inner_text()
    track = page.locator(".story-track").bounding_box()
    theater = page.locator(".theater").bounding_box()
    assert track["width"] <= 512
    assert theater["x"] - (track["x"] + track["width"]) >= 80
    assert (
        page.locator(".story-prose").first.evaluate(
            "node => parseFloat(getComputedStyle(node).fontSize)"
        )
        >= 18
    )
    for index, city in ((0, "Goa"), (5, "Pune"), (7, "San Jose"), (11, "San Francisco")):
        scroll_to_checkpoint(page, index)
        assert_hud(page, snapshots[index + 1])
        expect(page.locator("#world-label")).to_have_text(city)
        expect(page.locator("#sheet-status")).to_contain_text("Chapter")
        assert "SCROLL TO EXPLORE" not in page.locator("#sheet-status").inner_text()
