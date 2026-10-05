**Portfolio Architecture**
Status: approved chapter-adventure design, implemented locally; final cross-browser/public verification is recorded in [handoff.md](handoff.md).
Prepared: 2026-09-06. Revised for the chapter adventure: 2026-10-04. Owner: Pranav Prem. Canonical origin: `https://pranavprem.com`.

**Purpose**
This is a warm pixel-game autobiography, not a resume with animation beside it. The enhanced site is a full-screen, linear chapter adventure. The landscape, current chapter object, dialogue, discoveries, stats, milestones, and controls form one game scene. The complete human story, including uncertainty, illness, boredom, burnout, hobbies, and current joy, remains more important than game chrome.

The public repository is `https://github.com/pranavprem/portfolio`. The private source PDFs are not build inputs. Their owner-authorized, public-safe evidence is preserved in [story.md](story.md); do not reopen, serve, embed, or commit them.

**Core Decisions**

- Runtime remains Python 3.13, Flask, Jinja, Gunicorn, one local CSS file, one vanilla JavaScript module, local JSON, system fonts, and original SVG.
- The server renders every paragraph, fact, link, stat equivalent, milestone description, and optional highlight. JavaScript changes presentation and visibility; it does not construct prose.
- Enhanced mode owns the usable `100dvh` viewport. Document scrolling does not drive progression.
- The story is linear. Start/Continue/Back, keyboard controls, and touch swipes change dialogue/chapter position; Inspect, Stats, and Quest log reveal optional information without changing the route.
- Game state is selected from absolute authored snapshots. No additive XP logic, random state, URL state, cookie, local storage, session storage, database, or server mutation exists.
- Mobile is a first-class game layout with a scene, dialogue panel, and fixed thumb controls, not a compressed desktop essay.
- No living avatar, mascot, pet, or companion appears. Eleven original objects identify the chapters.
- No framework, game engine, canvas/WebGL dependency, runtime npm, CMS, analytics, remote font, embed, or remote runtime request is introduced.

**Experience Contract**

The game has fourteen screens in presentation order:

1. Title screen using the opening state.
2. Twelve event screens from eleven chapters; chapter 09 has two events.
3. Epilogue holding the final event state.

Each event screen contains one or more paragraph-sized dialogue beats. Exactly one beat is visible in enhanced mode. The final beat reveals that event's milestone reward, if any. Continue advances a beat, then travels to the next event. Back rewinds a beat, then returns to the previous event at its final beat. This behavior is bounded at the title and epilogue.

The scene hotspot toggles the current card's discovery panel. Facts and contextual project links live there. It does not grant stats or branch the story. Stats opens the five-stat sheet; Quest log opens the 21 optional highlights. Escape closes an overlay and returns focus to the opening control.

Supported enhanced inputs:

| Input                     | Behavior                                                                                       |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| Start / Continue button   | Advance dialogue, then screen; open Quest log after the final epilogue beat.                   |
| Back button               | Rewind dialogue, then screen.                                                                  |
| Right Arrow, Enter, Space | Same as Continue when focus is not in an interactive/editable element and no modifier is held. |
| Left Arrow                | Same as Back under the same guard.                                                             |
| Horizontal touch swipe    | Left advances; right rewinds after a 52px distance threshold and directional check.            |
| Inspect                   | Toggle current scene discovery; Continue returns to dialogue while inspection is open.         |
| Stats / Quest log         | Open bounded overlays.                                                                         |
| Escape                    | Close an open overlay and restore focus.                                                       |

Wheel/trackpad movement is not progression input. Do not add wheel-to-advance, scroll-jacking, drag-only input, branching choices, combat, timers, skill checks, sound, saved progress, or browser-history entries per beat.

Approved ordinary links are curated GitHub work, LinkedIn, `mailto:pranavprem93@gmail.com`, and the timestamped Coldplay/Oxfam cameo. Links remain links, not whole-card targets or remote previews. Keyboard shortcuts yield while a link, button, form control, or editable element has focus.

**Story Map**

