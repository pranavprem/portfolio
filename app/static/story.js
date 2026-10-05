const STAT_KEYS = [
  "coding",
  "enthusiasm",
  "vitality",
  "charisma",
  "experience",
];

const REGIONS = {
  goa: "Goa",
  pune: "Pune",
  "san-jose": "San Jose",
  "bay-area": "San Francisco",
};

const OBJECT_BY_CHAPTER = {
  spawn: "controller",
  school: "backpack",
  detour: "compass",
  college: "laptop",
  "java-forge": "java-mug",
  automation: "automation-gear",
  sjsu: "books",
  "developer-ally": "toolkit",
  "cloud-and-fog": "cloud-terminal",
  "bot-workshop": "bot-console",
  continuing: "agent-nodes",
};

const OBJECT_LABELS = {
  controller: "Controller",
  backpack: "Backpack",
  compass: "Compass",
  laptop: "Laptop",
  "java-mug": "Java mug",
  "automation-gear": "Automation gear",
  books: "Books",
  toolkit: "Toolkit",
  "cloud-terminal": "Cloud terminal",
  "bot-console": "Bot console",
  "agent-nodes": "Agent nodes",
};

const clamp = (value, min, max) => Math.max(min, Math.min(value, max));

// The selected chapter is the save state. Absolute snapshots keep backtracking exact.
export function deriveState(game, eventIndex) {
  const index = clamp(eventIndex, -1, game.events.length - 1);
  const event = index < 0 ? game.initial : game.events[index];
  return {
    index,
    stats: index < 0 ? event.stats : event.stats_after,
    badges: index < 0 ? event.badges : event.badges_after,
    region: event.region_id,
    mood: event.mood,
    object: OBJECT_BY_CHAPTER[event.chapter_id] ?? "controller",
    position: { ...event.position },
  };
}

function validGame(game, markers, badgeIds) {
  if (
    game?.schema_version !== 2 ||
    !game.initial ||
    !Array.isArray(game.events) ||
    game.events.length !== markers.length ||
    !markers.length
  )
    return false;

  const snapshots = [game.initial, ...game.events];
  const orderedBadges = [...badgeIds];
  const validSnapshots = snapshots.every((event, index) => {
    const stats = index === 0 ? event.stats : event.stats_after;
    const badges = index === 0 ? event.badges : event.badges_after;
    const previousExperience =
      index < 2
        ? game.initial.stats.experience
        : snapshots[index - 1].stats_after.experience;
    return (
      stats &&
      Object.keys(stats).length === STAT_KEYS.length &&
      STAT_KEYS.every(
        (key) =>
          Number.isInteger(stats[key]) && stats[key] >= 0 && stats[key] <= 10,
      ) &&
      (index === 0 || stats.experience >= previousExperience) &&
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
      badges.every((id, badgeIndex) => id === orderedBadges[badgeIndex]) &&
      (index < 2 || badges.length >= snapshots[index - 1].badges_after.length)
    );
  });

  return (
    validSnapshots &&
    game.initial.badges.length === 0 &&
    game.events.every((event) =>
      Object.hasOwn(OBJECT_BY_CHAPTER, event.chapter_id),
    ) &&
    new Set(game.events.map((event) => event.id)).size === markers.length &&
    game.events.every(
      (event, index) =>
        event.id === markers[index].dataset.checkpoint &&
        event.chapter_id === markers[index].closest(".chapter").id,
    )
  );
}

