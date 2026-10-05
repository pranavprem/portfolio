"""Real-engine checks for the chapter-adventure enhancement and readable fallback."""

import html
import json
import random
import re
from copy import deepcopy
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.browser

OBJECTS_BY_SNAPSHOT = [
    "controller",
    "controller",
    "backpack",
    "compass",
    "laptop",
    "java-mug",
    "automation-gear",
    "books",
    "toolkit",
    "cloud-terminal",
    "cloud-terminal",
    "bot-console",
    "agent-nodes",
]

HUD = """() => ({
  index: Number(document.getElementById('journey').dataset.checkpointIndex),
  screen: Number(document.getElementById('journey').dataset.screenIndex),
  beat: Number(document.getElementById('journey').dataset.beatIndex),
  stats: Object.fromEntries([...document.querySelectorAll('[data-stat]')]
    .map(row => [row.dataset.stat, Number(row.querySelector('.stat-value').textContent)])),
  pips: Object.fromEntries([...document.querySelectorAll('[data-stat]')]
    .map(row => [row.dataset.stat, row.querySelectorAll('.stat-pips > .filled').length])),
  badges: [...document.querySelectorAll('li[data-badge].earned')].map(node => node.dataset.badge),
  region: document.querySelector('[data-region-art].current').dataset.regionArt,
  mood: document.getElementById('overworld').dataset.mood,
  object: document.querySelector('#journey-marker .object-sprite.current').dataset.objectSprite,
  transform: document.getElementById('journey-object-track').getAttribute('transform')
})"""


def settle(page):
    page.evaluate("""async () => {
      await document.fonts.ready;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    }""")


def open_game(page, live_server):
    response = page.goto(live_server + "/")
    assert response.status == 200
    expect(page.locator("html")).to_have_class("enhanced")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")
    expect(page.locator('.game-screen[data-screen-kind="intro"]')).to_be_visible()
    settle(page)


def assert_hud(page, expected):
    actual = page.evaluate(HUD)
    for key in ("index", "stats", "badges", "region", "mood"):
        assert actual[key] == expected[key], (key, actual, expected)
    assert actual["object"] == OBJECTS_BY_SNAPSHOT[expected["index"] + 1]
    assert actual["pips"] == expected["stats"]
    expect(page.locator("#badge-count")).to_have_text(f"{len(expected['badges']):02d}")
    return actual


def advance_to_next_screen(page):
    before = int(page.locator("#journey").get_attribute("data-screen-index"))
    for _ in range(10):
        page.locator('[data-action="advance"]').click()
        after = int(page.locator("#journey").get_attribute("data-screen-index"))
        if after != before:
            settle(page)
            return after
    raise AssertionError("The current scene could not be completed")


def go_to_event(page, index):
    target_screen = index + 1
    while int(page.locator("#journey").get_attribute("data-screen-index")) < target_screen:
        advance_to_next_screen(page)
    expect(page.locator("#journey")).to_have_attribute("data-checkpoint-index", str(index))


def assert_complete_story(page, story_document, snapshots, *, visible):
    expect(page.locator(".chapter")).to_have_count(11)
    cards = page.locator(".story-card[data-checkpoint]")
    expect(cards).to_have_count(12)
    for card in [card for chapter in story_document["chapters"] for card in chapter["cards"]]:
        node = page.locator(f'[data-checkpoint="{card["id"]}"]')
        expect(node.locator(".story-prose")).to_have_text(card["body"].split("\n\n"))
        expect(node.locator(".field-notes li")).to_have_text(card["facts"])
        if visible:
            for paragraph in node.locator(".story-prose").all():
                expect(paragraph).to_be_visible()
    for index, expected in enumerate(snapshots[1:]):
        expect(cards.nth(index).locator(".chapter-stats dd")).to_have_text(
            [f"{value}/10" for value in expected["stats"].values()]
        )
    expect(page.locator(".achievement-note")).to_have_count(len(story_document["achievements"]))
    expect(page.locator(".loot strong")).to_have_text(
        [badge["label"] for badge in story_document["badges"]]
    )


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