| Chapter          | Region        | Object          | Direction                                                                          |
| ---------------- | ------------- | --------------- | ---------------------------------------------------------------------------------- |
| `spawn`          | Goa           | controller      | PC games at seven and making small games at eight.                                 |
| `school`         | Goa           | backpack        | C/C++, house captain, public speaking/debate, Class 12 result.                     |
| `detour`         | Goa           | compass         | Complicated dengue and hospital month before finals; route to GEC.                 |
| `college`        | Goa           | laptop          | Independent living, leadership, Python/PyCon, Zuari, paper, hackathons, academics. |
| `java-forge`     | Pune          | Java mug        | HSDI, six-month Java training, top-of-class result, leadership.                    |
| `automation`     | Pune          | automation gear | Boredom, TasKing, Green Belt savings, banking friction, US study.                  |
| `sjsu`           | San Jose      | books           | MS, 110%-to-TA account, grading tools, SpartanBot.                                 |
| `developer-ally` | San Jose      | toolkit         | Google Hardware/Nest and developer-productivity focus.                             |
| `cloud-and-fog`  | San Francisco | cloud terminal  | Chat infrastructure, then sustainable COVID cadence.                               |
| `bot-workshop`   | San Francisco | bot console     | Einstein Bots reliability/API/migration and Copilot.                               |
| `continuing`     | San Francisco | agent nodes     | Agentforce, Atlas/AgentScript, current capability work and enthusiasm.             |

The epilogue returns narratively to San Jose for OpenClaw/Hermes/Morpheus, homelab automation, and 3D printing. It is not another stat checkpoint.

**Content And Provenance**

`docs/story.md` is the complete public-safe ledger. `app/content/story.json` is the curated runtime selection. Source kinds remain `owner-supplied`, `supplied-document`, and catalog-only `public-repository`; none means independent institutional verification or a security audit.

The current content schema is version 2:

- Exactly five stats in this order: `coding`, `enthusiasm`, `vitality`, `charisma`, `experience`.
- Exactly four regions in this order: `goa`, `pune`, `san-jose`, `bay-area`.
- Exactly eleven chapters and twelve cards/events; only chapter 09 has two cards.
- Exactly eleven milestones, granted once in authored order.
- Exactly 21 optional achievement groups.
- Complete absolute `stats_after` and cumulative `badges_after` snapshots.
- Region landmarks bounded to the shared `320 x 180` scene geometry.
- Plain-text prose and facts only. Contextual links are selected by trusted template logic.

Validation rejects unknown/missing keys, booleans as integers, nonfinite/out-of-range coordinates, duplicate JSON keys/IDs, invalid source references, wrong counts/order, decreasing Experience, duplicate badge grants, unsafe links, symlinks, missing assets, and unapproved static files. Authored errors fail startup; they are never silently repaired in the browser.

**State Contract**

`prepare_story()` emits a prose-free inert projection:

```text
{
  schema_version,
  initial: {stats, badges, region_id, position, mood},
  events: [{id, chapter_id, region_id, position, mood, stats_after, badges_after}]
}
```

Jinja serializes it in the quoted `data-game` attribute with `tojson | forceescape`. The browser parses it with `JSON.parse`; no executable inline data or fetch endpoint is used.

`deriveState(game, eventIndex)` clamps only untrusted numeric test input to `-1..11` and returns a fresh object containing the selected absolute stats, badge prefix, region, mood, chapter object, and landmark. Runtime navigation supplies only bounded values:

- title: event index `-1`
- event screens: `0..11`
- epilogue: event index `11`

Dialogue beat position is local presentation state. It cannot change stats, badges, region, mood, or source data. Re-entering an event restores that event's exact snapshot. The DOM exposes current screen, beat, and checkpoint indices for deterministic testing, not as a public API.

The authoritative snapshots are:

