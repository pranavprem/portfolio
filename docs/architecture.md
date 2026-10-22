**Portfolio Architecture**
Status: approved chapter-adventure design and current copy refinements published on `master`; exact-SHA browser verification and outstanding public-deployment gates are recorded in [handoff.md](handoff.md).
Prepared: 2026-09-06. Current revision: a short overview route with optional named topics and a chapter map. Owner: Pranav Prem. Canonical origin: `https://pranavprem.com`.

**Purpose**
This is a warm pixel-game autobiography, not a resume with animation beside it. The enhanced site is a full-screen, linear chapter adventure. The landscape, current chapter object, dialogue, discoveries, stats, milestones, and controls form one game scene. The complete human story, including uncertainty, illness, boredom, burnout, hobbies, and current joy, remains more important than game chrome.

The public repository is `https://github.com/pranavprem/portfolio`. The private source PDFs are not build inputs. Their owner-authorized, public-safe evidence is preserved in [story.md](story.md); do not reopen, serve, embed, or commit them.

**Core Decisions**

- Runtime remains Python 3.13, Flask, Jinja, Gunicorn, one local CSS file, one vanilla JavaScript module, local JSON, system fonts, and original SVG.
- The server renders every paragraph, fact, link, stat equivalent, milestone description, and optional highlight. JavaScript changes presentation and visibility; it does not construct prose.
- Enhanced mode owns the usable `100dvh` viewport. Document scrolling does not drive progression.
- The authored story remains chronological, but reading is not gated. Start/Next/Back, keyboard controls, and touch swipes move between chapter overviews; a chapter map allows direct visits. Named topics and window discoveries reveal detail without changing stats.
- Game state is selected from absolute authored snapshots. No additive XP logic, random state, URL state, cookie, local storage, session storage, database, or server mutation exists.
- Mobile is a first-class game layout with a scene, dialogue panel, and fixed thumb controls, not a compressed desktop essay.
- No living avatar, mascot, pet, or companion appears. Eleven original objects identify the chapters.
- No framework, game engine, canvas/WebGL dependency, runtime npm, CMS, analytics, remote font, embed, or remote runtime request is introduced.

**Experience Contract**

**Optional Detail Grouping**
The latest owner curation narrows the optional SJSU topic after its brief four-project expansion. Main-session design/review: keep the thirteen-stop route, three SJSU topic controls, all checkpoints, and journal/discovery counts. Random projects retains SpartanBot and Karma Mining, emphasizes the owner's enjoyment of Alexa skills/AWS Lambda serverless work, and names Heroku as his PaaS choice during SJSU. Remove CUSR/Dragonstone Pizzeria from runtime copy and the fixed link list, retaining their full source history. The overview still describes enterprise software, cloud technologies, and virtualization, with data mining on the side; project domains are not academic subjects.

The owner now identifies the 110% course as Prof. Paul Nguyen's Cloud Technologies class, covering Docker, Kubernetes, and AWS. Add that detail without inventing a grading mechanism, semester, or institutional record. Keep the TA/autograder/leaderboard paragraph. Opportunity Hack remains its own campus discovery with a result-led heading and explicit Alexa-powered City of San Jose work using AWS Lambda for serverless processing, plus the unchanged public project link. Preserve second place, not a win/first-place claim, and keep this project distinct from SpartanBot. Heroku's general PaaS preference does not assert where each project ran. No new date, current deployment, scale, or sole-authorship claim is needed.

Current-work prose explicitly says the owner works on Atlas, the reasoning engine behind Agentforce, while preserving AgentScript, the capability list, team tooling, and wages-versus-fun transition. His requested GitHub profile uses fixed ordinary anchors on the opening/ending screens. These are content/link corrections within the existing server-rendered model, not new topic controls, schema fields, remote requests, or security permissions.

