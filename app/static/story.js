// Progressive enhancement only: the server HTML is already the complete story.
// This module turns it into one scrolling world, and backs out (leaving the
// linear document) whenever the page or its data is not what it expects.

const TILE_WIDTH = 320;
const TILE_HEIGHT = 180;
// Scenes are separate places, so they sit apart like frames on a film strip.
const TILE_GAP = 8;
const MARKER_HALF_WIDTH = 16;
// Scene units kept between an extra's window and the edge of the view.
const EDGE_MARGIN = 12;
const TILE_IDS = ["goa", "pune", "san-jose", "bay-area", "san-jose-home"];
const STAT_KEYS = [
  "coding",
  "enthusiasm",
  "vitality",
  "charisma",
  "experience",
];
// Share of each stop spent walking to the next one; the rest holds still to read.
const TRAVEL_SHARE = 0.45;

const isPoint = (value) =>
  value !== null &&
  typeof value === "object" &&
  Number.isFinite(value.x) &&
  Number.isFinite(value.y);

const isStats = (value) =>
  value !== null &&
  typeof value === "object" &&
  STAT_KEYS.every(
    (key) =>
      Number.isInteger(value[key]) && value[key] >= 0 && value[key] <= 10,
  );

/** Reject projection data this script was not written for. */
export function isValidGame(game) {
  return (
    game !== null &&
    typeof game === "object" &&
    game.schema_version === 2 &&
    game.initial !== null &&
    typeof game.initial === "object" &&
    isStats(game.initial.stats) &&
    isPoint(game.initial.position) &&
    TILE_IDS.includes(game.initial.region_id) &&
    Array.isArray(game.events) &&
    game.events.length > 0 &&
    game.events.every(
      (event) =>
        event !== null &&
        typeof event === "object" &&
        typeof event.id === "string" &&
        typeof event.chapter_id === "string" &&
        isStats(event.stats_after) &&
        isPoint(event.position) &&
        TILE_IDS.includes(event.region_id) &&
        typeof event.mood === "string",
    ) &&
    game.epilogue_scene !== null &&
    typeof game.epilogue_scene === "object" &&
    TILE_IDS.includes(game.epilogue_scene.art_key) &&
    Array.isArray(game.epilogue_scene.positions) &&
    game.epilogue_scene.positions.length > 0 &&
    game.epilogue_scene.positions.every(isPoint)
  );
}

/** World x of a scene-local x: scenes sit side by side in story order. */
export function worldX(tileId, x) {
  return TILE_IDS.indexOf(tileId) * (TILE_WIDTH + TILE_GAP) + x;
}

/**
 * Absolute state for a stop: 0 is the title, 1..n the authored events, n+1 the
 * ending. Stats are snapshots, never sums, so any jump lands on the same values.
 */
export function deriveStop(game, stopIndex) {
  const last = game.events.length + 1;
  const index = Math.min(Math.max(Math.trunc(stopIndex) || 0, 0), last);
  if (index === 0) {
    const { stats, region_id: tile, position, mood } = game.initial;
    return {
      id: "title",
      tile,
      stats,
      mood,
      chapter: 0,
      x: worldX(tile, position.x),
      y: position.y,
    };
  }
  const chapters = [...new Set(game.events.map((event) => event.chapter_id))];
  if (index === last) {
    const final = game.events.at(-1);
    const tile = game.epilogue_scene.art_key;
    const position = game.epilogue_scene.positions[0];
    return {
      id: "epilogue",
      tile,
      stats: final.stats_after,
      mood: final.mood,
      chapter: chapters.length - 1,
      x: worldX(tile, position.x),
      y: position.y,
    };
  }
  const event = game.events[index - 1];
  return {
    id: event.id,
    tile: event.region_id,
    stats: event.stats_after,
    mood: event.mood,
    chapter: chapters.indexOf(event.chapter_id),
    x: worldX(event.region_id, event.position.x),
    y: event.position.y,
  };
}

/** Which stop is being read at a scroll position, and how far the walk to the next has gone. */
export function locate(tops, end, line) {
  let index = 0;
  while (index < tops.length - 1 && tops[index + 1] <= line) index += 1;
  if (index === tops.length - 1) return { index, travel: 0 };
  const top = tops[index];
  const bottom = Math.min(tops[index + 1], end);
  const walk = Math.max((bottom - top) * TRAVEL_SHARE, 1);
  const raw = Math.min(Math.max((line - (bottom - walk)) / walk, 0), 1);
  // Smoothstep: ease out of one stop and into the next.
  return { index, travel: raw * raw * (3 - 2 * raw) };
}

function readGame(journey) {
  try {
    const game = JSON.parse(journey.dataset.game);
    return isValidGame(game) ? game : null;
  } catch {
    return null;
  }
}

