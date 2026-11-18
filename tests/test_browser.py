"""Real-engine checks for the scrolling-world enhancement and its readable fallback."""

import html
import json
import random
import re
from copy import deepcopy
from urllib.parse import urlsplit

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.browser

# Independent oracle: one traveller object per chapter, held through the ending.
OBJECTS = [
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
    "agent-nodes",
]
PLACES = {"goa": "Goa", "pune": "Pune", "san-jose": "San Jose", "bay-area": "San Francisco"}
VIEWPORTS = [(320, 568), (375, 667), (390, 844), (1440, 1000)]

STATE = """() => {
  const stage = document.getElementById('stage');
  const rows = [...stage.querySelectorAll('[data-stat]')];
  return {
    stop: stage.dataset.stop,
    mood: stage.dataset.mood,
    stats: Object.fromEntries(rows.map(row =>
      [row.dataset.stat, Number(row.querySelector('.stat-value').textContent)])),
    pips: Object.fromEntries(rows.map(row =>
      [row.dataset.stat, row.querySelectorAll('.stat-pips > .on').length])),
    deltas: Object.fromEntries(rows.map(row =>
      [row.dataset.stat, row.querySelector('.stat-delta').textContent])),
    object: document.querySelector('#marker .object-sprite.current').dataset.objectSprite,
    place: document.getElementById('place').textContent,
    count: document.getElementById('route-count').textContent,
    current: [...document.querySelectorAll('#route a[aria-current="true"]')]
      .map(link => link.getAttribute('href')),
  };
}"""

GEOMETRY = """() => {
  const box = node => {
    const {left, right, top, bottom, width, height} = node.getBoundingClientRect();
    return {left, right, top, bottom, width, height};
  };
  return {
    viewport: box(document.querySelector('.viewport')),
    marker: box(document.getElementById('marker')),
    world: box(document.getElementById('world')),
    hotspots: [...document.querySelectorAll('.hotspot:not([hidden])')].map(node =>
      ({id: node.dataset.extraTarget, ...box(node)})),
  };
}"""


def settle(page):
    page.evaluate("""async () => {
      await document.fonts.ready;
      for (let i = 0; i < 4; i += 1) await new Promise(resolve => requestAnimationFrame(resolve));
    }""")


def open_world(page, live_server):
    response = page.goto(live_server + "/")
    assert response.status == 200
    expect(page.locator("html")).to_have_class("is-world")
    expect(page.locator("#stage")).to_have_attribute("data-stop", "title")
    settle(page)


def section_ids(snapshots):
    return ["top", *(f"moment-{item['id']}" for item in snapshots[1:]), "epilogue"]


def go_to_stop(page, section_id):
    # An instant anchor-style jump: the state must not depend on the route taken.
    page.evaluate("id => document.getElementById(id).scrollIntoView()", section_id)
    settle(page)


def expected_states(snapshots):
    """Title, twelve authored checkpoints, then the ending holding the final sheet."""
    states = []
    for index, item in enumerate([*snapshots, snapshots[-1]]):
        ending = index == len(snapshots)
        states.append(
            {
                "stop": "epilogue" if ending else item["id"] or "title",
                "mood": item["mood"],
                "stats": item["stats"],
                "pips": item["stats"],
                "object": OBJECTS[index],
                "place": "San Jose" if ending else PLACES[item["region"]],
                "count": "" if index == 0 else f"{index} / 13",
            }
        )
    return states


def assert_state(page, expected):
    actual = page.evaluate(STATE)
    for key, value in expected.items():
        assert actual[key] == value, (key, actual, expected)
    return actual


def paragraphs_of(story_document):
    for chapter in story_document["chapters"]:
        for card in chapter["cards"]:
            yield card, card["body"].split("\n\n")


