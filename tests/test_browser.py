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
    expect(page.locator("#character-sheet")).to_be_visible()
    expect(page.locator("#character-sheet")).not_to_have_attribute("aria-hidden", "true")
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
        if visible:
            for paragraph in node.locator(".story-prose").all():
                expect(paragraph).to_be_visible()
    for index, expected in enumerate(snapshots[1:]):
        expect(cards.nth(index).locator(".chapter-stats dd")).to_have_text(
            [f"{value}/10" for value in expected["stats"].values()]
        )
    for discovery in story_document["discoveries"]:
        node = page.locator(f"#discovery-{discovery['id']}")
        expect(node.locator(".discovery-copy")).to_have_text(discovery["body"].split("\n\n"))
        if visible:
            expect(node).to_be_visible()
    expect(page.locator(".achievement-note")).to_have_count(24)
    if visible:
        for item in page.locator(".achievement-note").all():
            expect(item).to_be_visible()
    expect(page.locator(".loot")).to_have_count(0)
    for badge in story_document["badges"]:
        expect(page.locator(f'[data-quest-badge="{badge["id"]}"] .milestone-detail')).to_have_text(
            badge["description"]
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
          const {deriveState} = await import(document.querySelector('script[type="module"]').src);
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
    go_to_event(page, 1)
    beats = page.locator(".game-screen.is-current-screen .dialogue-beat")
    expect(beats).to_have_count(2)
    expect(beats.nth(0)).to_be_visible()
    expect(beats.nth(1)).to_be_hidden()
    expect(page.locator(".scene-hotspot:visible")).to_have_count(0)
    page.locator('[data-action="advance"]').click()
    expect(beats.nth(0)).to_be_hidden()
    expect(beats.nth(1)).to_be_visible()
    expect(page.locator("#quest-school-unlocked")).to_have_class(re.compile("is-unlocked"))
    go_to_event(page, 3)
    screen = page.locator(".game-screen.is-current-screen")
    beats = screen.locator(".dialogue-beat")
    expect(beats).to_have_count(4)
    expect(beats.nth(0)).to_be_visible()
    hotspot = page.locator('[data-discovery="gec-extras"]')
    expect(hotspot).to_be_visible()
    hotspot.click()
    expect(screen.locator(".dialogue-card")).to_be_visible()
    popup = page.locator("#discovery-gec-extras")
    expect(popup).to_be_visible()
    expect(popup.locator("h3")).to_be_focused()
    expect(popup.locator(".discovery-copy")).to_have_text(
        story_document["discoveries"][0]["body"].split("\n\n")
    )
    expect(page.locator("#discovery-early-projects")).to_be_hidden()
    expect(page.locator("#quest-gec-extras")).to_have_class(re.compile("is-unlocked"))
    expect(page.locator("#quest-early-projects")).not_to_have_class(re.compile("is-unlocked"))
    expect(page.locator("#advance-label")).to_have_text("Return to story")
    page.locator('[data-action="advance"]').click()
    expect(screen.locator(".dialogue-card")).to_be_visible()
    expect(popup).to_be_hidden()
    expect(hotspot).to_be_focused()

    expect(page.locator("#journey")).to_have_attribute("data-beat-index", "0")


def test_keyboard_and_touch_swipe_are_complete_game_controls(page, live_server):
    open_game(page, live_server)
    page.keyboard.press("ArrowRight")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "1")
    page.keyboard.press("ArrowLeft")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")

    page.evaluate("""() => {
      const shell = document.querySelector('.game-shell');
      shell.dispatchEvent(new PointerEvent('pointerdown', {
        pointerType: 'touch', isPrimary: true, clientX: 300, clientY: 300, bubbles: true
      }));
      shell.dispatchEvent(new PointerEvent('pointerup', {
        pointerType: 'touch', isPrimary: true, clientX: 210, clientY: 305, bubbles: true
      }));
    }""")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "1")
    page.evaluate("""() => {
      const shell = document.querySelector('.game-shell');
      shell.dispatchEvent(new PointerEvent('pointerdown', {
        pointerType: 'touch', isPrimary: true, clientX: 120, clientY: 300, bubbles: true
      }));
      shell.dispatchEvent(new PointerEvent('pointerup', {
        pointerType: 'touch', isPrimary: true, clientX: 220, clientY: 304, bubbles: true
      }));
    }""")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")
    page.locator('[data-action="toggle-quests"]').focus()
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

    expect(page.locator("#character-sheet")).to_be_visible()
    stats = page.locator("#character-sheet").bounding_box()
    assert 0 <= stats["x"] and stats["x"] + stats["width"] <= width + 1
    assert 0 <= stats["y"] and stats["y"] + stats["height"] <= height + 1
    assert stats["y"] + stats["height"] <= layout["scene"]["top"]
    for stat in page.locator("[data-stat]").all():
        expect(stat.locator(".stat-value")).to_be_visible()
        expect(stat.locator(".stat-pips")).to_be_visible()
    page.locator('[data-action="toggle-quests"]').click()
    overlay = page.locator("#bonus").bounding_box()
    assert overlay["y"] >= stats["y"] + stats["height"]


