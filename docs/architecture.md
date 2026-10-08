**Portfolio Architecture**
Status: approved chapter-adventure design, implemented locally; final cross-browser/public verification is recorded in [handoff.md](handoff.md).
Prepared: 2026-09-06. Current revision: separate gaming/hobby discoveries and paid-work/personal-project copy in the San Jose home ending, with the chronological Quest log retained. Owner: Pranav Prem. Canonical origin: `https://pranavprem.com`.

**Purpose**
This is a warm pixel-game autobiography, not a resume with animation beside it. The enhanced site is a full-screen, linear chapter adventure. The landscape, current chapter object, dialogue, discoveries, stats, milestones, and controls form one game scene. The complete human story, including uncertainty, illness, boredom, burnout, hobbies, and current joy, remains more important than game chrome.

The public repository is `https://github.com/pranavprem/portfolio`. The private source PDFs are not build inputs. Their owner-authorized, public-safe evidence is preserved in [story.md](story.md); do not reopen, serve, embed, or commit them.

**Core Decisions**

- Runtime remains Python 3.13, Flask, Jinja, Gunicorn, one local CSS file, one vanilla JavaScript module, local JSON, system fonts, and original SVG.
- The server renders every paragraph, fact, link, stat equivalent, milestone description, and optional highlight. JavaScript changes presentation and visibility; it does not construct prose.
- Enhanced mode owns the usable `100dvh` viewport. Document scrolling does not drive progression.
- The story is linear. Start/Continue/Back, keyboard controls, and touch swipes change dialogue/chapter position; window discoveries and Quest log reveal optional information without changing the route. Stats remain visible throughout.
- Game state is selected from absolute authored snapshots. No additive XP logic, random state, URL state, cookie, local storage, session storage, database, or server mutation exists.
- Mobile is a first-class game layout with a scene, dialogue panel, and fixed thumb controls, not a compressed desktop essay.
- No living avatar, mascot, pet, or companion appears. Eleven original objects identify the chapters.
- No framework, game engine, canvas/WebGL dependency, runtime npm, CMS, analytics, remote font, embed, or remote runtime request is introduced.

**Experience Contract**

**Home Copy Revision**
The owner now describes the local-AI repositories as mostly defunct/not running and asks for a separate list-form hobby easter egg. Main-session design/review: remove `local-ai` and its OpenMemory/Qdrant/Neo Services links from runtime content; preserve their qualified source history. Keep `off-clock` for gaming and add `hobbies` at an original generic guitar `(264,113)`, leaving eleven discoveries and 24 journal records. No checkpoint, state, persistence, navigation rule, or network permission changes.

Add only optional discovery `list_items`: 1-12 distinct plain-text strings, each at most 100 characters, with paragraphs and list items together bounded to 600 characters. Existing paragraphs remain required. Reject invalid types, empty/duplicate items, controls, excess length, and unknown fields at startup. Jinja escapes a semantic `<ul>`/`<li>` after the paragraphs; no HTML/Markdown interpretation or client prose construction. The list remains complete in fallback and print, and its last item is "Making lists. You may have noticed." Review covers escaping, exact inventory, separate unlock/return targets, list order, mobile scrolling/focus/48px glints, enlarged text, and all engines.

The paid-work passage uses "For my wages, I build systems that connect..." rather than asserting enjoyment of corporate integration. "But for fun..." introduces the existing home projects, not new invented capabilities. Preserve the Agentforce technical scope, present enthusiasm, personal-agent/Morpheus account, and five ending beats/positions. The guitar is symbolic art, not an ownership, model, or skill claim.

**Home Scene Revision**
The owner's next correction gives "DevOps, but it's my house" its own San Jose home scene instead of holding the Golden Gate/Salesforce artwork. Main-session design/review: retain the four geographic regions, all eleven chapters, twelve stat checkpoints, eleven milestones, and 24 journal records. Add one original `san-jose-home.svg` scene variant and a validated `epilogue_scene` with region `san-jose`, that fixed art key, and five absolute marker positions corresponding to the five ending beats. The marker visits the front path, homelab, then printing bench; the last three printing beats share a position. This is an explicit presentation-only exception to the old final-scene hold, not another stat checkpoint.

The final stats/badges remain selected by event 11 through `deriveState()`. Rendering selects the home art, San Jose label, and authored marker position by the ending screen/beat. Back and Quest log jumps must restore the correct work/home scene while retaining the page-local journal. Existing stepped movement and reduced-motion behavior apply; add no idle animation, timer, or navigation gate. The two ending discoveries use the gaming monitor and guitar; the earlier server-rack discovery is retired by the copy revision above. Add the home illustration to no-JS/print output, startup asset requirements, the explicit Docker allowlist, and the 16-file runtime boundary.