def assert_complete_story(page, story_document, snapshots, *, visible):
    expect(page.locator("section.stop")).to_have_count(14)
    for card, paragraphs in paragraphs_of(story_document):
        for index, paragraph in enumerate(paragraphs):
            node = page.locator(f"#beat-{card['id']}-{index}")
            expect(node).to_have_text(paragraph)
            if visible:
                expect(node).to_be_visible()
    for index, expected in enumerate(snapshots[1:]):
        expect(page.locator(".chapter-stats").nth(index).locator("dd")).to_have_text(
            [f"{value}/10" for value in expected["stats"].values()]
        )
    for discovery in story_document["discoveries"]:
        node = page.locator(f"#discovery-{discovery['id']}")
        expect(node.locator(":scope > p:not(.project-links)")).to_have_text(
            discovery["body"].split("\n\n")
        )
        expect(node.locator(".extra-list > li")).to_have_text(discovery.get("list_items", []))
        expect(node.locator(".project-links a")).to_have_count(len(discovery["links"]))
        if visible:
            expect(node.locator(":scope > p").first).to_be_visible()
    printing = page.locator("#beat-epilogue-3")
    expect(printing).to_contain_text("MakerWorld, Bambu Studio, and Autodesk Fusion")
    expect(printing).to_contain_text("Retail therapy? Nah, I'll make my own stuff.")
    expect(printing.locator(".pla-meme")).to_have_text("I'm 40% PLA.")
    if visible:
        expect(printing.locator(".pla-meme")).to_be_visible()
        expect(page.locator(".postcard img")).to_have_count(13)
        expect(page.locator(".postcard img").first).to_be_visible()
    expect(page.locator('a[href="mailto:pranavprem93@gmail.com"]')).to_have_count(1)


def assert_linear(page, story_document, snapshots):
    expect(page.locator("html")).not_to_have_class("is-world")
    expect(page.locator("#stage")).to_be_hidden()
    assert_complete_story(page, story_document, snapshots, visible=True)


def serve_with_game(page, live_server, projection):
    def replace(route):
        response = route.fetch()
        source = response.text()
        attribute = re.search(r'data-game="([^"]*)"', source)
        assert attribute is not None
        value = projection if isinstance(projection, str) else json.dumps(projection)
        route.fulfill(
            response=response, body=source.replace(attribute[1], html.escape(value, quote=True))
        )

    page.route(live_server + "/", replace)
    page.goto(live_server + "/")


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


def test_pure_stop_state_is_absolute_and_order_independent(page, live_server, game, snapshots):
    open_world(page, live_server)
    # Import the already-loaded versioned module so the page is not enhanced twice.
    result = page.evaluate(
        """async ({game, order}) => {
          const src = document.querySelector('script[type="module"]').src;
          const {deriveStop, worldX, locate, isValidGame} = await import(src);
          return {
            valid: isValidGame(game),
            stops: order.map(index => [index, deriveStop(game, index)]),
            clamped: [deriveStop(game, -5).id, deriveStop(game, 99).id, deriveStop(game, NaN).id],
            tiles: ['goa', 'pune', 'san-jose', 'bay-area', 'san-jose-home']
              .map(tile => worldX(tile, 0)),
            held: locate([0, 1000, 2000], 3000, 500),
            walking: locate([0, 1000, 2000], 3000, 900),
            arrived: locate([0, 1000, 2000], 3000, 1000),
            last: locate([0, 1000, 2000], 3000, 2990),
          };
        }""",
        {"game": game, "order": random.Random(7).sample(range(14), 14)},  # noqa: S311
    )
    assert result["valid"] is True
    assert result["clamped"] == ["title", "epilogue", "title"]
    assert result["tiles"] == [0, 328, 656, 984, 1312]
    for index, stop in result["stops"]:
        expected = snapshots[min(index, 12)]
        assert stop["stats"] == expected["stats"], index
        assert stop["mood"] == expected["mood"], index
        assert stop["tile"] == ("san-jose-home" if index == 13 else expected["region"]), index
    assert result["held"] == {"index": 0, "travel": 0}
    assert result["walking"]["index"] == 0 and 0 < result["walking"]["travel"] < 1
    assert result["arrived"] == {"index": 1, "travel": 0}
    assert result["last"] == {"index": 2, "travel": 0}


@pytest.mark.parametrize("width,height", [(390, 844), (1440, 1000)])
def test_every_stop_shows_its_absolute_sheet_in_any_order(
    page, live_server, snapshots, width, height
):
    page.set_viewport_size({"width": width, "height": height})
    open_world(page, live_server)
    ids = section_ids(snapshots)
    states = expected_states(snapshots)
    order = list(range(14)) + random.Random(11).sample(range(14), 14)  # noqa: S311
    for index in order:
        go_to_stop(page, ids[index])
        actual = assert_state(page, states[index])
        assert actual["current"] == ([] if index == 0 else ["#" + ids[index]])
    go_to_stop(page, "moment-unexpected-detour")
    # Arrows carry the direction; the change is relative to the previous stop in the story.
    assert page.evaluate(STATE)["deltas"] == {
        "coding": "",
        "enthusiasm": "▼3",
        "vitality": "▼5",
        "charisma": "",
        "experience": "",
    }