function start() {
  const root = document.documentElement;
  const journey = document.getElementById("journey");
  const stage = document.getElementById("stage");
  const world = document.getElementById("world");
  const marker = document.getElementById("marker");
  const place = document.getElementById("place");
  const route = document.getElementById("route");
  const routeCount = document.getElementById("route-count");
  if (
    !journey ||
    !stage ||
    !world ||
    !marker ||
    !place ||
    !route ||
    !routeCount
  )
    return;
  // A stale or missing stylesheet cannot lay out the world; stay linear.
  if (window.getComputedStyle(root).getPropertyValue("--ui").trim() !== "world")
    return;

  const game = readGame(journey);
  if (!game) return;
  const sections = [...journey.querySelectorAll("[data-stop]")];
  const stops = sections.map((_, index) => deriveStop(game, index));
  if (
    sections.length !== game.events.length + 2 ||
    sections.some((section, index) => section.dataset.stop !== stops[index].id)
  ) {
    return;
  }

  const viewport = stage.querySelector(".viewport");
  const tiles = [...world.querySelectorAll(".tile")];
  const sprites = [...marker.querySelectorAll(".object-sprite")];
  const statRows = STAT_KEYS.map((key) =>
    stage.querySelector(`[data-stat="${key}"]`),
  );
  const routeLinks = [...route.querySelectorAll("a")];
  const hotspots = [...world.querySelectorAll(".hotspot")];
  const encounters = [...world.querySelectorAll(".encounter")];
  if (
    !viewport ||
    tiles.length !== TILE_IDS.length ||
    tiles.some((tile, index) => tile.dataset.tile !== TILE_IDS[index]) ||
    sprites.length === 0 ||
    statRows.some((row) => !row) ||
    routeLinks.length !== sections.length - 1
  ) {
    return;
  }

  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const labels = Object.fromEntries(
    sections.map((section, index) => [
      stops[index].tile,
      section.querySelector(".postcard figcaption")?.textContent ??
        place.textContent,
    ]),
  );
  labels[stops[0].tile] = place.textContent;

  let unit = 1;
  // Left edge of the visible scene at each stop, in scene units.
  let cameras = stops.map(() => 0);
  let overlay = false;
  let tops = [];
  let end = 0;
  let active = -1;
  let frame = 0;

  // Hotspots and encounters live in world coordinates so they travel with the scene.
  const placeInWorld = (element, x, y) => {
    element.style.transform = `translate3d(${Math.round(x * unit)}px, ${Math.round(y * unit)}px, 0)`;
  };

  function measure() {
    // Round up to whole tile pixels so neighbouring scenes never show a seam.
    unit =
      Math.ceil((viewport.clientHeight / TILE_HEIGHT) * TILE_WIDTH) /
      TILE_WIDTH;
    stage.style.setProperty("--u", `${unit}px`);
    const offset = window.scrollY;
    tops = sections.map(
      (section) => section.getBoundingClientRect().top + offset,
    );
    end = sections.at(-1).getBoundingClientRect().bottom + offset;
    const spans = stops.map((stop) => [stop.x, stop.x]);
    for (const hotspot of hotspots) {
      const screen = Number(hotspot.dataset.screen);
      const stop = stops[screen];
      const x = Number(hotspot.dataset.x);
      const y = Number(hotspot.dataset.y);
      if (stop && Number.isFinite(x) && Number.isFinite(y)) {
        const sceneX = worldX(stop.tile, x);
        placeInWorld(hotspot, sceneX, y);
        spans[screen] = [
          Math.min(spans[screen][0], sceneX),
          Math.max(spans[screen][1], sceneX),
        ];
      }
    }
    // Wide layout: the stage is the whole window, so frame the scene in the
    // space the placard leaves free rather than behind it.
    overlay = stage.clientHeight >= window.innerHeight - 1;
    const width = viewport.clientWidth;
    const visible = width / unit;
    const card = sections[0].querySelector(".card");
    const cardRight = overlay && card ? card.getBoundingClientRect().right : 0;
    const focus = width > 0 ? (cardRight + width) / 2 / width : 0.5;
    const total = worldX(TILE_IDS.at(-1), TILE_WIDTH);
    const clamp = (value, low, high) => Math.min(Math.max(value, low), high);
    cameras = spans.map(([left, right], index) => {
      let camera = (left + right) / 2 - visible * focus;
      // Keep every extra on screen when the scene is wide enough to hold them.
      if (right - left + 2 * EDGE_MARGIN <= visible) {
        camera = clamp(
          camera,
          right + EDGE_MARGIN - visible,
          left - EDGE_MARGIN,
        );
      }
      // The traveller outranks the extras: it is never framed off the scene.
      const reach = MARKER_HALF_WIDTH + 1;
      camera = clamp(
        camera,
        stops[index].x + reach - visible,
        stops[index].x - reach,
      );
      return clamp(camera, 0, Math.max(total - visible, 0));
    });
    for (const encounter of encounters) {
      placeInWorld(
        encounter,
        worldX(encounter.dataset.tile, Number(encounter.dataset.x)),
        Number(encounter.dataset.y),
      );
    }
  }

  function activate(index) {
    active = index;
    const stop = stops[index];
    const before = index > 0 ? stops[index - 1].stats : null;
    stage.dataset.stop = stop.id;
    stage.dataset.mood = stop.mood;
    place.textContent = labels[stop.tile] ?? "";
    routeCount.textContent =
      index === 0 ? "" : `${index} / ${stops.length - 1}`;
    sprites.forEach((sprite, spriteIndex) => {
      sprite.classList.toggle(
        "current",
        spriteIndex === Math.min(stop.chapter, sprites.length - 1),
      );
    });
    STAT_KEYS.forEach((key, row) => {
      const value = stop.stats[key];
      const change = before ? value - before[key] : 0;
      const delta = statRows[row].querySelector(".stat-delta");
      statRows[row].querySelector(".stat-value").textContent = String(value);
      statRows[row]
        .querySelectorAll(".stat-pips i")
        .forEach((pip, pipIndex) => {
          pip.classList.toggle("on", pipIndex < value);
        });
      // The arrow carries direction so the change never depends on colour alone.
      delta.textContent =
        change > 0 ? `▲${change}` : change < 0 ? `▼${-change}` : "";
      delta.classList.toggle("up", change > 0);
      delta.classList.toggle("down", change < 0);
    });
    routeLinks.forEach((link, linkIndex) => {
      if (linkIndex === index - 1) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
    for (const hotspot of hotspots) {
      hotspot.hidden = Number(hotspot.dataset.screen) !== index;
    }
  }

  function render() {
    frame = 0;
    const readingTop = overlay ? 0 : stage.clientHeight;
    const line =
      window.scrollY + readingTop + (window.innerHeight - readingTop) * 0.5;
    const { index, travel } = locate(tops, end, line);
    if (index !== active) activate(index);

    const from = stops[index];
    const to = stops[Math.min(index + 1, stops.length - 1)];
    const progress = reducedMotion.matches ? 0 : travel;
    const x = from.x + (to.x - from.x) * progress;
    const y = from.y + (to.y - from.y) * progress;
    const nextIndex = Math.min(index + 1, stops.length - 1);
    const camera =
      cameras[index] + (cameras[nextIndex] - cameras[index]) * progress;
    world.style.transform = `translate3d(${-Math.round(camera * unit)}px, 0, 0)`;
    placeInWorld(marker, x, y);
  }

  const schedule = () => {
    if (!frame) frame = requestAnimationFrame(render);
  };

  function goTo(index) {
    const target = sections[Math.min(Math.max(index, 0), sections.length - 1)];
    target.scrollIntoView({
      behavior: reducedMotion.matches ? "auto" : "smooth",
      block: "start",
    });
  }

  function openExtra(hotspot) {
    const extra = document.getElementById(
      hotspot.getAttribute("aria-controls"),
    );
    if (!extra || !journey.contains(extra) || !extra.matches("details.extra"))
      return;
    const more = extra.closest("details.more");
    if (more) more.open = true;
    extra.open = true;
    extra.querySelector("summary")?.focus({ preventScroll: true });
    // Opening changes the layout; scroll once it has settled or the browser drops the request.
    requestAnimationFrame(() => {
      extra.scrollIntoView({
        behavior: reducedMotion.matches ? "auto" : "smooth",
        block: "nearest",
      });
    });
  }

  const details = [...journey.querySelectorAll("details")];
  for (const element of details) element.open = false;
  for (const hint of journey.querySelectorAll(".scroll-hint"))
    hint.hidden = false;
  root.classList.add("is-world");

  for (const hotspot of hotspots) {
    hotspot.addEventListener("click", () => openExtra(hotspot));
    const extra = document.getElementById(
      hotspot.getAttribute("aria-controls"),
    );
    extra?.addEventListener("toggle", () => {
      hotspot.setAttribute("aria-expanded", String(extra.open));
    });
  }

  route.addEventListener("click", (event) => {
    if (event.target.closest("a")) route.open = false;
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && route.open) {
      route.open = false;
      route.querySelector("summary").focus();
      return;
    }
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey)
      return;
    if (
      event.target.closest?.(
        "a, button, summary, input, textarea, select, [contenteditable]",
      )
    ) {
      return;
    }
    if (event.key === "ArrowRight") goTo(active + 1);
    else if (event.key === "ArrowLeft") goTo(active - 1);
    else return;
    event.preventDefault();
  });

  // Closed extras do not print; open them for paper and restore the reader's state after.
  let openBeforePrint = [];
  window.addEventListener("beforeprint", () => {
    openBeforePrint = details.map((element) => element.open);
    for (const element of details) element.open = true;
  });
  window.addEventListener("afterprint", () => {
    details.forEach((element, index) => {
      element.open = openBeforePrint[index] ?? false;
    });
  });

  const remeasure = () => {
    measure();
    schedule();
  };
  new ResizeObserver(remeasure).observe(journey);
  window.addEventListener("resize", remeasure);
  window.addEventListener("scroll", schedule, { passive: true });
  reducedMotion.addEventListener("change", schedule);
  measure();
  render();
}

if (typeof document !== "undefined") start();