| State              | Coding | Enthusiasm | Health | Charisma | Experience |
| ------------------ | -----: | ---------: | -----: | -------: | ---------: |
| Opening            |      0 |          1 |      1 |        1 |          0 |
| First game         |      1 |          6 |      8 |        2 |          1 |
| School             |      3 |          8 |      8 |        5 |          2 |
| Dengue / finals    |      3 |          5 |      3 |        5 |          2 |
| College            |      6 |          9 |      7 |        6 |          3 |
| Java training      |      7 |          8 |      7 |        6 |          4 |
| HSBC automation    |      6 |          3 |      7 |        6 |          4 |
| SJSU               |     10 |          9 |      8 |        7 |          5 |
| Google             |      8 |         10 |      8 |        7 |          5 |
| Chat               |      8 |          9 |      8 |        7 |          6 |
| COVID cadence      |      8 |          7 |      6 |        7 |          6 |
| Bots/Copilot       |      8 |          9 |      7 |        7 |          6 |
| Agentforce / final |      8 |         10 |      8 |        7 |          7 |

Only Enthusiasm is full at the ending. SJSU Coding 10 is a historical intensity peak, not a mastery claim. Experience never decreases.

**Rendering Model**

Base HTML is an ordinary complete document:

- one introduction
- eleven semantic chapter sections and twelve article cards
- all dialogue paragraphs and discoveries
- semantic per-card stat equivalents and milestone descriptions
- ending and optional catalog
- in-flow region illustrations

Controls are present but hidden by base CSS. If JavaScript validates the projection and matching DOM markers, it adds `.enhanced`, marks fallback-only nodes assistive-hidden, and selects one game screen/beat. If parsing, validation, or initialization fails, `.enhanced` is removed and every server-rendered section remains readable. CSS failure also leaves document-order HTML. Print overrides enhanced visibility and exposes all content.

JavaScript uses `textContent`, class changes, `aria-*`, `inert`, focus, and narrowly bounded SVG `transform` attributes. It does not use `innerHTML`, string-to-code evaluation, remote requests, runtime templates, or inline style strings. The only CSSOM write is the bounded chapter-progress width.

**Visual Layout**

Desktop uses a two-pane frame: landscape left, dialogue right, HUD above, controls below. Mobile uses four rows: HUD, landscape, dialogue, thumb controls. Both fit the usable viewport and include all safe-area insets.

Normal mobile targets:

- Minimum supported width: 320 CSS pixels.
- Controls: at least 48 CSS pixels high.
- Landscape: approximately 31-37dvh depending on viewport height.
- Dialogue: remaining flexible space; one paragraph beat normally fits without scrolling.
- Internal dialogue scrolling is allowed only for enlarged text, unusually short screens, or long optional overlays.
- No horizontal overflow, page scrolling, text shrinking, hidden overflow used to mask defects, or separate low-information mobile HUD.

The visual language remains cream paper, dark green ink, amber/rust accents, crisp pixel landscapes, system serif display type, monospace game labels, square borders, and stepped shadows. Dark mode follows `prefers-color-scheme` with no toggle/storage.

The scene uses original landscapes and factual building labels, not logos or copied architecture. Object markers are inanimate and decorative. The PLA block uses the original generic robot and “I'm 40% PLA.” without an explicit character voice cue. No copied franchise artwork is permitted.

**Motion**

- Scene object movement between authored landmarks uses a short stepped CSS transition.
- A milestone's final dialogue beat reveals a reward block and one eight-logical-pixel object hop with static sparks.
- There is no requestAnimationFrame loop, idle movement, flashing, camera shake, sound, confetti, count-up, or queued animation.
- `prefers-reduced-motion: reduce` disables all transitions/animations immediately while preserving state and controls.
- Opening/closing overlays may use a brief bounded stepped transition, but initial page load must not flash a closed panel.

**Accessibility**

- Buttons are native `button type="button"` elements with explicit labels and at least 48px mobile targets.
- Noncurrent game screens and fallback-only duplicate headings/art are removed from the enhanced accessibility tree.
- Scene art and object SVGs are decorative; narrative equivalents are text.
- Numeric `n / 10` text is authoritative; pips do not carry meaning alone.
- Dynamic HUD is `aria-live="off"`; changing screens moves focus to the new heading.
- Closed overlays are inert and assistive-hidden. Quest log makes the game shell inert while open. Escape restores focus.
- Text selection, ordinary links, semantic headings/lists, forced colors, reduced motion, print, and no-JS reading remain supported.
- Automated axe checks supplement rather than replace physical-device, zoom, and screen-reader review.

**Security And Privacy**