def test_quest_log_is_optional_overlay_and_restores_focus(page, live_server, story_document):
    open_game(page, live_server)
    button = page.locator('[data-action="toggle-quests"]')
    button.click()
    expect(page.locator("#bonus")).to_be_visible()
    expect(button).to_have_attribute("aria-expanded", "true")
    expect(page.locator("#bonus .achievement-note")).to_have_count(24)
    expect(page.locator("#bonus-title")).to_have_text("Quest log")
    expect(page.locator("#bonus .achievement-note:visible")).to_have_count(0)
    expect(page.locator(".quest-empty")).to_be_visible()
    assert page.locator(".story-deck").get_attribute("inert") is not None
    assert page.locator(".game-controls").get_attribute("inert") is not None
    page.keyboard.press("Tab")
    expect(page.locator('#bonus [data-action="close-panels"]')).to_be_focused()
    page.keyboard.press("ArrowRight")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")
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
    if resource in {"story.js", "story.css"}:
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
    for index in (0, 2, 4, 6, 7, 8, 9, 10, 11):
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
    for state in ("intro", "chapter", "discovery", "quests"):
        if state == "chapter":
            go_to_event(page, 6)
        elif state == "discovery":
            page.locator('[data-discovery="opportunity-hack"]').click()
        elif state == "quests":
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
      const nodes = document.querySelectorAll('.dialogue-card *, .game-controls *, .game-hud *');
      const sizes = [...nodes]
        .map(node => [node, parseFloat(getComputedStyle(node).fontSize)]);
      sizes.forEach(([node, size]) => { if (size) node.style.fontSize = `${size * 2}px`; });
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
    for row in page.locator("[data-stat]").all():
        assert row.evaluate("node => node.scrollWidth <= node.clientWidth + 1")