def test_pure_chapter_state_is_absolute_and_order_independent(page, live_server, game, snapshots):
    open_game(page, live_server)
    indexes = list(range(-4, 17)) * 3
    random.Random(20261004).shuffle(indexes)  # noqa: S311 - deterministic test order
    result = page.evaluate(
        """async ({game, indexes}) => {
          const {deriveState} = await import('/static/story.js');
          const before = JSON.stringify(game);
          return {states: indexes.map(index => deriveState(game, index)),
            unchanged: JSON.stringify(game) === before};
        }""",
        {"game": game, "indexes": indexes},
    )
    assert result["unchanged"]
    seen = {}
    for requested, state in zip(indexes, result["states"], strict=True):
        index = max(-1, min(requested, 11))
        expected = snapshots[index + 1]
        for key in ("index", "stats", "badges", "region", "mood"):
            assert state[key] == expected[key]
        assert state["object"] == OBJECTS_BY_SNAPSHOT[index + 1]
        assert 20 <= state["position"]["x"] <= 300
        assert 0 <= state["position"]["y"] <= 180
        if requested in seen:
            assert state == seen[requested]
        seen[requested] = state


def test_buttons_play_every_chapter_and_backtrack_exactly(page, live_server, snapshots):
    open_game(page, live_server)
    assert_hud(page, snapshots[0])
    for index in range(12):
        assert advance_to_next_screen(page) == index + 1
        state = assert_hud(page, snapshots[index + 1])
        expect(page.locator(".game-screen.is-current-screen")).to_have_attribute(
            "data-checkpoint", snapshots[index + 1]["id"]
        )
        expect(page.locator("#sheet-status")).to_contain_text("Chapter")
        assert state["screen"] == index + 1

    assert advance_to_next_screen(page) == 13
    expect(page.locator('.game-screen[data-screen-kind="ending"]')).to_be_visible()
    assert_hud(page, snapshots[-1])

    # Back rewinds dialogue first, then returns to the previous deterministic checkpoint.
    page.locator('[data-action="back"]').click()
    expect(page.locator("#journey")).to_have_attribute("data-beat-index", "2")
    for _ in range(2):
        page.locator('[data-action="back"]').click()
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "12")
    assert_hud(page, snapshots[-1])


def test_dialogue_is_part_of_play_and_scene_hotspots_reveal_discoveries(
    page, live_server, story_document
):
    open_game(page, live_server)
    go_to_event(page, 0)
    screen = page.locator(".game-screen.is-current-screen")
    beats = screen.locator(".dialogue-beat")
    expect(beats).to_have_count(1)
    expect(beats).to_be_visible()
    expect(page.locator('[data-action="inspect"]')).to_be_visible()
    page.locator('[data-action="inspect"]').click()
    expect(screen.locator(".dialogue-card")).to_be_hidden()
    expect(screen.locator(".discovery-panel")).to_be_visible()
    expect(screen.locator(".field-notes li")).to_have_text(
        story_document["chapters"][0]["cards"][0]["facts"]
    )
    expect(page.locator("#advance-label")).to_have_text("Return to story")
    page.locator('[data-action="advance"]').click()
    expect(screen.locator(".dialogue-card")).to_be_visible()

    go_to_event(page, 1)
    beats = page.locator(".game-screen.is-current-screen .dialogue-beat")
    expect(beats).to_have_count(2)
    expect(beats.nth(0)).to_be_visible()
    expect(beats.nth(1)).to_be_hidden()
    page.locator('[data-action="advance"]').click()
    expect(beats.nth(0)).to_be_hidden()
    expect(beats.nth(1)).to_be_visible()
    expect(page.locator(".game-screen.is-current-screen .loot")).to_be_visible()