The two retained SJSU project links are rendered from the template's fixed allowlist. A bounded Jinja macro partitions literal project labels in any order, recursively processing a strictly smaller trusted list and autoescaping every remaining text fragment. There is no raw HTML construction, `|safe`, Markdown parsing, new JSON link field, or client-generated prose. Tests cover multiple labels, arbitrary order, and hostile text, as well as the two omitted runtime links and the separately linked hackathon discovery.

The epilogue has exactly three topics: My house, My agents, and 3D printing. The last groups the existing printing paragraph, retail-therapy line, and original PLA portrait/joke in one `.dialogue-beat` container. They are not separate tabs, and the quote is not repeated in the overview. The overview still uses the ending summary's first sentence; the log may summarize printing as before. Coordinate Python/JS validation, projection, template controls, and independent fixtures to exactly three positions: `(119,165)`, `(236,165)`, `(161,165)`. Reject the retired five-position shape rather than adding a compatibility path. This is presentation grouping with unchanged final stats, artwork, and the 16-file runtime boundary.

**Reader-Controlled Pacing**
The owner reports that a friend stopped after college because the experience became verbose and repetitive, and requests a more intuitive, interactive redesign while retaining the content. The measured baseline has 36 mandatory dialogue screens; its existing thirteen story summaries contain 400 words. More animation would not remove that reading obligation. This revision deliberately supersedes paragraph-by-paragraph progression, not the biography, counts, snapshots, or privacy boundary.

Main-session design and review, using interaction, editorial, accessibility, and engineering lenses rather than claiming independent experts:

- Keep the title, twelve event screens, and epilogue. Each opens on a short overview using its existing `summary` (or original prose for a single-paragraph card). Next/Back always move one story screen, not one paragraph; the complete quick route takes thirteen advances from title to home. No detail interaction is required to continue.
- The initial pacing pass preserved every body/discovery; later owner-authorized content/grouping changes are documented above. Cards have `beat_labels`, one distinct plain-text label of 1-32 characters per paragraph. Named 48px buttons open those paragraphs individually; Back to overview restores the summary. These are reading choices, not biography branches. The ending's three topics use its three matching home positions, with arrival also serving the overview.
- The short route reuses summaries rather than creating another independent claim set. The home overview uses its summary's opening sentence; all printing copy/portrait stays together in the printing topic, not the overview. Overview copies and topic controls start hidden in server HTML and are enabled only after validation. No-JS, CSS/JS/projection failure, and print expose full prose/catalog, including grouped printing content. The full-copy 900-word budget remains; separately test the short route at no more than 550 narrative/title words.
- Add a Chapters overlay with thirteen server-rendered links derived from the existing story records. All are available immediately, including the later work and home chapters. Opening it, closing it, and following its links preserve focus and never update URL/history. A jump changes only the selected absolute snapshot; it does not record skipped chapters as visited or find their discoveries.
- The Quest log remains a separate visited/found journal with 24 records. A story record unlocks when its overview is visited; a discovery still unlocks only when opened. Back/jumps retain the page-local sets; reload clears them. This is navigation state, not a claim that a visitor read every word.
- Keep all five numeric/pip meters visible, but reduce HUD framing and decorative clutter. Use a more compact scene/card composition, a clear stop counter, meaningful chapter/topic labels, and a visible hint when the current landscape contains discoveries. Preserve original pixel art, cream/green/rust colors, system fonts, and reduced motion. No idle animation or fabricated mini-game is added.
- Topic selection is a bounded integer `-1` (overview) or an existing paragraph index. Cache and validate each topic button's DOM identity, screen, index, and `aria-controls`; reject missing/duplicate/out-of-range associations before enhancement. Cache chapter-map links against the thirteen derived story destinations. The stat projection remains version 2 and prose-free; no persisted-data compatibility path is needed.
- Chapters and Quest log share bounded modal handling below the HUD: only one is open, background surfaces are inert, Tab stays within the active overlay, Escape restores its actual trigger, and progression pauses while open. Headers/Close stay outside the scrollable `.overlay-body`, so closing never requires scrolling back to the top. Escape from a selected topic returns to its overview and topic button. Modified keys and interactive/editable targets retain normal browser behavior. Native buttons/links provide alternatives to gestures.
- Navigation and reveals never wait for animation or a network event. Invalid metadata leaves the complete document; before load the original server content remains visible. There is no new fail-closed waiting gate. Motion remains local and bounded; selecting topics does not replay chapter encounters or award extra stats.