The house and equipment are original symbolic art: generic home automation, servers, a gaming/simulator corner, and a printer. They are not a real facade, floor plan, address, device model, network topology, or NAS-location disclosure. No private photograph or configuration is needed. Acceptance covers correct home entry/return, each beat's visual position, unchanged final stats, discovery geometry/focus, reduced motion, malformed scene data, missing art, fallback/print, CSP/SVG safety, mobile fit, and the rebuilt container.

**Quest Log Revision**
The Quest log correction supersedes the old 21-item, newest-first catalog and timeline-only unlock rules. The owner explicitly chose to keep scene popups, include their summaries in the Quest log, avoid repeats elsewhere in the game, provide chronological summaries of the whole main story, and make each log entry revisit its original scene. That earlier task authorized its commit/push, not a production redeployment or blanket publication permission for later revisions.

Main-session design and review:

- Keep eleven chapters, twelve event snapshots, five stats, and the main route. Add a short `summary` to each card and an `epilogue_summary`. Derive a chronological Quest log with thirteen main-story records and eleven discovery records, rather than maintaining a separate achievement catalog. Main summaries cover the whole card and revisit its first beat. The title's identity/Goa context is covered by the current-work and childhood summaries rather than inserting a present-day entry before childhood.
- Replace card `facts` and the old catalog with one authored `discoveries` collection. Each record owns its ID, target card (or `epilogue`), heading, period label, plain-text paragraphs, short summary, source references, reviewed links, and bounded scene position. Python prepares the popup and log from that one source. No fact may exist only in the log. The original catalog's degree, research, tool, metric, project, nomination, promotion, award, and hobby details remain in main prose or a discovery; the full ledger stays intact.
- Discovery targets: GEC extras and early games/CyanogenMod at college; Green Belt/CI-CD and Coldplay at the Pune chapter; Opportunity Hack at SJSU; degree/research detail and concrete developer tooling during the MS/Google scene; promotions and awards at current work; gaming and a separate hobby list at the ending. The cameo's supplied age 22 supports its narrative placement after the age-20 HSDI recollection; do not invent a calendar date or imply filming in Pune. Broad period labels remain broad. Grouped awards span the career and do not inherit the current chapter's year.
- Main summaries unlock at their card's final beat; discovery summaries unlock only when their popup is opened. Two bounded in-memory sets retain reached story cards and found discoveries for this page visit. Back/jump restores absolute stats without erasing the journal. Reload resets it; no cookie, storage, session, URL progress, or server mutation is introduced. Discoveries never gate the main route or modify stats.
- Keep nonmodal scene popups, one open at a time, with visible dialogue, native 48px glints, Escape/Close, and exact trigger focus restoration. Multiple discoveries may share a screen; positions must not overlap at tested mobile sizes. Validated numeric positions use bounded CSSOM `left`/`top` values under the existing CSP.
- Remove repeated narrative reward blocks from the main scene, including Green Belt's spoiler. Keep the decorative milestone response and authored snapshot prefix. Milestone descriptions belong in the Quest log with the corresponding story/discovery record. The HUD rack remains decorative and its numeric count authoritative. Opportunity Hack exists once as a popup plus its summary, not in the main SJSU beat. Gaming and other hobbies likewise each have one ending discovery.
- Quest log headings are internal links in fallback HTML. Enhanced activation closes the log, moves to the validated target, and focuses its heading; discovery entries reopen their original popup. Only unlocked entries may navigate. External project/video links remain separate. No whole-card click handler, URL/history update, animation wait, or arbitrary selector execution is added.
- Retain every popup and all 24 summaries in semantic server HTML, no-JS, invalid-data, CSS/script failure, and print output. Validate exact coverage, unique IDs, known targets, safe links, finite positions, sources, and text limits. The prose-free stat projection stays version 2; the coordinated internal authoring/DOM revision needs no compatibility layer because no content API or persisted progress exists.
- Acceptance: every prior catalog detail has a main/popup source; no repeated optional/reward prose; chronological order; found-only discoveries; main completion; jump/back/focus; retained journal on revisit; reload reset; invalid targets/positions fail safely; complete fallback/print; all browser engines, CSP, mobile target separation, and reduced motion. No new runtime dependency, route, file, or network permission is needed.

Persistent HUD stats, place-only captions, and bounded mosquito/COVID encounters remain. The Quest log overlays the game below the HUD; keyboard/swipe progression pauses while it is open. Observed verification status belongs in the handoff.