function startJourney(root) {
  const html = document.documentElement;
  const gameShell = root.querySelector(".game-shell");
  const screens = [...root.querySelectorAll(".game-screen")];
  const chapters = [...root.querySelectorAll(".chapter")];
  const fallbackOnly = [
    ...root.querySelectorAll(
      ".chapter-header, .fallback-landscape, .chapter-stats",
    ),
  ];
  const markers = [...root.querySelectorAll("[data-checkpoint]")];
  const statRows = [...root.querySelectorAll("[data-stat]")];
  const badgeSlots = [...root.querySelectorAll("[data-badge]")];
  const art = [...root.querySelectorAll("[data-region-art]")];
  const objectSprites = [...root.querySelectorAll("[data-object-sprite]")];
  const status = document.getElementById("sheet-status");
  const statsPanel = document.getElementById("character-sheet");
  const questLog = document.getElementById("bonus");
  const statsButton = root.querySelector('[data-action="toggle-stats"]');
  const questsButton = root.querySelector('[data-action="toggle-quests"]');
  const inspectButton = root.querySelector('[data-action="inspect"]');
  const backButton = root.querySelector('[data-action="back"]');
  const advanceLabel = document.getElementById("advance-label");
  const beatProgress = document.getElementById("beat-progress");
  const chapterProgress = document.getElementById("chapter-progress-fill");
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const beatIndexes = screens.map(() => 0);
  let game;
  let screenIndex = 0;
  let lastEventIndex = null;
  let touchStart = null;
  let focusedHeading = null;

  function eventIndexForScreen() {
    if (screenIndex === 0) return -1;
    return Math.min(screenIndex - 1, game.events.length - 1);
  }

  function currentScreen() {
    return screens[screenIndex];
  }

  function currentBeats() {
    return [...currentScreen().querySelectorAll(".dialogue-beat")];
  }

  function closePanels(returnFocus = false) {
    const activeToggle = questLog.classList.contains("is-open")
      ? questsButton
      : statsPanel.classList.contains("is-open")
        ? statsButton
        : null;
    statsPanel.classList.remove("is-open");
    questLog.classList.remove("is-open");
    statsPanel.setAttribute("aria-hidden", "true");
    questLog.setAttribute("aria-hidden", "true");
    statsPanel.inert = true;
    questLog.inert = true;
    statsButton.setAttribute("aria-expanded", "false");
    questsButton.setAttribute("aria-expanded", "false");
    gameShell.inert = false;
    if (returnFocus) activeToggle?.focus();
  }

  function openPanel(panel, button) {
    closePanels();
    panel.classList.add("is-open");
    panel.removeAttribute("aria-hidden");
    panel.inert = false;
    button.setAttribute("aria-expanded", "true");
    if (panel === questLog) gameShell.inert = true;
    panel.querySelector(".panel-close")?.focus();
  }

  function renderState(state) {
    if (state.index !== lastEventIndex) {
      statRows.forEach((row) => {
        const value = state.stats[row.dataset.stat];
        row.querySelector(".stat-value").textContent = value;
        row
          .querySelectorAll(".stat-pips > span")
          .forEach((pip, index) =>
            pip.classList.toggle("filled", index < value),
          );
      });
      badgeSlots.forEach((slot) => {
        const earned = state.badges.includes(slot.dataset.badge);
        slot.classList.toggle("earned", earned);
        if (earned) {
          slot.removeAttribute("aria-hidden");
          slot.setAttribute("aria-label", slot.dataset.badgeLabel);
        } else {
          slot.setAttribute("aria-hidden", "true");
          slot.removeAttribute("aria-label");
        }
      });
      document.getElementById("badge-count").textContent = String(
        state.badges.length,
      ).padStart(2, "0");
      art.forEach((image) =>
        image.classList.toggle(
          "current",
          image.dataset.regionArt === state.region,
        ),
      );
      objectSprites.forEach((object) =>
        object.classList.toggle(
          "current",
          object.dataset.objectSprite === state.object,
        ),
      );
      document.getElementById("world-label").textContent =
        REGIONS[state.region];
      document.getElementById("scene-object-label").textContent =
        OBJECT_LABELS[state.object];
      document.getElementById("overworld").dataset.mood = state.mood;
      root.dataset.checkpointIndex = state.index;
      lastEventIndex = state.index;
    }
    document
      .getElementById("journey-object-track")
      .setAttribute(
        "transform",
        `translate(${state.position.x} ${state.position.y})`,
      );
  }

  function render() {
    const screen = currentScreen();
    const beats = currentBeats();
    const beatIndex = clamp(beatIndexes[screenIndex], 0, beats.length - 1);
    beatIndexes[screenIndex] = beatIndex;
    const eventIndex = eventIndexForScreen();

    screens.forEach((candidate, index) => {
      const current = index === screenIndex;
      candidate.classList.toggle("is-current-screen", current);
      candidate.setAttribute("aria-hidden", String(!current));
    });
    chapters.forEach((chapter) => {
      const current = chapter.contains(screen);
      chapter.classList.toggle("is-current-chapter", current);
      chapter.setAttribute("aria-hidden", String(!current));
    });
    beats.forEach((beat, index) =>
      beat.classList.toggle("is-current-beat", index === beatIndex),
    );

    const finalBeat = beatIndex === beats.length - 1;
    screen.classList.toggle("is-reward-visible", finalBeat);
    document
      .getElementById("journey-marker")
      .classList.toggle(
        "is-celebrating",
        finalBeat &&
          screen.dataset.screenKind === "chapter" &&
          !reducedMotion.matches,
      );

    renderState(deriveState(game, eventIndex));
    const chapter = screen.closest(".chapter");
    status.textContent = chapter
      ? `Chapter ${chapter.dataset.chapterNumber} / 11 - ${REGIONS[chapter.dataset.region]}`
      : screen.dataset.screenKind === "ending"
        ? "Epilogue - San Jose"
        : "Title screen";
    chapterProgress.style.width = `${(screenIndex / (screens.length - 1)) * 100}%`;
    root.dataset.screenIndex = screenIndex;
    root.dataset.beatIndex = beatIndex;
    beatProgress.textContent =
      beats.length > 1
        ? `Dialogue ${beatIndex + 1} / ${beats.length}`
        : status.textContent;
    backButton.disabled = screenIndex === 0 && beatIndex === 0;
    inspectButton.hidden = screen.dataset.screenKind !== "chapter";
    inspectButton.setAttribute(
      "aria-expanded",
      String(screen.classList.contains("is-inspecting")),
    );

    if (screen.classList.contains("is-inspecting")) {
      advanceLabel.textContent = "Return to story";
    } else if (screenIndex === 0) {
      advanceLabel.textContent = "Start game";
    } else if (!finalBeat) {
      advanceLabel.textContent = "Continue";
    } else if (screen.dataset.screenKind === "ending") {
      advanceLabel.textContent = "Open quest log";
    } else {
      advanceLabel.textContent = "Travel onward";
    }
  }

  function moveToScreen(nextIndex, direction = 1) {
    const previousScreen = currentScreen();
    previousScreen.classList.remove("is-inspecting");
    screenIndex = clamp(nextIndex, 0, screens.length - 1);
    const beats = [...screens[screenIndex].querySelectorAll(".dialogue-beat")];
    beatIndexes[screenIndex] =
      direction < 0 ? Math.max(0, beats.length - 1) : 0;
    lastEventIndex = null;
    render();
    focusedHeading?.removeAttribute("tabindex");
    focusedHeading = currentScreen().querySelector("h1, h2, h3");
    focusedHeading?.setAttribute("tabindex", "-1");
    focusedHeading?.focus({ preventScroll: true });
  }

  function advance() {
    const screen = currentScreen();
    if (screen.classList.contains("is-inspecting")) {
      screen.classList.remove("is-inspecting");
      render();
      return;
    }
    const beats = currentBeats();
    if (beatIndexes[screenIndex] < beats.length - 1) {
      beatIndexes[screenIndex] += 1;
      render();
      return;
    }
    if (screenIndex < screens.length - 1) moveToScreen(screenIndex + 1);
    else openPanel(questLog, questsButton);
  }

  function back() {
    const screen = currentScreen();
    if (screen.classList.contains("is-inspecting")) {
      screen.classList.remove("is-inspecting");
      render();
      return;
    }
    if (beatIndexes[screenIndex] > 0) {
      beatIndexes[screenIndex] -= 1;
      render();
      return;
    }
    if (screenIndex > 0) moveToScreen(screenIndex - 1, -1);
  }

  function fallback() {
    closePanels();
    html.classList.remove("enhanced");
    screens.forEach((screen) => {
      screen.classList.remove(
        "is-current-screen",
        "is-inspecting",
        "is-reward-visible",
      );
      screen.removeAttribute("aria-hidden");
    });
    root
      .querySelectorAll(".chapter")
      .forEach((chapter) => chapter.classList.remove("is-current-chapter"));
    chapters.forEach((chapter) => chapter.removeAttribute("aria-hidden"));
    fallbackOnly.forEach((node) => node.removeAttribute("aria-hidden"));
    statsPanel.inert = false;
    questLog.inert = false;
    status.textContent = "Opening stats. The complete story follows.";
  }

  try {
    game = JSON.parse(root.dataset.game);
    if (
      screens.length !== markers.length + 2 ||
      statRows.length !== STAT_KEYS.length ||
      statRows.some((row, index) => row.dataset.stat !== STAT_KEYS[index]) ||
      !validGame(
        game,
        markers,
        new Set(badgeSlots.map((slot) => slot.dataset.badge)),
      )
    )
      throw new Error("Invalid story projection");

    html.classList.add("enhanced");
    fallbackOnly.forEach((node) => node.setAttribute("aria-hidden", "true"));
    statsPanel.setAttribute("aria-hidden", "true");
    questLog.setAttribute("aria-hidden", "true");
    statsPanel.inert = true;
    questLog.inert = true;
    render();

    root.addEventListener("click", (event) => {
      const action = event.target.closest("[data-action]")?.dataset.action;
      if (!action) return;
      if (action === "advance") advance();
      else if (action === "back") back();
      else if (action === "inspect") {
        currentScreen().classList.toggle("is-inspecting");
        render();
      } else if (action === "toggle-stats") {
        if (statsPanel.classList.contains("is-open")) closePanels(true);
        else openPanel(statsPanel, statsButton);
      } else if (action === "toggle-quests") {
        if (questLog.classList.contains("is-open")) closePanels(true);
        else openPanel(questLog, questsButton);
      } else if (action === "close-panels") closePanels(true);
    });

    document.addEventListener("keydown", (event) => {
      if (event.defaultPrevented || event.isComposing) return;
      if (event.key === "Escape") {
        closePanels(true);
        return;
      }
      if (
        event.altKey ||
        event.ctrlKey ||
        event.metaKey ||
        event.shiftKey ||
        (typeof event.target?.closest === "function" &&
          event.target.closest(
            "a, button, input, textarea, select, [contenteditable]",
          ))
      )
        return;
      if (["ArrowRight", "Enter", " "].includes(event.key)) {
        event.preventDefault();
        advance();
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        back();
      }
    });

    gameShell.addEventListener(
      "pointerdown",
      (event) => {
        if (event.pointerType === "touch")
          touchStart = { x: event.clientX, y: event.clientY };
      },
      { passive: true },
    );
    gameShell.addEventListener(
      "pointerup",
      (event) => {
        if (!touchStart || event.pointerType !== "touch") return;
        const x = event.clientX - touchStart.x;
        const y = event.clientY - touchStart.y;
        touchStart = null;
        if (Math.abs(x) < 52 || Math.abs(y) > Math.abs(x) * 0.75) return;
        if (x < 0) advance();
        else back();
      },
      { passive: true },
    );
    reducedMotion.addEventListener("change", render);
    window.addEventListener("pageshow", render);
  } catch {
    fallback();
  }
}

const journey = document.getElementById("journey");
if (journey) startJourney(journey);