Review acceptance: every original paragraph is reachable by a named control; thirteen advances reach home; unrestricted map jumps preserve exact stats and visit only their destination; all 24 journal targets remain correct; modal/focus/keyboard/touch behavior is consistent; all targets are at least 48px; mobile overviews fit at ordinary phone heights, while short/enlarged views can scroll internally. Verify both themes, forced colors, no-JS/failure/print, CSP, three engines, and the unchanged 16-file container boundary. A repeat human review is still needed to establish whether attention actually improves; automated correctness and a shorter route are not retention evidence.

**Cameo Placement Correction**
The owner explicitly places the Coldplay/Oxfam cameo during GEC, not HSBC. Main-session design/review: retarget `coldplay` to `college-unlocked` (screen 4), use `GEC / Coldplay & Oxfam`, and retain its prose, sources, and approved timestamped link. The old Profile age label remains historical evidence only; neither a replacement age/year nor a campus filming location is inferred. The existing derivation moves the journal entry before HSBC and returns to the GEC popup without new navigation logic, stats, counts, or required beats.

College now has three glints. Its original west/east wings are spread slightly so the cameo window `(191,100)`, GEC-extras window `(267,99)`, and unchanged early-projects window `(114.5,96.5)` preserve distinct 48px targets at 320x568. This is symbolic art geometry, not new campus or filming evidence. Acceptance covers three-target separation, found-only unlocks, Pune absence, return/focus/stats, source history, fallback/print, and all browser engines.

**Home Copy Revision**
The owner now describes the local-AI repositories as mostly defunct/not running and asks for a separate list-form hobby easter egg. Main-session design/review: remove `local-ai` and its OpenMemory/Qdrant/Neo Services links from runtime content; preserve their qualified source history. Keep `off-clock` for gaming and add `hobbies` at an original generic guitar `(264,113)`, leaving eleven discoveries and 24 journal records. No checkpoint, state, persistence, navigation rule, or network permission changes.

Add only optional discovery `list_items`: 1-12 distinct plain-text strings, each at most 100 characters, with paragraphs and list items together bounded to 600 characters. Existing paragraphs remain required. Reject invalid types, empty/duplicate items, controls, excess length, and unknown fields at startup. Jinja escapes a semantic `<ul>`/`<li>` after the paragraphs; no HTML/Markdown interpretation or client prose construction. The list remains complete in fallback and print, and its last item is "Making lists. You may have noticed." Review covers escaping, exact inventory, separate unlock/return targets, list order, mobile scrolling/focus/48px glints, enlarged text, and all engines.

The paid-work passage uses "For my wages, I build systems that connect..." rather than asserting enjoyment of corporate integration. "But for fun..." introduces the existing home projects, not new invented capabilities. Preserve the Agentforce technical scope, present enthusiasm, personal-agent/Morpheus account, and complete ending prose. The guitar is symbolic art, not an ownership, model, or skill claim.

**Home Scene Revision**
The home revision gives "DevOps, but it's my house" a San Jose scene rather than holding the Golden Gate/Salesforce artwork. Four regions, eleven chapters, twelve checkpoints, eleven milestones, and 24 journal records remain. Original `san-jose-home.svg` and validated `epilogue_scene` now provide three positions for the three ending topics. Overview/house uses the front path, agents the homelab, and printing the printer bench. This is a presentation-only exception, not another checkpoint or a mandatory tour.