@pytest.mark.parametrize("width,height", VIEWPORTS)
def test_camera_keeps_traveller_and_current_extras_in_the_scene(
    page, live_server, snapshots, quest_targets, width, height
):
    page.set_viewport_size({"width": width, "height": height})
    open_world(page, live_server)
    extras_by_screen = {}
    for quest, (kind, screen) in quest_targets.items():
        if kind == "discovery":
            extras_by_screen.setdefault(screen, set()).add(quest)
    seen_offsets = set()
    for index, section_id in enumerate(section_ids(snapshots)):
        go_to_stop(page, section_id)
        geometry = page.evaluate(GEOMETRY)
        view, marker = geometry["viewport"], geometry["marker"]
        assert view["left"] <= marker["left"] and marker["right"] <= view["right"], section_id
        assert view["top"] <= marker["top"] and marker["bottom"] <= view["bottom"] + 1, section_id
        # The strip always covers the scene: no blank edge at either end of the world.
        assert geometry["world"]["left"] <= view["left"] + 0.5
        assert geometry["world"]["right"] >= view["right"] - 0.5
        assert {spot["id"] for spot in geometry["hotspots"]} == extras_by_screen.get(index, set())
        offscreen = []
        for spot in geometry["hotspots"]:
            assert spot["width"] >= 47.999 and spot["height"] >= 47.999
            centre = (spot["left"] + spot["right"]) / 2
            if not view["left"] < centre < view["right"]:
                offscreen.append(spot["id"])
        # One scene is wider than a tall phone can show at once: the traveller stands
        # 196 scene units from the far window. That extra stays reachable under More.
        too_wide = section_id == "moment-continuing-unlocked" and width < 400 < height
        assert offscreen == (["career-titles"] if too_wide and offscreen else []), section_id
        spots = geometry["hotspots"]
        for first in spots:
            for second in spots:
                if first["id"] < second["id"]:
                    apart = max(
                        abs(first["left"] - second["left"]), abs(first["top"] - second["top"])
                    )
                    assert apart >= 47.999, (first["id"], second["id"])
        seen_offsets.add(round(geometry["world"]["left"]))
    # The scene really travels: Goa, Pune, San Jose, San Francisco and home differ.
    assert len(seen_offsets) >= 5


def test_scrolling_walks_between_stops_and_reduced_motion_steps(page, live_server):
    page.set_viewport_size({"width": 390, "height": 844})
    open_world(page, live_server)

    def offsets():
        return page.evaluate("""async () => {
          // Firefox delivers the scroll event a frame later than the other engines.
          const frame = () => new Promise(resolve => requestAnimationFrame(resolve));
          const settle = async () => { for (let i = 0; i < 4; i += 1) await frame(); };
          const world = document.getElementById('world');
          const from = document.getElementById('moment-college-unlocked');
          const to = document.getElementById('moment-java-unlocked');
          const left = () => world.getBoundingClientRect().left;
          const stage = document.getElementById('stage');
          const pinned = stage.clientHeight >= innerHeight - 1 ? 0 : stage.clientHeight;
          // Plain scrollTo throughout: Firefox re-applies a scrollIntoView target on
          // the next frame, which would undo the programmatic scroll that follows.
          scrollTo(0, from.getBoundingClientRect().top + scrollY - pinned); await settle();
          const start = left();
          // Two thirds of the way through the reading area's approach to the next stop.
          const reading = innerHeight - document.getElementById('stage').clientHeight;
          scrollTo(0, to.getBoundingClientRect().top + scrollY - innerHeight + reading * 0.25);
          await settle();
          const middle = left();
          const stop = document.getElementById('stage').dataset.stop;
          scrollTo(0, to.getBoundingClientRect().top + scrollY - pinned); await settle();
          return {start, middle, stop, end: left()};
        }""")

    walking = offsets()
    assert walking["stop"] == "college-unlocked"
    assert walking["end"] < walking["middle"] < walking["start"]
    page.emulate_media(reduced_motion="reduce")
    stepped = offsets()
    assert stepped["middle"] == stepped["start"] and stepped["end"] == walking["end"]
    assert page.evaluate("document.getAnimations().length") == 0