@pytest.mark.parametrize("width,height", [(320, 568), (390, 844), (1440, 1000)])
def test_every_dialogue_starts_in_view_and_short_screens_can_read_to_the_end(
    page, live_server, width, height
):
    page.set_viewport_size({"width": width, "height": height})
    open_game(page, live_server)
    for _ in range(70):
        data = page.evaluate("""() => {
          const screen = document.querySelector('.is-current-screen');
          const panel = screen.querySelector('.title-card, .dialogue-card');
          const beat = screen.querySelector('.is-current-beat');
          const bounds = panel.getBoundingClientRect();
          return {screen: document.querySelector('#journey').dataset.screenIndex,
            beat: document.querySelector('#journey').dataset.beatIndex,
            top: beat.getBoundingClientRect().top, panelTop: bounds.top, panelHeight: bounds.height,
            overflow: panel.scrollHeight - panel.clientHeight, scrollTop: panel.scrollTop};
        }""")
        assert data["panelHeight"] > 0 and data["top"] >= data["panelTop"]
        assert data["scrollTop"] == 0
        if width > 320:
            assert data["overflow"] <= 1, data
        else:
            panel = page.locator(
                ".is-current-screen .title-card, .is-current-screen .dialogue-card"
            )
            panel.evaluate("node => { node.scrollTop = node.scrollHeight; }")
            assert panel.evaluate("""node => node.querySelector('.is-current-beat')
              .getBoundingClientRect().bottom <= node.getBoundingClientRect().bottom""")
        if data["screen"] == "13" and data["beat"] == "4":
            break
        page.locator('[data-action="advance"]').click()
    else:
        raise AssertionError("The final dialogue was not reached")


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
    assert "find a pace I could keep up without burning myself out" in selected
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
    expect(page.locator(".scene-hotspot")).to_have_count(11)
    expect(page.locator("#scene-object-label")).to_have_count(0)
    expect(page.locator(".game-controls button")).to_have_count(2)
    expect(page.locator("#bonus .achievement-note")).to_have_count(24)
    assert page.locator('a[href="mailto:pranavprem93@gmail.com"]').count() == 1
    expect(page.locator(".pla-meme")).to_have_text("I'm 40% PLA.")
    slack_link = (
        "https://github.com/forcedotcom/einstein-bot-channel-connector/commits/master/"
        "?author=pranavprem"
    )
    expect(
        page.locator(f'[data-checkpoint="bots-unlocked"] .story-prose a[href="{slack_link}"]')
    ).to_have_text("public Slack connector")
    expect(page.locator(f'.discovery-panel a[href="{slack_link}"]')).to_have_count(0)
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


def test_scene_change_moves_focus_and_has_no_avatar_or_companion(page, live_server):
    open_game(page, live_server)
    page.locator('[data-action="advance"]').click()
    heading = page.locator(".game-screen.is-current-screen h2")
    expect(heading).to_be_focused()
    expect(page.locator("#traveler, #companion")).to_have_count(0)
    expect(page.locator("#journey-marker .object-sprite.current")).to_have_count(1)
    expect(page.locator("#world-label")).to_have_text("Goa")


def test_story_log_records_completed_chapters_and_survives_backtracking(
    page, live_server, quest_targets
):
    open_game(page, live_server)
    completed = set()
    for direction in ("advance", "back"):
        for _ in range(70):
            state = page.evaluate("""() => ({
              screen: Number(document.querySelector('#journey').dataset.screenIndex),
              beat: Number(document.querySelector('#journey').dataset.beatIndex),
              count: document.querySelector('.game-screen.is-current-screen')
                .querySelectorAll('.dialogue-beat').length
            })""")
            if state["screen"] > 0 and state["beat"] == state["count"] - 1:
                completed.add(state["screen"])
            expected = [
                key
                for key, (kind, screen) in quest_targets.items()
                if kind == "story" and screen in completed
            ]
            actual = page.locator(".achievement-note.is-unlocked").evaluate_all(
                "nodes => nodes.map(node => node.dataset.quest)"
            )
            assert actual == expected, state
            if (
                direction == "advance"
                and state["screen"] == 13
                and state["beat"] == state["count"] - 1
            ):
                page.locator('[data-action="advance"]').click()
                expect(page.locator("#bonus .achievement-note:visible")).to_have_count(13)
                expect(page.locator('[data-quest-kind="discovery"]:visible')).to_have_count(0)
                expect(page.locator(".quest-empty")).to_be_hidden()
                page.keyboard.press("Escape")
                expect(page.locator('[data-action="advance"]')).to_be_focused()
                break
            if direction == "back" and state["screen"] == state["beat"] == 0:
                break
            page.locator(f'[data-action="{direction}"]').click()
        else:
            raise AssertionError("The bounded journey did not reach its end")
    page.reload()
    expect(page.locator(".achievement-note.is-unlocked")).to_have_count(0)