The final stats/badges remain selected by event 11 through `deriveState()`. Rendering selects the home art, San Jose label, and authored marker position by the ending screen/beat. Back and Quest log jumps must restore the correct work/home scene while retaining the page-local journal. Existing stepped movement and reduced-motion behavior apply; add no idle animation, timer, or navigation gate. The two ending discoveries use the gaming monitor and guitar; the earlier server-rack discovery is retired by the copy revision above. Add the home illustration to no-JS/print output, startup asset requirements, the explicit Docker allowlist, and the 16-file runtime boundary.

The house and equipment are original symbolic art: generic home automation, servers, a gaming/simulator corner, and a printer. They are not a real facade, floor plan, address, device model, network topology, or NAS-location disclosure. No private photograph or configuration is needed. Acceptance covers correct home entry/return, each beat's visual position, unchanged final stats, discovery geometry/focus, reduced motion, malformed scene data, missing art, fallback/print, CSP/SVG safety, mobile fit, and the rebuilt container.

**Quest Log Revision**
The Quest log correction supersedes the old 21-item, newest-first catalog and timeline-only unlock rules. The owner explicitly chose to keep scene popups, include their summaries in the Quest log, avoid repeats elsewhere in the game, provide chronological summaries of the whole main story, and make each log entry revisit its original scene. That earlier task authorized its commit/push, not a production redeployment or blanket publication permission for later revisions.

Main-session design and review:

- Keep eleven chapters, twelve event snapshots, five stats, and the main route. Card `summary` and `epilogue_summary` produce thirteen story records alongside eleven discoveries, instead of an independent achievement catalog. Main summaries revisit the overview. The title's identity/Goa context is covered by the current-work and childhood summaries rather than inserting a present-day entry before childhood.
- Replace card `facts` and the old catalog with one authored `discoveries` collection. Each record owns its ID, target card (or `epilogue`), heading, period label, plain-text paragraphs, short summary, source references, reviewed links, and bounded scene position. Python prepares the popup and log from that one source. No fact may exist only in the log. The original catalog's degree, research, tool, metric, project, nomination, promotion, award, and hobby details remain in main prose or a discovery; the full ledger stays intact.
- Discovery targets: GEC extras, early games/CyanogenMod, and Coldplay at college; Green Belt/CI-CD at the Pune chapter; Opportunity Hack at SJSU; degree/research detail and concrete developer tooling during the MS/Google scene; promotions and awards at current work; gaming and a separate hobby list at the ending. Coldplay follows the owner's GEC correction, not the earlier age-based Pune placement. Do not invent a calendar date, replacement age, or filming location. Broad period labels remain broad. Grouped awards span the career and do not inherit the current chapter's year.
- Main summaries unlock on visiting their overview; discovery summaries unlock only when their popup is opened. Two bounded in-memory sets retain reached story cards and found discoveries for this page visit. Back/jump restores absolute stats without erasing the journal. Skipped map destinations are not marked visited. Reload resets it; no cookie, storage, session, URL progress, or server mutation is introduced. Discoveries never gate the main route or modify stats.
- Keep nonmodal scene popups, one open at a time, with visible dialogue, native 48px glints, Escape/Close, and exact trigger focus restoration. Multiple discoveries may share a screen; positions must not overlap at tested mobile sizes. Validated numeric positions use bounded CSSOM `left`/`top` values under the existing CSP.
- Remove repeated narrative reward blocks from the main scene, including Green Belt's spoiler. Keep the decorative milestone response and authored snapshot prefix. Milestone descriptions belong in the Quest log with the corresponding story/discovery record. The HUD rack remains decorative and its numeric count authoritative. Opportunity Hack exists once as a popup plus its summary, not in the main SJSU beat. Gaming and other hobbies likewise each have one ending discovery.
- Quest log headings are internal links in fallback HTML. Enhanced activation closes the log, moves to the target overview, and focuses its heading; discovery entries reopen the original popup. Only visited/found journal entries may navigate. The separate chapter map intentionally permits every validated story destination. External links remain separate. No whole-story-card click handler, URL/history update, animation wait, or arbitrary selector execution is added.
- Retain every popup and all 24 summaries in semantic server HTML, no-JS, invalid-data, CSS/script failure, and print output. Validate exact coverage, unique IDs, known targets, safe links, finite positions, sources, and text limits. The prose-free stat projection stays version 2; the coordinated internal authoring/DOM revision needs no compatibility layer because no content API or persisted progress exists.
- Acceptance: every prior catalog detail has a main/popup source; no repeated optional/reward prose; chronological order; found-only discoveries; main completion; jump/back/focus; retained journal on revisit; reload reset; invalid targets/positions fail safely; complete fallback/print; all browser engines, CSP, mobile target separation, and reduced motion. No new runtime dependency, route, file, or network permission is needed.