def test_disclosures_start_closed_and_reveal_every_paragraph(page, live_server, story_document):
    open_world(page, live_server)
    expect(page.locator("details[open]")).to_have_count(0)
    for card, paragraphs in paragraphs_of(story_document):
        go_to_stop(page, f"moment-{card['id']}")
        section = page.locator(f"#moment-{card['id']}")
        expect(section.locator(".lead")).to_have_text(paragraphs[0])
        expect(section.locator(".lead")).to_be_visible()
        expect(section.locator("h2")).to_be_in_viewport()
        if len(paragraphs) == 1 and section.locator("details.more").count() == 0:
            continue
        expect(section.locator(f"#beat-{card['id']}-1")).to_be_hidden()
        section.locator("details.more > summary").click()
        for index in range(1, len(paragraphs)):
            expect(section.locator(f"#beat-{card['id']}-{index}")).to_be_visible()
        section.locator("details.more > summary").click()
        expect(section.locator("details.more")).not_to_have_attribute("open", "")


@pytest.mark.parametrize("width,height", [(375, 667), (1440, 1000)])
def test_scene_hotspots_open_and_focus_their_extras(
    page, live_server, story_document, quest_targets, snapshots, width, height
):
    page.set_viewport_size({"width": width, "height": height})
    open_world(page, live_server)
    ids = section_ids(snapshots)
    for discovery in story_document["discoveries"]:
        go_to_stop(page, ids[quest_targets[discovery["id"]][1]])
        hotspot = page.locator(f'.hotspot[data-extra-target="{discovery["id"]}"]')
        extra = page.locator(f"#discovery-{discovery['id']}")
        expect(hotspot).to_have_attribute("aria-expanded", "false")
        expect(extra.locator(":scope > p").first).to_be_hidden()
        # Some wide-layout windows sit behind the placard; the control must still work.
        hotspot.dispatch_event("click")
        expect(hotspot).to_have_attribute("aria-expanded", "true")
        expect(extra.locator("summary")).to_be_focused()
        expect(extra.locator(":scope > p").first).to_be_visible()
        expect(extra.locator("summary")).to_be_in_viewport()
        extra.locator("summary").click()
        expect(hotspot).to_have_attribute("aria-expanded", "false")


def test_coldplay_cameo_is_a_gec_extra_with_the_exact_link(page, live_server):
    open_world(page, live_server)
    go_to_stop(page, "moment-college-unlocked")
    page.locator('.hotspot[data-extra-target="coldplay"]').dispatch_event("click")
    extra = page.locator("#moment-college-unlocked #discovery-coldplay")
    expect(extra).to_contain_text("That's my silhouette at 3:41")
    expect(extra.locator("a")).to_have_attribute("href", "https://youtu.be/ogItgrO9GSg?t=221")