The game has fourteen screens in presentation order:

1. Title screen using the opening state.
2. Twelve event screens from eleven chapters; chapter 09 has two events.
3. Epilogue holding the final stats/badges while returning to the San Jose home scene.

Each event screen contains one or more paragraph-sized dialogue beats. Exactly one beat is visible in enhanced mode. The final beat records that story moment and gives decorative milestone feedback if applicable; it does not repeat the story in a reward paragraph. Continue advances a beat, then travels to the next event. Back rewinds a beat, then returns to the previous event at its final beat. This is bounded at the title and epilogue.

College retains four main beats (independence, Python/PyCon, hackathons, academic standing). Department leadership, Zuari, and the paper are separate paragraphs in a GEC discovery. Automation retains two main beats; Green Belt and separate CI/CD detail are a discovery, not another dialogue or reward recital. Stat snapshots and milestone grant points are unchanged. Finding optional content unlocks its log record but never gates main progression or mutates stats.

Each active glint opens its own discovery popup over the landscape while dialogue stays visible. Only one popup is open at a time; multiple glints on one screen retain distinct targets and focus. The five-stat HUD is always visible. Quest log shows reached story summaries and found discoveries below it. Escape closes an overlay and returns focus to the actual opener, including the epilogue's final button.

Supported enhanced inputs:

| Input                     | Behavior                                                                                       |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| Start / Continue button   | Advance dialogue, then screen; open Quest log after the final epilogue beat.                   |
| Back button               | Rewind dialogue, then screen.                                                                  |
| Right Arrow, Enter, Space | Same as Continue when focus is not in an interactive/editable element and no modifier is held. |
| Left Arrow                | Same as Back under the same guard.                                                             |
| Horizontal touch swipe    | Left advances; right rewinds after a 52px distance threshold and directional check.            |
| Window glint              | Toggle current scene discovery; Continue returns to dialogue while the popup is open.          |
| Quest log                 | Open a bounded overlay below the persistent HUD.                                               |
| Escape                    | Close an open overlay and restore focus.                                                       |

Wheel/trackpad movement is not progression input. Do not add wheel-to-advance, scroll-jacking, drag-only input, branching choices, combat, timers, skill checks, sound, saved progress, or browser-history entries per beat.

Approved ordinary links are curated GitHub work, LinkedIn, `mailto:pranavprem93@gmail.com`, and the timestamped Coldplay/Oxfam cameo. Links remain links, not whole-card targets or remote previews. Keyboard shortcuts yield while a link, button, form control, or editable element has focus.

**Story Map**

| Chapter          | Region        | Object          | Direction                                                                          |
| ---------------- | ------------- | --------------- | ---------------------------------------------------------------------------------- |
| `spawn`          | Goa           | controller      | PC games at seven and making small games at eight.                                 |
| `school`         | Goa           | backpack        | Computer science in 11th/12th grade, C/C++, house captain, public speaking/debate. |
| `detour`         | Goa           | compass         | Complicated dengue and hospital month before finals; route to GEC.                 |
| `college`        | Goa           | laptop          | Independent living, leadership, Python/PyCon, Zuari, paper, hackathons, academics. |
| `java-forge`     | Pune          | Java mug        | HSDI, six-month Java training, top-of-class result, leadership.                    |
| `automation`     | Pune          | automation gear | Boredom, TasKing, Green Belt savings, banking friction, US study.                  |
| `sjsu`           | San Jose      | books           | MS, 110%-to-TA account, grading tools, SpartanBot.                                 |
| `developer-ally` | San Jose      | toolkit         | Google Hardware/Nest and developer-productivity focus.                             |
| `cloud-and-fog`  | San Francisco | cloud terminal  | Chat infrastructure, then sustainable COVID cadence.                               |
| `bot-workshop`   | San Francisco | bot console     | Einstein Bots reliability/API/migration and Copilot.                               |
| `continuing`     | San Francisco | agent nodes     | Agentforce, Atlas/AgentScript, current capability work and enthusiasm.             |

The epilogue returns visually and narratively to San Jose for OpenClaw/Hermes/Morpheus, homelab automation, and 3D printing. Its original home scene replaces the prior Golden Gate backdrop without adding a stat checkpoint or geographic region.

**Content And Provenance**

`docs/story.md` is the complete public-safe ledger. `app/content/story.json` is the curated runtime selection. Source kinds remain `owner-supplied`, `supplied-document`, and discovery-only `public-repository`; none means independent institutional verification or a security audit.