Persistent HUD stats, place-only captions, and bounded mosquito/COVID encounters remain. The Quest log overlays the game below the HUD; keyboard/swipe progression pauses while it is open. Observed verification status belongs in the handoff.

The game has fourteen screens in presentation order:

1. Title screen using the opening state.
2. Twelve event screens from eleven chapters; chapter 09 has two events.
3. Epilogue holding the final stats/badges while returning to the San Jose home scene.

Each event screen opens at overview selection `-1`. Single-paragraph cards show their original prose; other cards show their existing summary and named optional topics. Selecting a topic shows exactly its original paragraph without changing the checkpoint. Next and Back always move one screen and reset it to the overview. Reaching a screen records that moment and gives bounded milestone feedback if applicable, without a repeated reward paragraph. Title and epilogue bound the main route; the chapter map can select any of its thirteen story destinations.

College retains four distinct detailed beats (independence, Python/PyCon, hackathons, academic standing), now optional named topics rather than required slides. Department leadership, Zuari, and the paper remain a GEC discovery. Automation retains two detail topics; Green Belt/separate CI-CD remain a discovery. Snapshots and grant points are unchanged. Details and discoveries never gate main progression or mutate stats.

Each active glint opens its own discovery popup over the landscape while dialogue stays visible. Only one popup is open at a time; multiple glints on one screen retain distinct targets and focus. The five-stat HUD is always visible. Quest log shows reached story summaries and found discoveries below it. Escape closes an overlay and returns focus to the actual opener, including the epilogue's final button.

Supported enhanced inputs:

| Input                     | Behavior                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| Start / Next button       | Advance one story screen; open Quest log from the home overview or any home topic.           |
| Back button               | Return to the previous story screen at its overview.                                         |
| Right Arrow, Enter, Space | Same as Next when focus is not in an interactive/editable element and no modifier is held.   |
| Left Arrow                | Same as Back under the same guard.                                                           |
| Horizontal touch swipe    | Left advances; right rewinds after a 52px distance threshold and directional check.          |
| Named topic               | Show the selected detail and focus the reading; Back to overview restores the summary.       |
| Chapters                  | Open the unrestricted thirteen-stop map below the HUD.                                       |
| Window glint              | Toggle current scene discovery; the main next control returns to the story while it is open. |
| Quest log                 | Open a bounded overlay below the persistent HUD.                                             |
| Escape                    | Close the active overlay, or return from a topic to its overview, restoring trigger focus.   |

Wheel/trackpad movement is not progression input. Do not add wheel-to-advance, scroll-jacking, drag-only input, branching choices, combat, timers, skill checks, sound, saved progress, or browser-history entries per beat.

Approved ordinary links are the GitHub profile at `https://github.com/pranavprem`, curated GitHub work, LinkedIn, `mailto:pranavprem93@gmail.com`, and the timestamped Coldplay/Oxfam cameo. Links remain links, not whole-card targets or remote previews. Keyboard shortcuts yield while a link, button, form control, or editable element has focus.

**Story Map**

