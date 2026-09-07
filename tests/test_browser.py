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
        expect(node.locator(".story-prose")).to_have_text(card["body"])
        expect(node.locator(".story-prose")).to_be_visible()
        expect(node.locator(".field-notes li")).to_have_text(card["facts"])
    for index, expected in enumerate(snapshots[1:]):
        expect(cards.nth(index).locator(".chapter-snapshot dd")).to_have_text(
            [f"{value}/10" for value in expected["stats"].values()]
        )
        expect(cards.nth(index).locator(".chapter-snapshot")).to_be_visible()
    expect(page.locator(".inventory-ledger dd")).to_have_text(
        [badge["description"] for badge in story_document["badges"]]
    )
    expect(page.locator("a, button, input, form, [tabindex], [role=application]")).to_have_count(0)


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
        heading = page.locator(".story-card h3").nth(index).bounding_box()
        assert heading["y"] >= geometry["top"]
        assert heading["y"] + heading["height"] < geometry["height"]
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
        'h1, h2, h3, .story-prose, .field-notes li, .stat-value, .stat-max, .inventory-ledger dd')]
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
    page.set_viewport_size({"width": 1440, "height": 200})
    open_journey(page, live_server)
    scroll_to_checkpoint(page, 6)
    assert_hud(page, snapshots[7])
    hud = page.locator("#character-sheet").bounding_box()
    position = page.locator(".theater").evaluate("node => getComputedStyle(node).position")
    if hud["height"] > 200:
        assert position not in {"sticky", "fixed"}, {"hud": hud, "theaterPosition": position}
    else:
        assert 0 <= hud["y"] < hud["y"] + hud["height"] <= 200


def test_no_javascript_has_the_complete_story(new_context, live_server, story_document, snapshots):
    page = new_context(java_script_enabled=False).new_page()
    page.goto(live_server + "/")
    assert_complete_story(page, story_document, snapshots)
    expect(page.locator("html")).not_to_have_class("enhanced")
    expect(page.locator("#sheet-status")).to_have_text("Opening stats; chapter snapshots follow.")
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
            "Opening stats; chapter snapshots follow."
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
        "marker-id",
        "chapter-id",
    ],
)
def test_invalid_projection_falls_back(page, live_server, game, story_document, snapshots, failure):
    projection = deepcopy(game)
    if failure == "version":
        projection["schema_version"] = 2
    elif failure == "boolean-stat":
        projection["events"][0]["stats_after"]["coding"] = True
    elif failure == "position":
        projection["events"][0]["position"]["x"] = 301
    elif failure == "empty-events":
        projection["events"] = []
    elif failure == "duplicate-badge":
        projection["events"][0]["badges_after"] *= 2
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
    expect(page.locator("#sheet-status")).to_have_text("Storybook mode; chapter snapshots follow.")
    expect(page.locator("html")).not_to_have_class("enhanced")
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
    expect(page.locator("#sheet-status")).to_have_text("Storybook mode; chapter snapshots follow.")
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
    page.emulate_media(reduced_motion="reduce")
    expect(page.locator("#traveler")).to_have_attribute("data-frame", "0")
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
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "11")
    page.keyboard.press("Home")
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "-1")
    page.keyboard.press("PageDown")
    expect(page.locator(".masthead")).not_to_be_in_viewport()
    page.keyboard.press("Home")
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", "-1")
    page.mouse.wheel(0, 500)
    expect(page.locator(".masthead")).not_to_be_in_viewport()


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
def test_local_axe_accessibility(page, live_server, project_root, width):
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
        return label.width && label.right > value.left;
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
    assert page.locator(".chapter-snapshot").nth(9).is_visible()
    selected = page.evaluate("""() => {
      const range = document.createRange();
      const paragraph = document.querySelector('[data-checkpoint="fog-arrives"] .story-prose');
      range.selectNodeContents(paragraph);
      const selection = window.getSelection();
      selection.removeAllRanges(); selection.addRange(range);
      return selection.toString();
    }""")
    assert "I burnt out" in selected