The HTTP surface remains GET/HEAD-only:

| Path             | Contract                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------ |
| `/`              | Complete HTML, fixed canonical origin, `Cache-Control: no-cache`.                          |
| `/healthz`       | Minimal JSON, `Cache-Control: no-store`.                                                   |
| `/static/<path>` | Approved static inventory only; conditional one-hour cache and deterministic digest query. |
| errors           | Generic 400/404/405/413/500 pages with no reflected request details.                       |

Keep exact trusted hosts, bounded request bodies, Jinja autoescaping, strict CSP, generic sanitized logging, no CORS/sessions, no forwarded-header trust, and no request-derived redirect/template/path behavior. No visitor data, progress, query, IP, header, token, or PII is logged or persisted by the application.

Production remains the hardened `portfolio` Gunicorn service plus pinned `cloudflared`, using `compose.yaml` and `compose.tunnel.yaml`, no published ports, read-only roots, nonroot identities, dropped capabilities, resource limits, and the private origin `http://portfolio:8000`. Portainer supplies `CLOUDFLARED_TOKEN`; only cloudflared receives the mapped `TUNNEL_TOKEN`. Never expose it in Git, commands, logs, screenshots, or support output.

Cloudflare owns public TLS and HTTP-to-HTTPS redirect. Keep `PORTFOLIO_HSTS=0` until the redirect is verified publicly; then enable the exact one-year HSTS value without includeSubDomains/preload.

**Verification Matrix**

| Area             | Required checks                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Content          | Exact schema/counts, source mapping, word budget, all snapshots/badge prefixes, complete server HTML.                          |
| Navigation       | Start, every dialogue beat, event transitions, epilogue, bounded Back, keyboard guards, horizontal swipes.                     |
| Interaction      | Inspect toggle, optional links, Stats and Quest log overlays, Escape/focus restoration, no branching mutation.                 |
| Responsive       | 320x568, 390x844, tablet, desktop; scene/dialogue/control clearance; 48px targets; safe areas; no page/horizontal scroll.      |
| Accessibility    | Heading focus, semantic fallback, inert/aria states, axe in both themes, enlarged text, forced colors, selection, print.       |
| Failure          | No JS, invalid projection variants, CSS/JS/art failure, missing assets, startup validation errors.                             |
| Motion           | Reward/transition bounds, no idle animations, reduced-motion behavior.                                                         |
| Security/privacy | CSP, same-origin requests, empty cookies/storage, hostile escaped content, static/traversal/host/method boundaries.            |
| Runtime          | Lint/format, all Python tests, Chromium/Firefox/WebKit, Compose parsing, healthy local container, exact runtime file boundary. |
| Production       | Exact-SHA CI, Portainer pull/redeploy, versioned public assets, HTTPS/health/headers, HTTP redirect before HSTS.               |

**Completion Gate**

Do not call the redesign complete until:

1. `AGENTS.md`, README, this architecture, story ledger, handoff, review, and retrospective agree on the chapter-adventure contract.
2. All local lint, Python, three-engine browser, and container checks pass with outcomes recorded in the handoff.
3. Main-session visual review covers at least 390x844 mobile and 1440x1000 desktop in both an opening and mid-story scene.
4. Exact deployment commit CI passes and Portainer deploys that revision.
5. Public HTML references the new digest-versioned JS/CSS and public behavior matches the chapter game.
6. HTTP redirects to HTTPS before HSTS is enabled.
7. Remaining physical-device, native zoom, screen-reader, NAS firewall/isolation, and recovery checks are stated as unverified unless actually performed.

**Decision Record**

- The earlier native-scroll essay and later sticky-stage layout are superseded. Owner review found both still felt like reading a book with animation beside it.
- The chapter adventure was selected over direct avatar movement. It provides genuine interaction and mobile parity without inventing a character, collision engine, branching biography, or inaccessible gesture-only controls.
- Paragraph-sized dialogue preserves the approved prose while preventing a wall of text.
- Optional facts became scene discoveries; the achievement appendix became a Quest log. Neither alters canonical state.
- Server-rendered fallback remains non-negotiable so content survives JavaScript, CSS, projection, print, accessibility, and archival failure modes.