| Chapter          | Region        | Object          | Direction                                                                          |
| ---------------- | ------------- | --------------- | ---------------------------------------------------------------------------------- |
| `spawn`          | Goa           | controller      | PC games at seven and making small games at eight.                                 |
| `school`         | Goa           | backpack        | Computer science in 11th/12th grade, C/C++, house captain, public speaking/debate. |
| `detour`         | Goa           | compass         | Complicated dengue and hospital month before finals; route to GEC.                 |
| `college`        | Goa           | laptop          | Independent living, leadership, Python/PyCon, Zuari, paper, hackathons, academics. |
| `java-forge`     | Pune          | Java mug        | HSDI, six-month Java training, top-of-class result, leadership.                    |
| `automation`     | Pune          | automation gear | Boredom, TasKing, Green Belt savings, banking friction, US study.                  |
| `sjsu`           | San Jose      | books           | MS, 110%-to-TA account, grading tools, and optional project experiments.           |
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
- Cards own `summary` text and required `beat_labels`, one distinct 1-32-character plain-text label per paragraph; the root owns `epilogue_summary`. Discoveries own `id`, `card_id`, `heading`, `period_label`, `body`, `summary`, `position`, `source_refs`, and `links`, with optional bounded `list_items`. The old `facts`, `achievements`, `era`, and `unlock_after` fields are not compatibility aliases.
- Each discovery target must be a card ID or `epilogue`. Each badge's `quest_id` must resolve to a story/discovery at that badge's grant card. Python derives screen indices, internal hrefs, popup paragraphs, and the ordered log. Invalid client target/position metadata restores the complete document.
- Complete absolute `stats_after` and cumulative `badges_after` snapshots.
- Region landmarks bounded to the shared `320 x 180` scene geometry.
- A separate `epilogue_scene` has exactly `region_id`, `art_key`, and three `positions`. The region/art are fixed to `san-jose` / `san-jose-home`; positions reject booleans, nonfinite values, and coordinates outside x `20..300`, y `0..180`. Its three positions must match the three ending topic containers, not the number of text elements nested in printing.
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

Topic selection never changes stats, badges, mood, or source data. Main events retain their region and landmark. The ending selects home and positions `(119,165)`, `(236,165)`, `(161,165)` for its three topics; overview also uses the first position. `deriveState()` still supplies event 11's final snapshot, and `renderState()` applies the visual route. Entering/leaving home invalidates the existing checkpoint cache so the shared final numeric index cannot leave stale art/captions. DOM screen, topic, checkpoint, region, and art markers support deterministic tests, not a public API.

The journal is separate, page-local presentation state: `completedScreens` records screens 1-13 on visiting their overview; the name means reached, not proof that every note was read. `foundDiscoveries` records actual popup openings. Both survive Back/map/log jumps for this visit and reset on reload; jumps add only their destination. Chronological DOM order follows target screens, with story before discoveries and authored order for ties, not repository dates or age/year conversions.

| Story Screen           | Discoveries                                |
| ---------------------- | ------------------------------------------ |
| College                | `gec-extras`, `early-projects`, `coldplay` |
| Automation / Pune      | `green-belt`                               |
| SJSU                   | `opportunity-hack`                         |
| Google / during the MS | `masters`, `google-tools`                  |
| Current work           | `career-titles`, `awards`                  |
| Epilogue               | `off-clock`, `hobbies`                     |

Every log entry has a validated target. Story entries revisit the overview; discoveries reopen their popup. Cached identity and reached/found sets authorize journal jumps; a forged visibility class cannot unlock an entry. Map links have their own validated identities and intentionally need no prior visit. Jumps close the modal and focus the destination without updating URL/history. Fallback journal links remain ordinary internal links.

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

