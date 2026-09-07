const STAT_KEYS = [
  "coding",
  "enthusiasm",
  "vitality",
  "charisma",
  "automancy",
  "sidequests",
];
const REGIONS = {
  goa: [
    "WORLD 01 / GOA",
    "The starter town",
    "Salt air. Small programs. Big possibilities.",
    "15.3 N\n74.1 E",
  ],
  pune: [
    "WORLD 02 / PUNE",
    "The Java forge",
    "New language acquired. Main quest reconsidered.",
    "18.5 N\n73.9 E",
  ],
  "san-jose": [
    "WORLD 03 / SAN JOSE",
    "The learning grounds",
    "Hard mode, finally. And the right kind of party.",
    "37.3 N\n121.9 W",
  ],
  "bay-area": [
    "WORLD 04 / BAY AREA",
    "The helper workshop",
    "Build the tools. Help the humans. Repeat.",
    "37.8 N\n122.4 W",
  ],
};
const clamp = (value, min, max) => Math.max(min, Math.min(value, max));

// Absolute snapshots make a rewind, a scrollbar jump, and normal travel identical.
export function deriveState(
  game,
  anchors,
  readingPosition,
  reducedMotion = false,
) {
  let index = -1;
  for (let i = 0; i < anchors.length; i += 1) {
    if (anchors[i] > readingPosition) break;
    index = i;
  }
  const event = index < 0 ? game.initial : game.events[index];
  const next = game.events[index + 1];
  let position = { ...event.position };
  let frame = 0;
  if (!reducedMotion && index >= 0 && next?.region_id === event.region_id) {
    const fraction = clamp(
      (readingPosition - anchors[index]) /
        (anchors[index + 1] - anchors[index]),
      0,
      1,
    );
    position = {
      x: Math.round(
        event.position.x + (next.position.x - event.position.x) * fraction,
      ),
      y: Math.round(
        event.position.y + (next.position.y - event.position.y) * fraction,
      ),
    };
    frame = Math.floor(fraction * 12) % 4;
  }
  return {
    index,
    stats: index < 0 ? event.stats : event.stats_after,
    badges: index < 0 ? event.badges : event.badges_after,
    region: event.region_id,
    mood: event.mood,
    position,
    frame,
  };
}

function validGame(game, markers, badgeIds) {
  if (
    game?.schema_version !== 1 ||
    !game.initial ||
    !Array.isArray(game.events) ||
    game.events.length !== markers.length ||
    !markers.length
  )
    return false;
  const snapshots = [game.initial, ...game.events];
  const validSnapshots = snapshots.every((event, i) => {
    const stats = i === 0 ? event.stats : event.stats_after;
    const badges = i === 0 ? event.badges : event.badges_after;
    return (
      stats &&
      Object.keys(stats).length === STAT_KEYS.length &&
      STAT_KEYS.every(
        (key) =>
          Number.isInteger(stats[key]) && stats[key] >= 0 && stats[key] <= 10,
      ) &&
      Object.hasOwn(REGIONS, event.region_id) &&
      ["bright", "quiet", "fog"].includes(event.mood) &&
      Number.isFinite(event.position?.x) &&
      event.position.x >= 20 &&
      event.position.x <= 300 &&
      Number.isFinite(event.position?.y) &&
      event.position.y >= 0 &&
      event.position.y <= 180 &&
      Array.isArray(badges) &&
      new Set(badges).size === badges.length &&
      badges.every((id) => badgeIds.has(id))
    );
  });
  return (
    validSnapshots &&
    game.initial.badges.length === 0 &&
    new Set(game.events.map((event) => event.id)).size === markers.length &&
    game.events.every(
      (event, i) =>
        event.id === markers[i].dataset.checkpoint &&
        event.chapter_id === markers[i].closest(".chapter").id,
    )
  );
}