def test_keyboard_and_touch_swipe_are_complete_game_controls(page, live_server):
    open_game(page, live_server)
    page.keyboard.press("ArrowRight")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "1")
    page.keyboard.press("ArrowLeft")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")

    page.evaluate("""() => {
      const shell = document.querySelector('.game-shell');
      shell.dispatchEvent(new PointerEvent('pointerdown', {
        pointerType: 'touch', clientX: 300, clientY: 300, bubbles: true
      }));
      shell.dispatchEvent(new PointerEvent('pointerup', {
        pointerType: 'touch', clientX: 210, clientY: 305, bubbles: true
      }));
    }""")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "1")
    page.evaluate("""() => {
      const shell = document.querySelector('.game-shell');
      shell.dispatchEvent(new PointerEvent('pointerdown', {
        pointerType: 'touch', clientX: 120, clientY: 300, bubbles: true
      }));
      shell.dispatchEvent(new PointerEvent('pointerup', {
        pointerType: 'touch', clientX: 220, clientY: 304, bubbles: true
      }));
    }""")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")
    page.locator('[data-action="toggle-stats"]').focus()
    page.keyboard.press("ArrowRight")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")


@pytest.mark.parametrize("width,height", [(320, 568), (390, 844), (768, 1024), (1440, 1000)])
def test_mobile_first_game_fills_viewport_without_page_scrolling(page, live_server, width, height):
    page.set_viewport_size({"width": width, "height": height})
    open_game(page, live_server)
    go_to_event(page, 3)
    layout = page.evaluate("""() => {
      const shell = document.querySelector('.game-shell').getBoundingClientRect();
      const scene = document.querySelector('.scene-panel').getBoundingClientRect();
      const story = document.querySelector('.game-screen.is-current-screen')
        .getBoundingClientRect();
      const controls = document.querySelector('.game-controls').getBoundingClientRect();
      return {
        innerWidth, innerHeight, scrollWidth: document.documentElement.scrollWidth,
        scrollHeight: document.documentElement.scrollHeight,
        shell: {top: shell.top, bottom: shell.bottom, left: shell.left, right: shell.right},
        scene: {top: scene.top, bottom: scene.bottom, left: scene.left, right: scene.right},
        story: {top: story.top, bottom: story.bottom, left: story.left, right: story.right},
        controls: {top: controls.top, bottom: controls.bottom},
        buttons: [...document.querySelectorAll('.game-controls button')]
          .map(node => node.getBoundingClientRect().height)
      };
    }""")
    assert layout["scrollWidth"] <= width + 1
    assert layout["scrollHeight"] <= height + 1
    assert 0 <= layout["shell"]["top"] < layout["shell"]["bottom"] <= height + 1
    if width <= 760:
        assert layout["scene"]["bottom"] <= layout["story"]["top"] + 1
    assert layout["controls"]["bottom"] <= height + 1
    assert min(layout["buttons"]) >= 48
    expect(page.locator(".scene-panel")).to_be_visible()
    expect(page.locator(".game-screen.is-current-screen")).to_be_visible()

    page.locator('[data-action="toggle-stats"]').click()
    expect(page.locator("#character-sheet")).to_be_visible()
    stats = page.locator("#character-sheet").bounding_box()
    assert 0 <= stats["x"] and stats["x"] + stats["width"] <= width + 1
    assert 0 <= stats["y"] and stats["y"] + stats["height"] <= height + 1
    page.locator('#character-sheet [data-action="close-panels"]').click()


def test_quest_log_is_optional_overlay_and_restores_focus(page, live_server, story_document):
    open_game(page, live_server)
    button = page.locator('[data-action="toggle-quests"]')
    button.click()
    expect(page.locator("#bonus")).to_be_visible()
    expect(button).to_have_attribute("aria-expanded", "true")
    expect(page.locator("#bonus .achievement-note")).to_have_count(
        len(story_document["achievements"])
    )
    assert page.locator(".game-shell").get_attribute("inert") is not None
    page.keyboard.press("Escape")
    expect(page.locator("#bonus")).to_be_hidden()
    expect(button).to_be_focused()
    expect(button).to_have_attribute("aria-expanded", "false")