Controls are present but hidden by base CSS; previews, topics, and the map also start with native `hidden`. Initialization waits for load because WebKit can run the module before stylesheet application. Before that, the full server story remains readable with no loading gate. Enhancement requires the `reader-paced` stylesheet sentinel, projection, journal destinations, all map links, and topic index/control associations. Stale/missing CSS or invalid data keeps the original document. Print explicitly resets active/inspecting card height/display, restores original headings/paragraphs, and hides overview/map/topic UI, including when printing with a topic or overlay open.

JavaScript uses `textContent`, class changes, `aria-*`, `inert`, focus, and narrowly bounded SVG `transform` attributes. It does not use `innerHTML`, string-to-code evaluation, remote requests, runtime templates, or inline style strings. CSSOM writes are limited to the bounded chapter-progress width and validated numeric hotspot percentages. Discovery coordinates are within x `48..272`, y `48..132`; browser tests verify actual 48px target separation and popup bounds.

**Visual Layout**

Desktop uses a two-pane frame: landscape left, dialogue right, HUD above, controls below. Mobile uses four rows: HUD, landscape, dialogue, thumb controls. Both fit the usable viewport and include all safe-area insets.

Normal mobile targets:

- Minimum supported width: 320 CSS pixels.
- Controls: at least 48 CSS pixels high.
- Landscape: approximately 21-26dvh on mobile depending on viewport height, leaving room for persistent stats and dialogue. An aspect-ratio wrapper uses container dimensions to keep the window hit targets aligned with the actual SVG rather than the letterboxed panel.
- Story: remaining flexible space, with overview and topic choices fitting ordinary phone heights including 375x667 and 390x844. Topic rows use two-to-five columns where room permits; a full-width Back to overview control appears only after selecting a topic.
- Compact viewports at most 700px high and 760px wide use smaller card gutters and gaps, not smaller type, line spacing, or targets. Test the whole route with wider body fonts and wrapping serif headings; a title-only or macOS-only check misses later Linux overflow. All topic labels and the optional-reading prompt remain visible.
- Internal story scrolling is allowed for enlarged text, short screens such as 320x568, long optional topics, or overlays. The milestone count shares the location header; its decorative rack is omitted visually in enhanced mode, while all five stat bars remain visible.
- No horizontal overflow, page scrolling, text shrinking, hidden overflow used to mask defects, or separate low-information mobile HUD.

The visual language remains cream paper, dark green ink, amber/rust accents, crisp pixel landscapes, system serif display type, monospace game labels, square borders, and stepped shadows. Dark mode follows `prefers-color-scheme` with no toggle/storage.

The scene uses original landscapes and factual building labels, not logos or copied architecture. Object markers are inanimate and decorative. The PLA block uses the original generic robot and “I'm 40% PLA.” without an explicit character voice cue. No copied franchise artwork is permitted.

**Motion**

- Scene object movement between authored landmarks uses a short stepped CSS transition.
- The home marker moves only on entering the epilogue or changing its authored dialogue position. No printer/server idle loop is added; the existing transition is disabled by reduced motion.
- Entering a milestone screen uses one eight-logical-pixel hop on its selected object with static sparks, not a duplicate reward paragraph. Topic selection does not restart it; a motion-preference change disables reward/encounter replay for that entry.
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
- Closed Chapters/Quest log panels are inert and assistive-hidden. One may open at a time; background HUD, scene, story, and controls become inert while the HUD stays visible. Tab stays inside the active dialog and Escape restores its actual trigger, not an assumed `activeElement`. Opening a modal cancels a pending swipe. A discovery popup remains nonmodal, preserves story-panel geometry/reading position, and restores its glint. Topics focus the selected paragraph; Escape/Back to overview restores the summary.
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
- Paragraph-sized topics preserve the approved prose, but are now reader-selected rather than compulsory slides. A shorter mandatory route and an unrestricted map address the reported attention problem without adding game-like busywork.
- Optional facts became scene discoveries; the achievement appendix became a Quest log. Neither alters canonical state.
- Server-rendered fallback remains non-negotiable so content survives JavaScript, CSS, projection, print, accessibility, and archival failure modes.