function startJourney(root) {
  const html = document.documentElement;
  const hud = document.getElementById("character-sheet");
  const status = document.getElementById("sheet-status");
  const markers = [...root.querySelectorAll("[data-checkpoint]")];
  const statRows = [...hud.querySelectorAll("[data-stat]")];
  const badgeSlots = [...hud.querySelectorAll("[data-badge]")];
  const routes = [...root.querySelectorAll("[data-route]")];
  const art = [...root.querySelectorAll("[data-region-art]")];
  const badgeNames = [...root.querySelectorAll(".inventory-ledger dt")].map(
    (node) => node.textContent.trim(),
  );
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const mobile = matchMedia("(max-width: 1023px)");
  let game;
  let anchors = [];
  let readingOffset = 0;
  let maxScroll = 0;
  let geometryDirty = true;
  let lastIndex = null;
  let frameRequest = 0;
  let failed = false;

  function render(state, live = true) {
    if (state.index !== lastIndex) {
      statRows.forEach((row) => {
        const value = state.stats[row.dataset.stat];
        row.querySelector(".stat-value").textContent = value;
        row
          .querySelectorAll(".stat-pips > span")
          .forEach((pip, i) => pip.classList.toggle("filled", i < value));
      });
      badgeSlots.forEach((slot, i) => {
        const earned = state.badges.includes(slot.dataset.badge);
        slot.classList.toggle("earned", earned);
        if (earned) {
          slot.removeAttribute("aria-hidden");
          slot.setAttribute("aria-label", badgeNames[i]);
        } else {
          slot.setAttribute("aria-hidden", "true");
          slot.removeAttribute("aria-label");
        }
      });
      document.getElementById("badge-count").textContent = String(
        state.badges.length,
      ).padStart(2, "0");
      const chapter =
        state.index < 0
          ? 0
          : Number(
              markers[state.index].closest(".chapter").dataset.chapterNumber,
            );
      document.getElementById("player-level").textContent =
        `LV. ${String(chapter + 1).padStart(2, "0")}`;
      status.textContent = live
        ? `CHAPTER ${String(chapter).padStart(2, "0")} / 11 / SCROLL TO EXPLORE`
        : "Opening stats; chapter snapshots follow.";
      markers.forEach((marker, i) =>
        marker.classList.toggle("is-current", live && i === state.index),
      );
      art.forEach((image) =>
        image.classList.toggle(
          "current",
          image.dataset.regionArt === state.region,
        ),
      );
      routes.forEach((route, i) => {
        route.classList.toggle(
          "visited",
          i < Object.keys(REGIONS).indexOf(state.region),
        );
        if (route.dataset.route === state.region)
          route.setAttribute("aria-current", "location");
        else route.removeAttribute("aria-current");
      });
      [
        "world-label",
        "scene-place",
        "scene-description",
        "scene-coordinates",
      ].forEach((id, i) => {
        document.getElementById(id).textContent = REGIONS[state.region][i];
      });
      document.getElementById("overworld").dataset.mood = state.mood;
      root.dataset.checkpointIndex = state.index;
      lastIndex = state.index;
    }
    document
      .getElementById("travelers")
      .setAttribute(
        "transform",
        `translate(${state.position.x} ${state.position.y})`,
      );
    document.getElementById("traveler").dataset.frame = state.frame;
  }

  function measure() {
    const height = html.clientHeight;
    html.dataset.theaterFlow = String(
      !mobile.matches &&
        hud.closest(".theater").getBoundingClientRect().height + 24 > height,
    );
    html.dataset.hudDocked = String(mobile.matches);
    let hudBottom = 0;
    if (mobile.matches) {
      const box = hud.getBoundingClientRect();
      // Readability takes priority over a fixed sheet on short or heavily zoomed screens.
      if (box.bottom > height * 0.25) html.dataset.hudDocked = "false";
      else hudBottom = box.bottom;
    }
    html.style.setProperty("--hud-height", `${Math.ceil(hudBottom)}px`);
    const top = hudBottom ? hudBottom + 12 : 16;
    readingOffset = top + 0.35 * (height - top);
    anchors = markers.map(
      (marker) => marker.getBoundingClientRect().top + window.scrollY,
    );
    maxScroll = Math.max(0, document.scrollingElement.scrollHeight - height);
    if (
      anchors.some(
        (position, i) =>
          !Number.isFinite(position) || (i > 0 && position <= anchors[i - 1]),
      )
    )
      throw new Error("Invalid checkpoint geometry");
    geometryDirty = false;
  }

  function fallback() {
    failed = true;
    cancelAnimationFrame(frameRequest);
    html.classList.remove("enhanced");
    html.removeAttribute("data-hud-docked");
    html.removeAttribute("data-theater-flow");
    html.style.removeProperty("--hud-height");
    lastIndex = null;
    if (game?.initial) {
      try {
        render(deriveState(game, [], 0, true), false);
      } catch {
        hud.hidden = true;
      }
    }
    status.textContent = "Storybook mode; chapter snapshots follow.";
  }

  function update() {
    frameRequest = 0;
    if (failed) return;
    try {
      if (geometryDirty) measure();
      const readingPosition =
        clamp(window.scrollY, 0, maxScroll) + readingOffset;
      render(
        deriveState(game, anchors, readingPosition, reducedMotion.matches),
      );
    } catch {
      fallback();
    }
  }

  function schedule(remeasure = false) {
    if (failed) return;
    geometryDirty ||= remeasure;
    if (!frameRequest) frameRequest = requestAnimationFrame(update);
  }

  try {
    game = JSON.parse(root.dataset.game);
    if (
      !validGame(
        game,
        markers,
        new Set(badgeSlots.map((slot) => slot.dataset.badge)),
      )
    )
      throw new Error("Invalid story projection");
    html.classList.add("enhanced");
    measure();
    update();
    document.addEventListener("scroll", () => schedule(), { passive: true });
    window.addEventListener("resize", () => schedule(true), { passive: true });
    window.visualViewport?.addEventListener("resize", () => schedule(true), {
      passive: true,
    });
    window.addEventListener("pageshow", () => schedule(true));
    window.addEventListener("load", () => schedule(true));
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) schedule(true);
    });
    reducedMotion.addEventListener("change", () => schedule());
    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(() => schedule(true));
      observer.observe(root.querySelector(".story-track"));
      observer.observe(hud);
    }
    document.fonts?.ready.then(() => schedule(true));
  } catch {
    fallback();
  }
}

const journey = document.getElementById("journey");
if (journey) startJourney(journey);