@pytest.mark.parametrize("width,height", [(320, 568), (390, 844), (1440, 1000)])
def test_easter_eggs_follow_building_windows_and_popup_over_the_scene(
    page, live_server, width, height, story_document, quest_targets, discovery_positions
):
    page.set_viewport_size({"width": width, "height": height})
    open_game(page, live_server)
    for discovery_id, (x, y) in discovery_positions.items():
        target = quest_targets[discovery_id][1]
        while int(page.locator("#journey").get_attribute("data-screen-index")) < target:
            advance_to_next_screen(page)
        before = page.evaluate(HUD)
        screen = page.locator(".game-screen.is-current-screen")
        if target in {4, 6}:
            expect(screen.locator(".dialogue-beat")).to_have_count(4 if target == 4 else 2)
        hotspot = page.locator(f'[data-discovery="{discovery_id}"]')
        expect(page.locator(".scene-hotspot:visible")).to_have_count(
            sum(kind == "discovery" and dest == target for kind, dest in quest_targets.values())
        )
        boxes = [node.bounding_box() for node in page.locator(".scene-hotspot:visible").all()]
        for index, a in enumerate(boxes):
            for b in boxes[index + 1 :]:
                assert (
                    a["x"] + a["width"] <= b["x"] + 0.01
                    or b["x"] + b["width"] <= a["x"] + 0.01
                    or a["y"] + a["height"] <= b["y"] + 0.01
                    or b["y"] + b["height"] <= a["y"] + 0.01
                )
        rect = hotspot.bounding_box()
        art = page.locator(".scene-art").bounding_box()
        assert rect["width"] == pytest.approx(48, abs=0.001)
        assert rect["height"] == pytest.approx(48, abs=0.001)
        assert abs(rect["x"] + rect["width"] / 2 - (art["x"] + art["width"] * x / 320)) < 1
        assert abs(rect["y"] + rect["height"] / 2 - (art["y"] + art["height"] * y / 180)) < 1
        hotspot.focus()
        page.keyboard.press("Enter")
        popup = page.locator(f"#discovery-{discovery_id}")
        expect(popup).to_be_visible()
        expect(page.locator(".discovery-panel:visible")).to_have_count(1)
        expected = next(
            item for item in story_document["discoveries"] if item["id"] == discovery_id
        )
        expect(popup.locator(".discovery-copy")).to_have_text(expected["body"].split("\n\n"))
        assert page.evaluate(HUD) == before
        expect(page.locator(".is-current-screen .dialogue-card")).to_be_visible()
        scene = page.locator(".scene-panel").bounding_box()
        box = popup.bounding_box()
        assert scene["x"] <= box["x"] and box["x"] + box["width"] <= scene["x"] + scene["width"] + 1
        assert (
            scene["y"] <= box["y"] and box["y"] + box["height"] <= scene["y"] + scene["height"] + 1
        )
        popup.evaluate("node => { node.scrollTop = node.scrollHeight; }")
        expect(popup.locator(".discovery-copy, .project-links a").last).to_be_in_viewport()
        if discovery_id == "gec-extras":
            expect(
                popup.locator('a[href="https://github.com/pranavprem/ZuariSAPDetail"]')
            ).to_have_count(1)
            expect(popup.locator('a[href="https://github.com/pranavprem/fyp"]')).to_have_count(1)
        elif discovery_id == "green-belt":
            expect(popup.locator("a")).to_have_count(0)
        page.keyboard.press("Escape")
        expect(popup).to_be_hidden()
        expect(hotspot).to_be_focused()
        assert page.evaluate(HUD) == before


def test_discoveries_are_unique_outside_the_quest_log(page, live_server, story_document):
    open_game(page, live_server)
    copy = page.locator("#journey").evaluate(r"""node => {
      const clone = node.cloneNode(true);
      clone.querySelector('#bonus').remove();
      return clone.textContent.replace(/\s+/g, ' ').trim();
    }""")
    for discovery in story_document["discoveries"]:
        for paragraph in discovery["body"].split("\n\n"):
            assert copy.count(paragraph) == 1, discovery["id"]
    expect(page.locator(".loot")).to_have_count(0)
    assert (
        "Green Belt"
        not in page.locator('[data-checkpoint="automation-unlocked"] .dialogue-card').text_content()
    )
    assert (
        "Opportunity Hack"
        not in page.locator('[data-checkpoint="sjsu-unlocked"] .dialogue-card').text_content()
    )
    assert "Coldplay" not in " ".join(page.locator(".dialogue-card").all_text_contents())