@pytest.mark.parametrize("width,height", [(375, 667), (1440, 1000)])
def test_route_menu_jumps_anywhere_and_restores_focus(page, live_server, snapshots, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.emulate_media(reduced_motion="reduce")
    open_world(page, live_server)
    summary = page.locator("#route > summary")
    links = page.locator("#route a")
    expect(links).to_have_count(13)
    summary.click()
    expect(links.first).to_be_visible()
    box = links.nth(6).bounding_box()
    assert box["height"] >= 47.999
    page.keyboard.press("Escape")
    expect(links.first).to_be_hidden()
    expect(summary).to_be_focused()
    summary.click()
    links.nth(6).click()
    expect(links.first).to_be_hidden()
    expect(page.locator("#stage")).to_have_attribute("data-stop", "sjsu-unlocked")
    assert_state(page, expected_states(snapshots)[7])
    summary.click()
    links.nth(12).click()
    expect(page.locator("#stage")).to_have_attribute("data-stop", "epilogue")


def test_arrow_keys_step_between_stops_without_stealing_other_input(page, live_server):
    page.emulate_media(reduced_motion="reduce")
    open_world(page, live_server)
    stage = page.locator("#stage")
    page.keyboard.press("ArrowRight")
    expect(stage).to_have_attribute("data-stop", "first-script")
    page.keyboard.press("ArrowRight")
    expect(stage).to_have_attribute("data-stop", "school-unlocked")
    page.keyboard.press("ArrowLeft")
    expect(stage).to_have_attribute("data-stop", "first-script")
    for chord in ("Alt+ArrowRight", "Shift+ArrowRight", "Control+ArrowRight"):
        page.keyboard.press(chord)
    settle(page)
    expect(stage).to_have_attribute("data-stop", "first-script")
    page.locator("#route > summary").focus()
    page.keyboard.press("ArrowRight")
    settle(page)
    expect(stage).to_have_attribute("data-stop", "first-script")
    page.locator("#top").evaluate("node => node.scrollIntoView()")
    page.locator("body").evaluate("() => document.activeElement.blur()")
    page.keyboard.press("ArrowLeft")
    settle(page)
    expect(stage).to_have_attribute("data-stop", "title")


@pytest.mark.parametrize("width,height", VIEWPORTS)
@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_layout_fits_without_sideways_scrolling(
    page, live_server, snapshots, width, height, scheme
):
    page.emulate_media(color_scheme=scheme)
    page.set_viewport_size({"width": width, "height": height})
    open_world(page, live_server)
    for section_id in section_ids(snapshots):
        go_to_stop(page, section_id)
        layout = page.evaluate(
            """id => {
              const section = document.getElementById(id);
              const box = node => node.getBoundingClientRect();
              const stage = box(document.getElementById('stage'));
              const overlay = stage.height >= innerHeight - 1;
              return {
                scrollWidth: document.documentElement.scrollWidth,
                heading: box(section.querySelector('h1, h2')),
                lead: box(section.querySelector('.lead')),
                readingTop: overlay ? 0 : stage.bottom,
                fontSize: parseFloat(getComputedStyle(section.querySelector('.lead')).fontSize),
              };
            }""",
            section_id,
        )
        assert layout["scrollWidth"] <= width, section_id
        assert layout["fontSize"] >= 16
        # After a jump the heading is readable at once, clear of the pinned scene.
        assert layout["heading"]["top"] >= layout["readingTop"] - 0.5, section_id
        assert layout["heading"]["bottom"] <= height, section_id
        assert layout["lead"]["left"] >= 0 and layout["lead"]["right"] <= width, section_id
    for control in page.locator(".wordmark, #route > summary").all():
        assert control.bounding_box()["height"] >= 47.999


def test_default_route_is_short_and_links_are_the_reviewed_set(page, live_server, story_document):
    open_world(page, live_server)
    words = page.evaluate("""() => [...document.querySelectorAll('.stop .card > *')]
      .filter(node => !node.matches('.chapter-stats'))
      .reduce((total, node) => total + node.innerText.trim().split(/\\s+/).length, 0)
      - [...document.querySelectorAll('.stop .visually-hidden')]
      .reduce((total, node) => total + node.textContent.trim().split(/\\s+/).length, 0)""")
    print("collapsed words:", words)
    # Collapsed, the whole life is a few minutes of reading; detail is opt-in.
    assert words <= 480, words
    hrefs = set(page.locator("a").evaluate_all("nodes => nodes.map(node => node.href)"))
    external = {href for href in hrefs if not href.startswith(page.url.split("#")[0])}
    expected = {
        "https://www.linkedin.com/in/pranavprem/",
        "https://github.com/pranavprem",
        "mailto:pranavprem93@gmail.com",
        "https://github.com/pranavprem/mediaserver",
        "https://github.com/pranavprem/homeassistant",
        "https://github.com/pranavprem/morpheus",
        "https://github.com/pranavprem/TasKing",
        "https://github.com/pranavprem/Spartanbot",
        "https://github.com/pranavprem/karmamining",
        "https://github.com/forcedotcom/einstein-bot-channel-connector/commits/master/?author=pranavprem",
    }
    for discovery in story_document["discoveries"]:
        expected.update(discovery["links"].values())
    assert external == expected
    assert page.locator("audio, video, iframe, canvas, form, input").count() == 0


def test_no_javascript_keeps_the_complete_linear_story(
    new_context, live_server, story_document, snapshots
):
    page = new_context(java_script_enabled=False).new_page()
    page.goto(live_server + "/")
    assert_linear(page, story_document, snapshots)
    expect(page.locator("#route a")).to_have_count(13)


@pytest.mark.parametrize(
    "resource", ["story.js", "story.css", "art/goa.svg", "art/san-jose-home.svg"]
)
def test_failed_local_resource_never_removes_content(
    page, live_server, story_document, snapshots, resource
):
    page.route(f"**/static/{resource}*", lambda route: route.abort())
    page.goto(live_server + "/")
    if resource in {"story.js", "story.css"}:
        expect(page.locator("html")).not_to_have_class("is-world")
        assert_complete_story(page, story_document, snapshots, visible=resource == "story.js")
    else:
        # Missing art leaves a gap in the strip, never a missing sentence.
        expect(page.locator("html")).to_have_class("is-world")
        assert_complete_story(page, story_document, snapshots, visible=False)


@pytest.mark.parametrize(
    "failure",
    [
        "json",
        "version",
        "boolean-stat",
        "stat-range",
        "position",
        "empty-events",
        "missing-event",
        "extra-event",
        "event-id",
        "region",
        "home-art",
        "home-position",
        "missing-home",
    ],
)
def test_invalid_projection_falls_back(page, live_server, game, story_document, snapshots, failure):
    projection = deepcopy(game)
    if failure == "json":
        projection = "{not json"
    elif failure == "version":
        projection["schema_version"] = 1
    elif failure == "boolean-stat":
        projection["events"][0]["stats_after"]["coding"] = True
    elif failure == "stat-range":
        projection["events"][3]["stats_after"]["vitality"] = 11
    elif failure == "position":
        projection["events"][0]["position"]["x"] = None
    elif failure == "empty-events":
        projection["events"] = []
    elif failure == "missing-event":
        projection["events"].pop()
    elif failure == "extra-event":
        projection["events"].append(deepcopy(projection["events"][-1]))
    elif failure == "event-id":
        projection["events"][4]["id"] = "somewhere-else"
    elif failure == "region":
        projection["events"][2]["region_id"] = "atlantis"
    elif failure == "home-art":
        projection["epilogue_scene"]["art_key"] = "moon-base"
    elif failure == "home-position":
        projection["epilogue_scene"]["positions"] = []
    elif failure == "missing-home":
        del projection["epilogue_scene"]
    serve_with_game(page, live_server, projection)
    assert_linear(page, story_document, snapshots)


@pytest.mark.parametrize("damage", ["stop", "tile", "sheet", "route"])
def test_unexpected_markup_falls_back(page, live_server, story_document, snapshots, damage):
    script = {
        "stop": "document.getElementById('moment-java-unlocked').dataset.stop = 'forged'",
        "tile": "document.querySelector('.tile').dataset.tile = 'forged'",
        "sheet": "document.querySelector('[data-stat=\"charisma\"]').remove()",
        "route": "document.querySelector('#route li').remove()",
    }[damage]
    # Runs after parsing but before the deferred module, like a mismatched deploy.
    page.add_init_script(f"document.addEventListener('readystatechange', () => {{ {script} }});")
    page.goto(live_server + "/")
    expect(page.locator("html")).not_to_have_class("is-world")
    expect(page.locator("#stage")).to_be_hidden()
    expect(page.locator("#beat-college-unlocked-3")).to_be_visible()


def test_stale_stylesheet_restores_full_reading(page, live_server, story_document, snapshots):
    def old_stylesheet(route):
        response = route.fetch()
        source = response.text()
        assert "--ui: world" in source
        route.fulfill(response=response, body=source.replace("--ui: world", "--ui: adventure"))

    page.route("**/static/story.css*", old_stylesheet)
    page.goto(live_server + "/")
    assert_linear(page, story_document, snapshots)


def test_print_shows_the_linear_document_with_extras_open(
    page, live_server, story_document, snapshots
):
    open_world(page, live_server)
    go_to_stop(page, "moment-sjsu-unlocked")
    page.locator("#moment-sjsu-unlocked details.more > summary").click()
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    page.emulate_media(media="print")
    expect(page.locator("#stage")).to_be_hidden()
    expect(page.locator(".topbar")).to_be_hidden()
    assert_complete_story(page, story_document, snapshots, visible=True)
    expect(page.locator(".chapter-stats").first).to_be_visible()
    page.emulate_media(media="screen")
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    # The reader's own open panel survives; everything else closes again.
    expect(page.locator("details[open]")).to_have_count(1)
    expect(page.locator("#moment-sjsu-unlocked details.more")).to_have_attribute("open", "")


def test_csp_privacy_and_bounded_motion(page, live_server, observations, snapshots):
    open_world(page, live_server)
    for section_id in section_ids(snapshots):
        go_to_stop(page, section_id)
    page.locator('.hotspot[data-extra-target="hobbies"]').dispatch_event("click")
    go_to_stop(page, "moment-unexpected-detour")
    # The mosquito is a one-shot flourish, not a loop: it is over within two seconds.
    page.wait_for_timeout(2100)
    encounter_animations = page.evaluate("""() => document.getAnimations()
      .filter(animation => animation.effect.target.closest('.encounter')).length""")
    assert encounter_animations == 0
    idle = page.evaluate("""() => ({
      local: localStorage.length,
      session: sessionStorage.length,
      cookies: document.cookie,
      hash: location.hash,
    })""")
    assert idle == {"local": 0, "session": 0, "cookies": "", "hash": ""}
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
    page.emulate_media(color_scheme=scheme, reduced_motion="reduce")
    page.set_viewport_size({"width": width, "height": 900})
    open_world(page, live_server)
    axe_path = project_root / "node_modules/axe-core/axe.min.js"
    assert axe_path.is_file(), "Run npm ci to install the pinned local axe-core dependency"
    page.evaluate(axe_path.read_text(encoding="utf-8"))
    for state in ("title", "route", "quiet", "extra", "hobbies"):
        if state == "route":
            page.locator("#route > summary").click()
        elif state == "quiet":
            page.keyboard.press("Escape")
            go_to_stop(page, "moment-unexpected-detour")
        elif state == "extra":
            go_to_stop(page, "moment-sjsu-unlocked")
            page.locator('.hotspot[data-extra-target="opportunity-hack"]').dispatch_event("click")
        elif state == "hobbies":
            go_to_stop(page, "epilogue")
            page.locator('.hotspot[data-extra-target="hobbies"]').dispatch_event("click")
        settle(page)
        violations = page.evaluate("""async () => {
          const result = await axe.run(document, {runOnly: {
            type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
          }});
          return result.violations.map(({id, impact, nodes}) => ({id, impact,
            nodes: nodes.map(({target, failureSummary}) => ({target, failureSummary}))}));
        }""")
        assert violations == [], (state, json.dumps(violations, indent=2))


def test_text_enlargement_keeps_everything_reachable(page, live_server, story_document):
    page.set_viewport_size({"width": 320, "height": 700})
    page.add_init_script(
        "document.addEventListener('readystatechange', () => {"
        " document.documentElement.style.fontSize = '200%'; });"
    )
    open_world(page, live_server)
    for card, paragraphs in paragraphs_of(story_document):
        go_to_stop(page, f"moment-{card['id']}")
        section = page.locator(f"#moment-{card['id']}")
        if section.locator("details.more").count():
            section.locator("details.more > summary").click()
        last = section.locator(f"#beat-{card['id']}-{len(paragraphs) - 1}")
        last.scroll_into_view_if_needed()
        expect(last).to_be_in_viewport()
        assert page.evaluate("document.documentElement.scrollWidth") <= 320


def test_forced_colors_keep_the_sheet_and_extras_usable(page, live_server, snapshots):
    page.emulate_media(forced_colors="active")
    open_world(page, live_server)
    go_to_stop(page, "moment-college-unlocked")
    assert_state(page, expected_states(snapshots)[4])
    colours = page.evaluate("""() => {
      const pips = document.querySelectorAll('[data-stat="coding"] .stat-pips i');
      return [getComputedStyle(pips[0]).backgroundColor, getComputedStyle(pips[9]).backgroundColor];
    }""")
    assert colours[0] != colours[1]
    page.locator('.hotspot[data-extra-target="coldplay"]').dispatch_event("click")
    expect(page.locator("#discovery-coldplay summary")).to_be_focused()