def test_no_javascript_and_script_failure_keep_complete_readable_story(
    new_context, live_server, story_document, snapshots
):
    page = new_context(java_script_enabled=False).new_page()
    page.goto(live_server + "/")
    assert_complete_story(page, story_document, snapshots, visible=True)
    expect(page.locator("html")).not_to_have_class("enhanced")
    expect(page.locator(".fallback-landscape")).to_have_count(11)
    expect(page.locator(".game-controls")).to_be_hidden()
    expect(page.locator(".scene-panel")).to_be_hidden()
    expect(page.locator("#character-sheet")).to_be_visible()


@pytest.mark.parametrize("resource", ["story.js", "story.css", "art/goa.svg"])
def test_failed_local_resource_never_removes_content(
    page, live_server, story_document, snapshots, resource
):
    page.route(f"**/static/{resource}*", lambda route: route.abort())
    page.goto(live_server + "/")
    assert_complete_story(
        page, story_document, snapshots, visible=resource in {"story.js", "story.css"}
    )
    if resource == "story.js":
        expect(page.locator("html")).not_to_have_class("enhanced")


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
    expect(page.locator("html")).not_to_have_class("enhanced")
    expect(page.locator("#sheet-status")).to_have_text("Opening stats. The complete story follows.")
    assert_complete_story(page, story_document, snapshots, visible=True)


def test_reduced_motion_disables_reactions_but_keeps_game_state(page, live_server, snapshots):
    page.emulate_media(reduced_motion="reduce")
    open_game(page, live_server)
    go_to_event(page, 1)
    page.locator('[data-action="advance"]').click()
    expect(page.locator("#journey-marker")).not_to_have_class(re.compile("is-celebrating"))
    assert page.locator("#journey-marker").evaluate("node => node.getAnimations().length") == 0
    assert_hud(page, snapshots[2])


def test_csp_privacy_and_idle_scene_are_clean(page, live_server, observations, snapshots):
    open_game(page, live_server)
    for index in (0, 4, 8, 9, 11):
        go_to_event(page, index)
        assert_hud(page, snapshots[index + 1])
    page.wait_for_timeout(500)
    idle = page.evaluate("""() => ({
      animations: document.getAnimations().length,
      local: localStorage.length,
      session: sessionStorage.length,
      cookies: document.cookie,
      scrollY: window.scrollY
    })""")
    assert idle == {"animations": 0, "local": 0, "session": 0, "cookies": "", "scrollY": 0}
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
    page.set_viewport_size({"width": width, "height": 900})
    open_game(page, live_server)
    axe_path = project_root / "node_modules/axe-core/axe.min.js"
    assert axe_path.is_file(), "Run npm ci to install the pinned local axe-core dependency"
    page.evaluate(axe_path.read_text(encoding="utf-8"))
    for state in ("intro", "chapter", "stats", "quests"):
        if state == "chapter":
            go_to_event(page, 9)
        elif state == "stats":
            page.locator('[data-action="toggle-stats"]').click()
        elif state == "quests":
            page.locator('#character-sheet [data-action="close-panels"]').click()
            page.locator('[data-action="toggle-quests"]').click()
        violations = page.evaluate("""async () => {
          const result = await axe.run(document, {runOnly: {
            type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
          }});
          return result.violations.map(({id, impact, nodes}) => ({id, impact,
            nodes: nodes.map(({target, failureSummary}) => ({target, failureSummary}))}));
        }""")
        assert violations == [], json.dumps(violations, indent=2)