def test_log_revisits_every_story_and_discovery_without_losing_entries(
    page, live_server, quest_targets, snapshots
):
    open_game(page, live_server)
    initial_url = page.url
    history_length = page.evaluate("history.length")
    # A locked, programmatically activated entry cannot skip ahead or add a URL fragment.
    page.locator('#quest-continuing-unlocked [data-action="revisit"]').dispatch_event("click")
    page.locator("#quest-continuing-unlocked").evaluate("node => node.classList.add('is-unlocked')")
    page.locator('#quest-continuing-unlocked [data-action="revisit"]').dispatch_event("click")
    expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")
    for target in range(1, 14):
        while int(page.locator("#journey").get_attribute("data-screen-index")) < target:
            advance_to_next_screen(page)
        for discovery_id, (kind, screen) in quest_targets.items():
            if kind == "discovery" and screen == target:
                page.locator(f'[data-discovery="{discovery_id}"]').click()
                expect(page.locator(f"#discovery-{discovery_id}")).to_be_visible()
                page.keyboard.press("Escape")
    for _ in range(4):
        page.locator('[data-action="advance"]').click()
    expect(page.locator(".achievement-note.is-unlocked")).to_have_count(24)
    for quest_id, (kind, target) in quest_targets.items():
        page.locator('[data-action="toggle-quests"]').click()
        expect(page.locator(".achievement-note:visible")).to_have_count(24)
        page.locator(f'#quest-{quest_id} [data-action="revisit"]').click()
        expect(page.locator("#bonus")).to_be_hidden()
        expect(page.locator("#journey")).to_have_attribute("data-screen-index", str(target))
        expect(page.locator("#journey")).to_have_attribute("data-beat-index", "0")
        assert_hud(page, snapshots[min(target, 12)])
        if kind == "discovery":
            popup = page.locator(f"#discovery-{quest_id}")
            expect(popup).to_be_visible()
            expect(popup.locator("h3")).to_be_focused()
            page.keyboard.press("Escape")
            expect(page.locator(f'[data-discovery="{quest_id}"]')).to_be_focused()
        else:
            expect(page.locator(".is-current-screen h2").first).to_be_focused()
        assert page.url == initial_url
        assert page.evaluate("history.length") == history_length
        expect(page.locator(".achievement-note.is-unlocked")).to_have_count(24)
    page.reload()
    expect(page.locator(".achievement-note.is-unlocked")).to_have_count(0)


@pytest.mark.parametrize("event,card", [(2, "unexpected-detour"), (9, "fog-arrives")])
def test_encounters_are_bounded_nonblocking_and_respect_motion_changes(
    page, live_server, event, card, snapshots
):
    page.add_init_script(
        "document.addEventListener('animationend', event => event.stopImmediatePropagation(), true)"
    )
    open_game(page, live_server)
    go_to_event(page, event)
    encounter = page.locator(f'[data-encounter="{card}"]')
    expect(encounter).to_be_visible()
    timings = encounter.evaluate(
        "node => node.getAnimations({subtree: true}).map(a => a.effect.getTiming())"
    )
    assert len(timings) == 1
    assert 0 < timings[0]["duration"] <= 2000 and timings[0]["iterations"] == 1
    assert_hud(page, snapshots[event + 1])
    page.wait_for_timeout(2050)
    assert encounter.evaluate("node => node.getAnimations({subtree: true}).length") == 0
    page.locator('[data-action="toggle-quests"]').click()
    page.keyboard.press("Escape")
    assert encounter.evaluate("node => node.getAnimations({subtree: true}).length") == 0
    advance_to_next_screen(page)
    expect(encounter).to_be_hidden()
    page.locator('[data-action="back"]').click()
    expect(encounter).to_be_visible()
    page.emulate_media(reduced_motion="reduce")
    expect(encounter).to_be_visible()
    expect(encounter).not_to_have_class(re.compile("can-animate"))
    assert encounter.evaluate("node => node.getAnimations({subtree: true}).length") == 0
    page.emulate_media(reduced_motion="no-preference")
    settle(page)
    assert encounter.evaluate("node => node.getAnimations({subtree: true}).length") == 0
    advance_to_next_screen(page)
    page.locator('[data-action="back"]').click()
    assert encounter.evaluate("node => node.getAnimations({subtree: true}).length") == 1
    # No event callback, delay, or combat action can hold navigation closed.
    advance_to_next_screen(page)
    expect(encounter).to_be_hidden()
    page.emulate_media(reduced_motion="reduce")
    page.locator('[data-action="back"]').click()
    expect(encounter).to_be_visible()
    assert encounter.evaluate("node => node.getAnimations({subtree: true}).length") == 0


