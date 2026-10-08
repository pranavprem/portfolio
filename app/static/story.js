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
    game.epilogue_scene?.region_id !== "san-jose" ||
    game.epilogue_scene?.art_key !== "san-jose-home" ||
    !Array.isArray(game.epilogue_scene?.positions) ||
    game.epilogue_scene.positions.length !== 5 ||
    !game.epilogue_scene.positions.every(
      (position) =>
        Number.isFinite(position?.x) &&
        position.x >= 20 &&
        position.x <= 300 &&
        Number.isFinite(position?.y) &&
        position.y >= 0 &&
        position.y <= 180,
    ) ||
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
  const art = [...root.querySelectorAll("[data-scene-art]")];
  const objectSprites = [...root.querySelectorAll("[data-object-sprite]")];
  const encounters = [...root.querySelectorAll("[data-encounter]")];
  const status = document.getElementById("sheet-status");
  const questLog = document.getElementById("bonus");
  const questEntries = [...questLog.querySelectorAll("[data-quest]")];
  const gameSurfaces = [
    ...root.querySelectorAll(
      ".game-hud, .scene-panel, .story-deck, .game-controls",
    ),
  ];
  const questsButton = root.querySelector('[data-action="toggle-quests"]');
  const inspectButtons = [...root.querySelectorAll('[data-action="inspect"]')];
  const quests = new Map(
    questEntries.map((node) => [
      node.dataset.quest,
      {
        node,
        kind: node.dataset.questKind,
        screen: Number(node.dataset.targetScreen),
      },
    ]),
  );
  const discoveries = new Map(
    inspectButtons.map((button) => [
      button.dataset.discovery,
      {
        button,
        panel: document.getElementById(button.getAttribute("aria-controls")),
        screen: Number(button.dataset.screen),
        x: Number(button.dataset.x),
        y: Number(button.dataset.y),
      },
    ]),
  );
  const completedScreens = new Set();
  const foundDiscoveries = new Set();
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
  let questTrigger = questsButton;
  let activeDiscovery = null;

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

  function closeQuestLog(returnFocus = false) {
    const wasOpen = questLog.classList.contains("is-open");
    questLog.classList.remove("is-open");
    questLog.setAttribute("aria-hidden", "true");
    questLog.inert = true;
    questLog.removeAttribute("role");
    questLog.removeAttribute("aria-modal");
    questsButton.setAttribute("aria-expanded", "false");
    gameSurfaces.forEach((surface) => {
      surface.inert = false;
    });
    if (returnFocus && wasOpen) questTrigger.focus();
  }

  function openQuestLog(trigger = questsButton) {
    closeDiscovery();
    questTrigger = trigger;
    questLog.classList.add("is-open");
    questLog.removeAttribute("aria-hidden");
    questLog.inert = false;
    questLog.setAttribute("role", "dialog");
    questLog.setAttribute("aria-modal", "true");
    questLog.scrollTop = 0;
    questsButton.setAttribute("aria-expanded", "true");
    gameSurfaces.forEach((surface) => {
      surface.inert = true;
    });
    questLog.querySelector(".panel-close").focus();
  }

  function closeDiscovery(returnFocus = false) {
    if (!activeDiscovery) return;
    const { button, panel } = discoveries.get(activeDiscovery);
    panel.classList.remove("is-open");
    activeDiscovery = null;
    currentScreen().classList.remove("is-inspecting");
    render();
    if (returnFocus) button.focus();
  }

  function openDiscovery(id) {
    const discovery = discoveries.get(id);
    if (!discovery || discovery.screen !== screenIndex) return;
    closeDiscovery();
    activeDiscovery = id;
    foundDiscoveries.add(id);
    discovery.panel.classList.add("is-open");
    currentScreen().classList.add("is-inspecting");
    render();
    discovery.panel.scrollTop = 0;
    const heading = discovery.panel.querySelector("h3");
    heading.setAttribute("tabindex", "-1");
    heading.focus({ preventScroll: true });
  }

  function renderState(state) {
    // Home shares the final stats, not the final work scene.
    const home =
      currentScreen().dataset.screenKind === "ending"
        ? game.epilogue_scene
        : null;
    const region = home ? home.region_id : state.region;
    const scene = home ? home.art_key : state.region;
    const position = home
      ? home.positions[beatIndexes[screenIndex]]
      : state.position;
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
      });
      document.getElementById("badge-count").textContent = String(
        state.badges.length,
      ).padStart(2, "0");
      art.forEach((image) =>
        image.classList.toggle("current", image.dataset.sceneArt === scene),
      );
      objectSprites.forEach((object) =>
        object.classList.toggle(
          "current",
          object.dataset.objectSprite === state.object,
        ),
      );
      document.getElementById("world-label").textContent = REGIONS[region];
      document.getElementById("overworld").dataset.region = region;
      encounters.forEach((encounter) => {
        const active =
          encounter.dataset.encounter === currentScreen().dataset.checkpoint;
        encounter.classList.toggle("is-active", active);
        encounter.classList.toggle(
          "can-animate",
          active && !reducedMotion.matches,
        );
      });
      document.getElementById("overworld").dataset.mood = state.mood;
      root.dataset.checkpointIndex = state.index;
      lastEventIndex = state.index;
    }
    document
      .getElementById("journey-object-track")
      .setAttribute("transform", `translate(${position.x} ${position.y})`);
  }

  function render() {
    const screen = currentScreen();
    const beats = currentBeats();
    const beatIndex = clamp(beatIndexes[screenIndex], 0, beats.length - 1);
    const dialogueChanged =
      root.dataset.screenIndex !== String(screenIndex) ||
      root.dataset.beatIndex !== String(beatIndex);
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
    if (dialogueChanged)
      screen.querySelector(".title-card, .dialogue-card").scrollTop = 0;

    const finalBeat = beatIndex === beats.length - 1;
    document
      .getElementById("journey-marker")
      .classList.toggle(
        "is-celebrating",
        finalBeat &&
          screen.dataset.screenKind === "chapter" &&
          screen.dataset.milestone === "true" &&
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
    inspectButtons.forEach((button) => {
      const active =
        discoveries.get(button.dataset.discovery).screen === screenIndex;
      button.hidden = !active;
      button.setAttribute(
        "aria-expanded",
        String(active && activeDiscovery === button.dataset.discovery),
      );
    });
    if (screenIndex > 0 && finalBeat) completedScreens.add(screenIndex);
    quests.forEach((quest, id) => {
      quest.node.classList.toggle(
        "is-unlocked",
        quest.kind === "story"
          ? completedScreens.has(quest.screen)
          : foundDiscoveries.has(id),
      );
    });
    questLog.classList.toggle(
      "is-empty",
      !questEntries.some((entry) => entry.classList.contains("is-unlocked")),
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
      advanceLabel.textContent = "Next";
    }
  }

  function moveToScreen(nextIndex, direction = 1) {
    closeDiscovery();
    const previousScreen = currentScreen();
    previousScreen.classList.remove("is-inspecting");
    screenIndex = clamp(nextIndex, 0, screens.length - 1);
    const beats = [...screens[screenIndex].querySelectorAll(".dialogue-beat")];
    beatIndexes[screenIndex] =
      direction < 0 ? Math.max(0, beats.length - 1) : 0;
    lastEventIndex = null;
    touchStart = null;
    render();
    focusedHeading?.removeAttribute("tabindex");
    focusedHeading = currentScreen().querySelector("h1, h2, h3");
    focusedHeading?.setAttribute("tabindex", "-1");
    focusedHeading?.focus({ preventScroll: true });
  }

  function advance(trigger = document.activeElement) {
    if (questLog.classList.contains("is-open")) return;
    const screen = currentScreen();
    if (screen.classList.contains("is-inspecting")) {
      closeDiscovery(true);
      return;
    }
    const beats = currentBeats();
    if (beatIndexes[screenIndex] < beats.length - 1) {
      beatIndexes[screenIndex] += 1;
      render();
      return;
    }
    if (screenIndex < screens.length - 1) moveToScreen(screenIndex + 1);
    else openQuestLog(trigger);
  }

  function back() {
    if (questLog.classList.contains("is-open")) return;
    const screen = currentScreen();
    if (screen.classList.contains("is-inspecting")) {
      closeDiscovery(true);
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
    closeQuestLog();
    html.classList.remove("enhanced");
    screens.forEach((screen) => {
      screen.classList.remove("is-current-screen", "is-inspecting");
      screen.removeAttribute("aria-hidden");
    });
    root
      .querySelectorAll(".chapter")
      .forEach((chapter) => chapter.classList.remove("is-current-chapter"));
    chapters.forEach((chapter) => chapter.removeAttribute("aria-hidden"));
    fallbackOnly.forEach((node) => node.removeAttribute("aria-hidden"));
    questLog.inert = false;
    questLog.removeAttribute("aria-hidden");
    status.textContent = "Opening stats. The complete story follows.";
  }

  try {
    game = JSON.parse(root.dataset.game);
    const validScreen = (value) =>
      Number.isInteger(value) && value >= 1 && value < screens.length;
    const storyQuests = [...quests.entries()].filter(
      ([, quest]) => quest.kind === "story",
    );
    if (
      window
        .getComputedStyle(html)
        .getPropertyValue("--chapter-adventure")
        .trim() !== "ready" ||
      screens.length !== markers.length + 2 ||
      art.length !== 5 ||
      new Set(art.map((image) => image.dataset.sceneArt)).size !== 5 ||
      art.some(
        (image) =>
          !Object.hasOwn(REGIONS, image.dataset.sceneArt) &&
          image.dataset.sceneArt !== "san-jose-home",
      ) ||
      questEntries.length !== 24 ||
      quests.size !== 24 ||
      inspectButtons.length !== 11 ||
      discoveries.size !== 11 ||
      root.querySelectorAll("[data-discovery-panel]").length !== 11 ||
      storyQuests.length !== game.events.length + 1 ||
      new Set(storyQuests.map(([, quest]) => quest.screen)).size !==
        storyQuests.length ||
      [...quests].some(([id, quest]) => {
        if (
          !/^[a-z][a-z0-9-]{0,63}$/.test(id) ||
          !validScreen(quest.screen) ||
          quest.node.dataset.targetScreen !== String(quest.screen)
        )
          return true;
        const screen = screens[quest.screen];
        const link = quest.node.querySelector('[data-action="revisit"]');
        if (quest.kind === "story")
          return (
            id !== (screen.dataset.checkpoint ?? "epilogue") ||
            link?.getAttribute("href") !== `#${screen.id}`
          );
        if (quest.kind !== "discovery") return true;
        const discovery = discoveries.get(id);
        return (
          !discovery ||
          discovery.screen !== quest.screen ||
          discovery.button.dataset.screen !== String(discovery.screen) ||
          discovery.panel?.id !== `discovery-${id}` ||
          discovery.panel.dataset.discoveryPanel !== id ||
          !screen.contains(discovery.panel) ||
          link?.getAttribute("href") !== `#discovery-${id}` ||
          !Number.isFinite(discovery.x) ||
          discovery.x < 48 ||
          discovery.x > 272 ||
          !Number.isFinite(discovery.y) ||
          discovery.y < 48 ||
          discovery.y > 132
        );
      }) ||
      statRows.length !== STAT_KEYS.length ||
      statRows.some((row, index) => row.dataset.stat !== STAT_KEYS[index]) ||
      !validGame(
        game,
        markers,
        new Set(badgeSlots.map((slot) => slot.dataset.badge)),
      ) ||
      game.epilogue_scene.positions.length !==
        screens.at(-1).querySelectorAll(".dialogue-beat").length
    )
      throw new Error("Invalid story projection");

    html.classList.add("enhanced");
    discoveries.forEach(({ button, x, y }) => {
      button.style.left = `${(x / 320) * 100}%`;
      button.style.top = `${(y / 180) * 100}%`;
    });
    fallbackOnly.forEach((node) => node.setAttribute("aria-hidden", "true"));
    questLog.setAttribute("aria-hidden", "true");
    questLog.inert = true;
    render();

    root.addEventListener("click", (event) => {
      const trigger = event.target.closest("[data-action]");
      const action = trigger?.dataset.action;
      if (!action) return;
      if (action === "revisit") {
        if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey)
          return;
        event.preventDefault();
        const entry = trigger.closest("[data-quest]");
        const quest = quests.get(entry?.dataset.quest);
        if (
          !quest ||
          quest.node !== entry ||
          !(quest.kind === "story"
            ? completedScreens.has(quest.screen)
            : foundDiscoveries.has(entry.dataset.quest))
        )
          return;
        closeQuestLog();
        moveToScreen(quest.screen);
        if (quest.kind === "discovery") openDiscovery(entry.dataset.quest);
      } else if (action === "advance") advance(trigger);
      else if (action === "back") back();
      else if (action === "inspect") {
        if (activeDiscovery === trigger.dataset.discovery) {
          closeDiscovery(true);
          return;
        }
        openDiscovery(trigger.dataset.discovery);
      } else if (action === "close-discovery") {
        closeDiscovery(true);
      } else if (action === "toggle-quests") {
        openQuestLog(trigger);
      } else if (action === "close-panels") closeQuestLog(true);
    });

    document.addEventListener("keydown", (event) => {
      if (event.defaultPrevented || event.isComposing) return;
      if (event.key === "Escape") {
        if (questLog.classList.contains("is-open")) closeQuestLog(true);
        else closeDiscovery(true);
        return;
      }
      if (questLog.classList.contains("is-open")) {
        if (
          event.key === "Tab" &&
          !event.altKey &&
          !event.ctrlKey &&
          !event.metaKey
        ) {
          const targets = [
            ...questLog.querySelectorAll("button, a[href]"),
          ].filter((node) => node.getClientRects().length);
          const edge = event.shiftKey ? targets[0] : targets.at(-1);
          if (document.activeElement === edge) {
            event.preventDefault();
            (event.shiftKey ? targets.at(-1) : targets[0]).focus();
          }
        }
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
        touchStart = null;
        if (
          event.pointerType === "touch" &&
          event.isPrimary &&
          !questLog.classList.contains("is-open") &&
          !event.target.closest(
            "a, button, input, textarea, select, [contenteditable], .discovery-panel",
          )
        )
          touchStart = {
            id: event.pointerId,
            x: event.clientX,
            y: event.clientY,
          };
      },
      { passive: true },
    );
    gameShell.addEventListener(
      "pointerup",
      (event) => {
        if (
          !touchStart ||
          event.pointerType !== "touch" ||
          event.pointerId !== touchStart.id
        )
          return;
        const x = event.clientX - touchStart.x;
        const y = event.clientY - touchStart.y;
        touchStart = null;
        if (Math.abs(x) < 52 || Math.abs(y) > Math.abs(x) * 0.75) return;
        if (x < 0) advance();
        else back();
      },
      { passive: true },
    );
    gameShell.addEventListener("pointercancel", () => {
      touchStart = null;
    });
    reducedMotion.addEventListener("change", () => {
      // Restoring motion does not replay an encounter already entered with reduced motion.
      encounters.forEach((encounter) =>
        encounter.classList.remove("can-animate"),
      );
      render();
    });
    window.addEventListener("pageshow", render);
  } catch {
    fallback();
  }
}

const journey = document.getElementById("journey");
if (journey) {
  // WebKit can execute a module before the stylesheet is applied. Until load,
  // the complete server document stays readable rather than hiding behind a gate.
  if (document.readyState === "complete") startJourney(journey);
  else
    window.addEventListener("load", () => startJourney(journey), {
      once: true,
    });
}