The latest semantic/voice review covers every public copy surface, including templates, rewards, the catalog, metadata, and controls. Keep real grammatical subjects and distinguish roles, tools, projects, and places; do not compress source facts into ambiguous resume fragments. The public Slack connector link is inline in the Bots/API beat, not in the unrelated hobbies discovery. This editorial revision changes no schema, snapshots, unlock anchors, or source classifications.

The current content schema is version 2:

- Exactly five stats in this order: `coding`, `enthusiasm`, `vitality`, `charisma`, `experience`.
- Exactly four regions in this order: `goa`, `pune`, `san-jose`, `bay-area`.
- Exactly eleven chapters and twelve cards/events; only chapter 09 has two cards.
- Exactly eleven milestones, granted once in authored order.
- Exactly eleven discoveries and 24 derived Quest log records: twelve cards, the epilogue, and the eleven discoveries.
- Cards own `summary` text; the root owns `epilogue_summary`. Discoveries own `id`, `card_id`, `heading`, `period_label`, `body`, `summary`, `position`, `source_refs`, and `links`, with optional bounded `list_items` as defined above. The old `facts`, `achievements`, `era`, and `unlock_after` fields are removed, not maintained as compatibility aliases.
- Each discovery target must be a card ID or `epilogue`. Each badge's `quest_id` must resolve to a story/discovery at that badge's grant card. Python derives screen indices, internal hrefs, popup paragraphs, and the ordered log. Invalid client target/position metadata restores the complete document.
- Complete absolute `stats_after` and cumulative `badges_after` snapshots.
- Region landmarks bounded to the shared `320 x 180` scene geometry.
- A separate `epilogue_scene` has exactly `region_id`, `art_key`, and five `positions`. The region/art are fixed to `san-jose` / `san-jose-home`; positions reject booleans, nonfinite values, and coordinates outside x `20..300`, y `0..180`. Its five positions must match the five rendered ending beats.
- Plain-text prose and facts only. Contextual links are selected by trusted template logic.

Validation rejects unknown/missing keys, booleans as integers, nonfinite/out-of-range coordinates, duplicate JSON keys/IDs, invalid source references, wrong counts/order, decreasing Experience, duplicate badge grants, unsafe links, symlinks, missing assets, and unapproved static files. Authored errors fail startup; they are never silently repaired in the browser.

**State Contract**

`prepare_story()` emits a prose-free inert projection:

```text
{
  schema_version,
  initial: {stats, badges, region_id, position, mood},
  epilogue_scene: {region_id, art_key, positions: [{x, y}]},
  events: [{id, chapter_id, region_id, position, mood, stats_after, badges_after}]
}
```

Jinja serializes it in the quoted `data-game` attribute with `tojson | forceescape`. The browser parses it with `JSON.parse`; no executable inline data or fetch endpoint is used.

`deriveState(game, eventIndex)` clamps only untrusted numeric test input to `-1..11` and returns a fresh object containing the selected absolute stats, badge prefix, region, mood, chapter object, and landmark. Runtime navigation supplies only bounded values:

- title: event index `-1`
- event screens: `0..11`
- epilogue: event index `11`

Dialogue beat position is local presentation state and never changes stats, badges, mood, or source data. Main events retain their authored region and landmark. The explicit ending exception selects the home scene/region and positions `(119,165)`, `(236,165)`, `(161,165)`, `(161,165)`, `(161,165)` for its five beats. `deriveState()` continues to supply the final stat snapshot at event 11; `renderState()` applies this visual-only route. Entering/leaving the epilogue invalidates the renderer's checkpoint cache through the existing screen-navigation path, so identical stat indices cannot leave stale art or captions behind. The DOM exposes current screen, beat, checkpoint, region, and scene-art identity for deterministic checks, not as a public API.

The journal is separate, page-local presentation state: `completedScreens` records screens 1-13 at their final beat; `foundDiscoveries` records actual popup openings. Both sets survive Back and log jumps for this visit and reset on reload. Chronological DOM order is derived from target screen order, with the story record before its optional discoveries and authored order for ties. It is not calculated from repository dates or invented age/year conversions. Grouped/overlapping periods retain their supplied labels.

| Story Screen           | Discoveries                    |
| ---------------------- | ------------------------------ |
| College                | `gec-extras`, `early-projects` |
| Automation / Pune      | `green-belt`, `coldplay`       |
| SJSU                   | `opportunity-hack`             |
| Google / during the MS | `masters`, `google-tools`      |
| Current work           | `career-titles`, `awards`      |
| Epilogue               | `off-clock`, `hobbies`         |