def test_touch_cancellation_vertical_drags_and_buttons_do_not_advance(page, live_server):
    open_game(page, live_server)
    for mode in ("cancel", "vertical", "short", "button"):
        page.evaluate(
            """mode => {
          const target = document.querySelector(mode === 'button'
            ? '[data-action="toggle-quests"]' : '.game-shell');
          const fire = (name, x, y) => target.dispatchEvent(new PointerEvent(name, {
            pointerType: 'touch', isPrimary: true, pointerId: 1,
            clientX: x, clientY: y, bubbles: true
          }));
          fire('pointerdown', 200, 200);
          if (mode === 'cancel') fire('pointercancel', 200, 200);
          fire('pointerup', mode === 'short' ? 180 : 100, mode === 'vertical' ? 350 : 200);
        }""",
            mode,
        )
        expect(page.locator("#journey")).to_have_attribute("data-screen-index", "0")


@pytest.mark.parametrize("value", ["0", "14", "NaN"])
def test_invalid_quest_metadata_restores_the_complete_catalog(
    page, live_server, story_document, snapshots, value
):
    def replace_unlock(route):
        response = route.fetch()
        source = re.sub(
            r'data-target-screen="\d+"', f'data-target-screen="{value}"', response.text(), count=1
        )
        route.fulfill(response=response, body=source)

    page.route(live_server + "/", replace_unlock)
    page.goto(live_server + "/")
    expect(page.locator("html")).not_to_have_class("enhanced")
    assert_complete_story(page, story_document, snapshots, visible=True)


def test_pending_stylesheet_preserves_server_content_and_enhances_after_load(page, live_server):
    pending = []
    page.route("**/static/story.css*", lambda route: pending.append(route))
    page.goto(live_server + "/", wait_until="commit")
    expect(page.locator(".story-card")).to_have_count(12)
    expect(page.locator(".achievement-note")).to_have_count(24)
    expect(page.locator("html")).not_to_have_class("enhanced")
    assert len(pending) == 1
    pending[0].continue_()
    page.wait_for_load_state("load")
    expect(page.locator("html")).to_have_class("enhanced")
    expect(page.locator("#character-sheet")).to_be_visible()


@pytest.mark.parametrize(
    "old,new",
    [
        ('data-quest-kind="story"', 'data-quest-kind="unknown"'),
        ('data-quest="school-unlocked"', 'data-quest="first-script"'),
        ('data-x="249"', 'data-x="NaN"'),
        ('data-x="249"', 'data-x="900"'),
        ('data-discovery="gec-extras"', 'data-discovery="unknown"'),
        ('aria-controls="discovery-gec-extras"', 'aria-controls="character-sheet"'),
        ('href="#moment-first-script"', 'href="#moment-school-unlocked"'),
    ],
)
def test_malformed_discovery_or_jump_data_restores_full_story(
    page, live_server, story_document, snapshots, old, new
):
    def replace_metadata(route):
        response = route.fetch()
        source = response.text()
        assert old in source
        route.fulfill(response=response, body=source.replace(old, new, 1))

    page.route(live_server + "/", replace_metadata)
    page.goto(live_server + "/")
    expect(page.locator("html")).not_to_have_class("enhanced")
    assert_complete_story(page, story_document, snapshots, visible=True)