def test_text_enlargement_keeps_controls_and_current_dialogue_reachable(page, live_server):
    page.set_viewport_size({"width": 320, "height": 700})
    open_game(page, live_server)
    go_to_event(page, 3)
    page.evaluate("""() => {
      document.querySelectorAll('.dialogue-card *, .game-controls *, .game-hud *')
        .forEach(node => {
          const size = parseFloat(getComputedStyle(node).fontSize);
          if (size) node.style.fontSize = `${size * 1.8}px`;
        });
    }""")
    settle(page)
    layout = page.evaluate("""() => ({
      width: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
      next: document.querySelector('[data-action=advance]').getBoundingClientRect(),
      story: document.querySelector('.game-screen.is-current-screen').getBoundingClientRect()
    })""")
    assert layout["scrollWidth"] <= layout["width"] + 1
    assert 0 <= layout["next"]["top"] < layout["next"]["bottom"] <= 700
    assert layout["story"]["height"] > 0
    expect(page.locator(".game-screen.is-current-screen .dialogue-card")).to_be_visible()


def test_print_and_no_js_keep_every_paragraph_and_snapshot(
    page, live_server, story_document, snapshots
):
    open_game(page, live_server)
    page.emulate_media(media="print")
    assert_complete_story(page, story_document, snapshots, visible=True)
    expect(page.locator(".game-hud")).to_be_hidden()
    expect(page.locator(".scene-panel")).to_be_hidden()
    expect(page.locator(".ending")).to_be_visible()


def test_forced_colors_selection_and_findable_text(page, live_server):
    page.emulate_media(forced_colors="active")
    open_game(page, live_server)
    go_to_event(page, 9)
    selected = page.evaluate("""() => {
      const paragraph = document.querySelector('[data-checkpoint="fog-arrives"] .story-prose');
      const range = document.createRange();
      range.selectNodeContents(paragraph);
      const selection = window.getSelection();
      selection.removeAllRanges(); selection.addRange(range);
      return selection.toString();
    }""")
    assert "new cadence of contribution" in selected
    expect(page.locator('[data-action="advance"]')).to_be_visible()


def test_story_budget_links_and_game_surface(page, live_server, story_document):
    open_game(page, live_server)
    words = page.locator("#main-story").evaluate(r"""node => {
      const copy = node.cloneNode(true);
      copy.querySelectorAll(
        '.chapter-header, .chapter-stats, .scene-period, .scene-heading, ' +
        '.story-card h3, .discovery-panel, .loot, .input-hint, .project-links'
      )
        .forEach(element => element.remove());
      return copy.textContent.trim().split(/\s+/).length;
    }""")
    assert words <= 900, f"Main story is {words} words"
    expect(page.locator("[data-stat]")).to_have_count(5)
    expect(page.locator(".scene-hotspot")).to_have_count(1)
    expect(page.locator(".game-controls button")).to_have_count(2)
    expect(page.locator("#bonus .achievement-note")).to_have_count(
        len(story_document["achievements"])
    )
    assert page.locator('a[href="mailto:pranavprem93@gmail.com"]').count() == 1
    expect(page.locator(".pla-meme")).to_have_text("I'm 40% PLA.")
    assert page.locator("iframe, video, canvas").count() == 0


@pytest.mark.parametrize("width", [390, 1440])
def test_dark_mode_does_not_reset_game(page, live_server, snapshots, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(color_scheme="light")
    open_game(page, live_server)
    go_to_event(page, 8)
    before = page.evaluate(HUD)
    page.emulate_media(color_scheme="dark")
    settle(page)
    assert page.evaluate(HUD) == before
    assert_hud(page, snapshots[9])
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")


def test_scene_change_moves_focus_and_has_no_living_sprites(page, live_server):
    open_game(page, live_server)
    page.locator('[data-action="advance"]').click()
    heading = page.locator(".game-screen.is-current-screen h2")
    expect(heading).to_be_focused()
    expect(page.locator("#traveler, #companion")).to_have_count(0)
    expect(page.locator("#journey-marker .object-sprite.current")).to_have_count(1)
    expect(page.locator("#world-label")).to_have_text("Goa")