Every log entry has a validated target. Story entries revisit the first beat of their card; discovery entries reopen the original popup. Cached DOM-node identity plus the reached/found sets authorize enhanced jumps; a forged visibility class cannot unlock a destination. Jumps close the modal and restore the proper focus, without updating the URL/history. Fallback uses ordinary internal fragment links.

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
- the ending's in-flow home illustration, also present without JS and in print

Controls are present but hidden by base CSS. Initialization runs after the load event because WebKit can execute the module before applying CSS. Until then the full server document remains untouched, not covered by a loading gate; an image that never loads cannot hide the story. If JavaScript validates the stylesheet sentinel, projection, catalog unlock bounds, and matching DOM markers, it adds `.enhanced` and selects one game screen/beat. If parsing, validation, CSS, or initialization fails, every server-rendered section remains readable. Print overrides enhanced visibility and catalog filtering to expose all content.

JavaScript uses `textContent`, class changes, `aria-*`, `inert`, focus, and narrowly bounded SVG `transform` attributes. It does not use `innerHTML`, string-to-code evaluation, remote requests, runtime templates, or inline style strings. CSSOM writes are limited to the bounded chapter-progress width and validated numeric hotspot percentages. Discovery coordinates are within x `48..272`, y `48..132`; browser tests verify actual 48px target separation and popup bounds.

**Visual Layout**

Desktop uses a two-pane frame: landscape left, dialogue right, HUD above, controls below. Mobile uses four rows: HUD, landscape, dialogue, thumb controls. Both fit the usable viewport and include all safe-area insets.

Normal mobile targets:

- Minimum supported width: 320 CSS pixels.
- Controls: at least 48 CSS pixels high.
- Landscape: approximately 21-26dvh on mobile depending on viewport height, leaving room for persistent stats and dialogue. An aspect-ratio wrapper uses container dimensions to keep the window hit targets aligned with the actual SVG rather than the letterboxed panel.
- Dialogue: remaining flexible space; one paragraph beat normally fits without scrolling.
- Internal dialogue scrolling is allowed only for enlarged text, unusually short screens, or long optional overlays.
- No horizontal overflow, page scrolling, text shrinking, hidden overflow used to mask defects, or separate low-information mobile HUD.

The visual language remains cream paper, dark green ink, amber/rust accents, crisp pixel landscapes, system serif display type, monospace game labels, square borders, and stepped shadows. Dark mode follows `prefers-color-scheme` with no toggle/storage.

The scene uses original landscapes and factual building labels, not logos or copied architecture. Object markers are inanimate and decorative. The PLA block uses the original generic robot and “I'm 40% PLA.” without an explicit character voice cue. No copied franchise artwork is permitted.

**Motion**

- Scene object movement between authored landmarks uses a short stepped CSS transition.
- The home marker moves only on entering the epilogue or changing its authored dialogue position. No printer/server idle loop is added; the existing transition is disabled by reduced motion.
- A milestone's final dialogue beat uses one eight-logical-pixel object hop with static sparks, not a duplicate narrative reward block.
- The mosquito swoop lasts 1600ms at `unexpected-detour`; the pandemic-symbol sweep lasts 1800ms at `fog-arrives`. Each has one iteration, then rests as static art. No animation-end event is needed for navigation, cleanup, or state. Leaving removes the active animation; reduced-motion changes remove animation eligibility for the rest of that entry, preventing replay when the preference is restored.
- There is no requestAnimationFrame loop, idle movement, flashing, camera shake, sound, confetti, count-up, or queued animation.
- `prefers-reduced-motion: reduce` disables all transitions/animations immediately while preserving state and controls.
- Opening/closing overlays may use a brief bounded stepped transition, but initial page load must not flash a closed panel.

**Accessibility**

- Buttons are native `button type="button"` elements with explicit labels and at least 48px mobile targets.
- Noncurrent game screens and fallback-only duplicate headings/art are removed from the enhanced accessibility tree.
- Scene art and object SVGs are decorative; narrative equivalents are text.
- Numeric `n / 10` text is authoritative; pips do not carry meaning alone.
- Dynamic HUD is `aria-live="off"`; changing screens moves focus to the new heading.
- Closed Quest log content is inert and assistive-hidden. While open, the separate HUD, scene, story deck, and navigation surfaces are inert; the HUD remains visible above the overlay. Tab stays inside the dialog and Escape restores the actual trigger, not an assumed `activeElement`. A discovery popup is nonmodal, leaves dialogue visible, and restores focus to its window glint.
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
| Interaction      | Window discoveries, persistent HUD, exact Quest log completion/rewind, Escape/focus restoration, no branching mutation.        |
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
