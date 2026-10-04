**Portfolio Architecture**
Status: approved design, implemented and locally verified. The documentation gate is delivered; NAS/public deployment and real-device checks remain open. Current evidence is in [handoff.md](handoff.md).
Prepared: 2026-09-06. Owner: Pranav Prem. Canonical origin: `https://pranavprem.com`.
Owner-approved PUBLIC repository: `https://github.com/pranavprem/portfolio`.

The design was reviewed before implementation and reconciled against the finished local app. The lead read both private PDFs under the owner's original explicit permission and preserved sanitized evidence in `docs/story.md`. Resume and Profile are `supplied-document` sources, not external or institutional verification. The originals are not public build inputs. The handoff records actual implementation, test, GitHub, and deployment status separately from the design targets below.

**Core Decisions**

- Build a small Python web application using Flask 3.1 or later, Jinja, and Gunicorn. Select a supported Python 3.13 patch release and pin tested dependency versions during implementation.
- Render the complete, semantic autobiography on the server. Vanilla CSS and one small JavaScript module enhance it into a game-like journey; they do not deliver or unlock otherwise inaccessible text.
- Use native vertical scrolling for the story. The current owner revision additionally allows reviewed GitHub/project links, LinkedIn, and the requested mailto link. No buttons, menus, forms, carousels, clickable whole cards/badges, downloads, custom keyboard controls, or horizontal scrolling. Dark mode follows device preference without a toggle or persistence.
- Curate 11 chapters in four original landscape regions. The journey ends with a continuing adventure, not a victory screen or contact call to action.
- Treat game state as a pure function of the current reading position. Absolute stat snapshots and cumulative badge prefixes make upward scrolling an exact rewind, including after large jumps and reload restoration.
- Use a sticky desktop theater with a top-right character sheet. On narrow screens keep the HUD compact and persistent, but put landscapes in the story flow rather than pinning a second large panel above the prose.
- Ship only local original SVG/pixel artwork and system fonts. No runtime npm, database, CMS, frontend framework, game engine, canvas/WebGL dependency, analytics, remote fonts, embeds, or runtime API calls.
- Deploy two services on the NAS: the application and `cloudflare/cloudflared`. Use a remotely managed tunnel. Docker Standalone/Portainer supplies authenticated stack variable `CLOUDFLARED_TOKEN`, which Compose maps only to cloudflared's supported `TUNNEL_TOKEN`; the app receives no credential. Publish no production host ports.

**Experience Contract**
The site should feel like opening a well-loved game cartridge containing someone's life: cream paper, forest-green ink, amber highlights, editorial typography, tiny inventory details, and landscapes with a sense of place. It is an autobiographical scroll essay with a game theater, not a resume inside a generic dashboard and not a game requiring instructions or skill.

The opening copy names Pranav Prem and establishes the premise: "A life in side quests." The instruction is "Scroll to explore. Up to rewind." It is plain text, not a start control. All scrolling methods supplied by the browser remain available: touch, wheel, trackpad, scrollbar dragging, arrows, Space, Page Up/Down, Home, and End. Native browser history, text selection, zoom, find-in-page, and assistive-technology navigation remain intact.

The current format is an 899-word main story (within five minutes at 180 wpm), followed by optional post-credits reading. Eleven chapters supply twelve stat checkpoints; chapter 09 has two cards. Independent beats remain separate: GEC's first paragraph introduces independent living, followed by six semantic list items; other cards use mini-paragraphs. Twenty-one compact bullet highlights follow the ending. Eleven actual achievement milestones appear at their story passages, with assistive descriptions, not a duplicate badge ledger. All reading is server-rendered; no text waits for motion or a click.

The presentation pass removes redundant chrome rather than hiding text: no masthead subtitle/edition, hero deck, chapter/world banners, player level/class, scene coordinates, or theater footnote. The HUD keeps its portrait, one chapter-status label, five meters, and milestone rack; scenery has one city caption. The original art, route, source links, state markers, and fallback equivalents remain. Compact bonus headings have secondary inline period labels and shorter summaries. Owner approval of the visual result remains separate from technical verification.

The latest owner narrative in `docs/story.md` supersedes original draft captions: opinions/public speaking/debate; complicated dengue and a hospital month a few weeks before Class 12 finals; GEC, SAP exposure, and seven hackathon miniboss wins; HSDI, Java training, a Rising Star nomination at 20, and banking red tape; hunger before GRE/TOEFL; 110%-to-TA and SpartanBot; Google's product culture, developer feedback and learning; San Francisco, smart colleagues and exploration; sustainable COVID contribution; Einstein Bots reliability/API/migration work; Copilot's configurable agent; Agentforce's Atlas/AgentScript/capability progression; and the return to San Jose for personal agents, the homelab, and printing. Do not restore detached résumé captions, make Slack the major Bots accomplishment, guarantee deterministic LLM output, expose confidential implementation, or restore rejected copy. The ledger retains prior accounts.

The emotional arc matters more than accumulating credentials: curiosity, confidence, an unwanted detour, independence, underused abilities, renewed challenge, discovering developer productivity, burnout, and renewed enthusiasm for useful automation. Humor belongs around machines and bureaucracy, not illness or burnout.

**Story Map**
The following copy is a direction for implementation, not a quotation attributed to the owner. Dates and claims must follow the provenance rules below.

| Chapter / ID          | Period / Region                                     | Reveal Direction And Supporting Content                                                                                                                                                                                                                                                                                                                     | Scene Landmark                                                                                                           |
| --------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 01 / `spawn`          | Childhood / Goa                                     | "The tutorial was a PC." PC games at seven; coding at eight. Start with tiny abilities and a disproportionately promising inventory. Omit birth year and inferred calendar years.                                                                                                                                                                           | A CRT-lit home beside palms and a shoreline path.                                                                        |
| 02 / `school`         | 2004-2010 / Goa                                     | "Small programs, bigger confidence." Navy Children School, C/C++, house captain, and the national top 0.01% Class 12 computer science result from Profile. Preserve the numeric claim with its supplied-document provenance, not an inferred exact rank.                                                                                                    | Naval-school-inspired courtyard, mast, chalkboard, and an original school building, without a copied crest.              |
| 03 / `detour`         | Weeks before Class 12 finals, 2010 / Goa            | "First boss: a mosquito." Complicated dengue and a month in hospital preceded the final exams by a few weeks. State the supplied timing plainly without treatment, accommodation, exact dates, or a comic illness reward. The next path leads to Goa University.                                                                                            | A forked monsoon path and a quiet shelter, not a monster battle.                                                         |
| 04 / `college`        | 2010-2014 / Goa                                     | "Learn to code. Learn to live." BE in Computer Engineering at Goa University, independent living, Python, and PyCon. Supporting lines cover the paper "A Transmission Control Tunnel for Datagrams," department general secretary, and an IEEE Xtreme national top-ten finish.                                                                              | An engineering courtyard, shared living space, Python-shaped abstract trail, and a paper kite.                           |
| 05 / `java-forge`     | Early HSBC chapter, within Aug 2014-Jan 2017 / Pune | "A surprisingly good Java tutorial." Joined HSBC, topped Java training, and grew into leading five engineers. Do not invent the month of the training result or leadership responsibility.                                                                                                                                                                  | A Pune courtyard office and a warm, mechanical training forge.                                                           |
| 06 / `automation`     | Later HSBC chapter, within 2014-2017 / Pune         | "Underused, not forgotten." Bank utilities stopped being challenging; TasKing and self-directed automation provided another route. The Lean Six Sigma Green Belt project saved 2,000+ hours. A GitHub adoption proposal was rejected; strong GRE/TOEFL results helped open the next route. No exact test scores or invented savings denominator.            | A paperwork mill being converted into a tiny conveyor workshop.                                                          |
| 07 / `sjsu`           | Jan 2017-Dec 2018 / San Jose                        | "Back on hard mode, happily." MS at SJSU, 3.90 GPA, cloud and enterprise systems, and work with Prof. Paul Nguyen. Include the owner's first-person account: "I scored 110%, the maximum possible. As I remember it, I was the only student to do so." TA tooling includes a Docker/Python autograder and leaderboard.                                      | A recognizable-in-spirit campus tower, library, and container-workshop courtyard.                                        |
| 08 / `developer-ally` | Jun-Aug 2018, during the MS / San Jose region       | "The best tool helps someone else build." Google Hardware/Nest internship: monitoring, testing, and engineering productivity. Discovering a love for helping developers is the central reveal. This is an interlude within the degree, not a job after graduation.                                                                                          | A nearby Silicon Valley hardware lab with test benches. Region grouping does not assert an exact office address or city. |
| 09 / `cloud-and-fog`  | 2019-2021 / San Francisco                           | Chat release automation, the monolith's data-center-to-AWS move, and freedom to explore with smart colleagues. A second card covers finding a sustainable COVID cadence, not an exhaustion monologue.                                                                                                                                                       | Original Salesforce Tower, then the same scene in quieter weather.                                                       |
| 10 / `bot-workshop`   | Later Salesforce / San Francisco                    | Einstein Bots: CI/CD/monitoring including Argo CD and 99.99% availability; public API; seamless migration of 100% of customer traffic from Heroku to multisubstrate public-cloud instances. Slack is a contribution within the API work. Then Copilot provides a configurable AI agent inside Salesforce. No invented dates, customer counts, or SLA scope. | Original helpful bots and a workshop.                                                                                    |
| 11 / `continuing`     | Agentforce / Present                                | Customers build agents; topics/actions evolved into Atlas Reasoning Engine and AgentScript for more deterministic behavior in an LLM world. Current capabilities include voice, MCP, native context/memory, agentic runtime, async work, and long-running turns/actions/sessions. Team tooling mirrors memory/context in a work assistant/coding harness.   | San Francisco career scene; the ending returns to San Jose for OpenClaw/Hermes/Morpheus, home automation, and printing.  |

The closing horizon and optional highlights follow chapter 11 without adding a chapter or duplicate milestone ledger. No employer logos, product screenshots, confidential systems, or implied employer endorsements are necessary to tell this story.

**Content Provenance**
Keep source status separate from narrative voice and from game fiction. First-person autobiographical wording is appropriate, but neither an owner account nor a supplied document implies independent verification. The owner explicitly authorized use of this story, including the 110%/sole-student account and Profile's national top 0.01% result; do not introduce another permission gate or replace these with vague copy.

| Source Or Claim                                                                                     | Status In This Draft                                     | Publication Rule                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Owner's timeline and personal reflections                                                           | `owner-supplied`                                         | Preserve the authorized first-person account and retain source references on every content card.                                                                                                                                                                                                                                                   |
| Resume                                                                                              | `supplied-document`, lead-extracted                      | The lead read it with the owner's permission. Use the sanitized evidence in `docs/story.md`; do not embed, serve, or commit the PDF or claim external verification.                                                                                                                                                                                |
| Profile                                                                                             | `supplied-document`, lead-extracted                      | The same boundary applies. Keep its claims distinct from Resume where they disagree.                                                                                                                                                                                                                                                               |
| Class 12 national top 0.01% CS                                                                      | Profile, `supplied-document`                             | Include the national top 0.01% Class 12 computer science result. Do not equate it with an exact first-place rank or invent an exam board, score, or comparison population.                                                                                                                                                                         |
| IEEE Xtreme rank                                                                                    | Profile says seventh; Resume says eighth                 | Publish "national top ten," not either exact rank. Retain both source claims in the sanitized disagreement ledger.                                                                                                                                                                                                                                 |
| Salesforce joining month                                                                            | Profile says January 2019; Resume says March 2019        | Publish `2019`. Retain the disagreement without inventing an explanation.                                                                                                                                                                                                                                                                          |
| SJSU GPA and dates; Google and HSBC date ranges                                                     | Lead-extracted supplied-document facts                   | Use the stated values and source mapping in `docs/story.md`. Do not invent a specific PDF attribution when the extract does not identify one, add precision, or round 3.90 upward.                                                                                                                                                                 |
| Prof. Nguyen's course result                                                                        | `owner-supplied`: 110%, maximum possible, sole student   | Include in first person as the owner's account/recollection. Do not suppress the number or uniqueness claim, invent the grading mechanism, or upgrade it to an institutionally verified or all-time record.                                                                                                                                        |
| Java training topper, five engineers, 2,000+ hours, Chat months-to-minutes, Principal February 2025 | Supplied-document facts, alongside the owner's narrative | Preserve scope and claim-level sources from `docs/story.md`. The hours belong to Green Belt, not TasKing or automation combined. Do not add annual savings, revenue, unsupported titles, or performance multipliers.                                                                                                                               |
| Bots availability/API/migration; Copilot/Agentforce evolution                                       | Latest `owner-supplied` account                          | Scope 99.99%, Argo CD/CI/CD/monitoring, public API, and the 100%-traffic Heroku-to-multisubstrate migration to Einstein Bots. Treat Slack as supporting API work. Preserve product progression and named public concepts without inventing dates, measurement windows, customer counts, confidential mechanics, or deterministic-model guarantees. |
| GRE/TOEFL                                                                                           | Strong results supplied; no approved exact scores        | Publish qualitative wording only.                                                                                                                                                                                                                                                                                                                  |
| Illness and work cadence                                                                            | Owner-supplied, explicitly revised                       | The owner now places complicated dengue and a month in hospital a few weeks before Class 12 final exams, with a mosquito boss-fight title. Include that account, not the superseded after-finals timing or invented dates/treatment/accommodations. COVID is sustainable contribution, not a burnout monologue.                                    |
| Stats, chapter objects, scene names, and invented badge titles                                      | `game-fiction`                                           | Clearly describe these as playful narrative meters and symbols, not medical measurements, official awards, or objective assessments of ability.                                                                                                                                                                                                    |

The private PDFs remain local and must not be modified, embedded, served, or committed. Continued implementation should use the sanitized story rather than require another PDF read. Future `.gitignore` rules must exclude PDFs case-insensitively, secret files/directories, `.env` files except a sanitized example, private notes, and development artifacts. `.dockerignore` must be an allowlist, not merely a list of the two current filenames. Public-repository approval is not permission to publish the private source documents or credential files. Before any first commit, inspect the intended staged file list and scan only the intended public artifacts for secrets.

**Art Direction**
Use a warm cartridge/editorial language rather than generic rounded SaaS cards. Suggested tokens are paper `#F6EEDB`, ink `#183C30`, amber `#D79832`, clay `#B96648`, and fog `#9AA99B`. These are design inputs, not a claim of verified contrast: test actual pairings. Use ink for small text on cream or amber; do not use amber as low-contrast body text on cream.

- Headings: a large system serif stack such as `Iowan Old Style, Palatino Linotype, Book Antiqua, Georgia, serif`, fluidly sized with `clamp()` and permitted to wrap.
- Body: readable system typography, 18px desktop and 17px on phones, 1.75 line height, and a desktop prose column capped at `32rem`. More space between chapters, not smaller body text, separates the beats.
- Details: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`; use pixel-like borders, segmented stat pips, labels, and stamped inventory slots. Do not use a pixel font for paragraphs.
- Composition: asymmetric editorial text beside a generous landscape. Cream gutters, light panel borders, restrained amber accents, and generous separation between columns. Avoid redundant frames and labels as well as glassmorphism, neon gradients, simulated browser windows, or a wall of identical cards.
- Art: four original SVG landscapes on a shared approximately `320 x 180` logical grid. Combine isometric buildings with a side-view walking path. Use a limited palette, integer-aligned edges, stepped silhouettes, and `shape-rendering="crispEdges"` where appropriate. Raster sprites, if used, get `image-rendering: pixelated`.
- Geography: Goa has shore, palms, NCS with its elephant, and GEC's smaller campus buildings; Pune has courtyard offices and an automation mill; San Jose has campus and a nearby hardware lab; San Francisco has Salesforce Tower, water, workshops, and a bridge. The old `bay-area` key/file remains an opaque identifier, not a second display name. These are illustrations, not precise personal locations.
- Objects: use no living avatar or companion. Eleven original pixel objects identify the current chapter: controller, backpack, compass, laptop, Java mug, automation gear, books, toolkit, cloud terminal, bot console, and agent nodes. Keep a consistent 32 x 32 logical footprint and the existing green/amber/rust palette; do not import brand or franchise assets.
- Motion: position-derived route interpolation, a one-pixel object step, and short local hops only. No autonomous bobbing, flashing, camera shake, confetti, sound, or time-based idle loop. The landscape remains still when scrolling stops.

Store original art sources publicly and document authorship/licensing in the README. Company names are factual text, not imported logos or endorsements. The owner specifically requested short signs on the buildings: NCS, GEC, HSBC, SJSU, Google/Nest, and Salesforce are original SVG text using a local system font. Semantic institution/region names also remain in HTML. Do not replace narrative information with art-only text.

The approved Coldplay/Oxfam cameo is an ordinary timestamped link only. Do not fetch a YouTube thumbnail, embed an iframe/player, or copy the Gmail silhouette into the runtime. The user's identification and public video metadata are recorded in the source ledger. The Bender/Futurama reference remains text in an originally styled blockquote; a tiny original generic pixel robot may accompany it. Do not use the rejected recognizable-character PNG, remote meme imagery, or copied franchise art.

**System Design**
The implementation should fit into a few small files. Do not introduce service/repository layers, a plugin system, a generic animation engine, or a schema framework for one static story.

```text
Browser
  | HTTPS GET / and /static/...
Cloudflare edge: DNS, TLS, HTTPS redirect, ordinary asset caching
  | encrypted outbound-established tunnel
cloudflared container [origin network + egress network]
  | HTTP http://portfolio:8000 on the private origin bridge
Gunicorn -> Flask -> validated local story JSON -> Jinja HTML

Browser HTML -> CSS presentation
            -> local JS reads inert game data + document geometry
            -> pure checkpoint selection
            -> HUD / badge slots / SVG attributes / card accents

No scroll information or game state returns to the server.
```

Implemented layout; developer tooling and CI are also mapped in the README:

```text
app/
  __init__.py              create_app, routes, configuration, headers, errors
  content.py               load/validate story; prepare public snapshots
  content/story.json       reviewed public story and game data only
  templates/base.html      semantic shell, local resources, metadata
  templates/index.html     story, theater, HUD, chapter snapshots
  templates/error.html     small shared static error presentation
  static/story.css         layout, cartridge styling, responsive/reduced motion
  static/story.js          pure state selector plus small browser controller
  static/art/              four landscapes, PLA robot, and favicon; chapter objects inline in Jinja
tests/
  test_content.py          content contract, provenance, snapshot expectations
  test_http.py             routes, headers, escaping, safe static serving
  test_browser.py          real JS, scrolling, accessibility and layout checks
requirements.txt          exact runtime dependencies, including transitives
requirements-dev.txt      test/lint tools, not copied to the runtime image
pyproject.toml            small test/lint configuration, no packaging ceremony
Dockerfile
compose.yaml              hardened app and origin network
compose.tunnel.yaml       production connector, egress network, protected token mapping
compose.local.yaml        explicit loopback-only local override
.gitignore
.dockerignore
AGENTS.md                 canonical contributor instructions
CLAUDE.md                 short entry point to AGENTS.md
README.md                 detailed setup, editing, testing, deployment runbook
docs/architecture.md
docs/story.md              existing complete sanitized narrative/source ledger
docs/handoff.md            actual implementation/test status and next steps
docs/retrospective.md      brief evidence-based learnings
```

`content.py` uses the standard library JSON loader and explicit validation, with one `ContentValidationError` type. `create_app()` loads content and compiles templates at startup. Routes do not reread files or call any service on every request. Two Gunicorn synchronous workers are a modest starting point; there is no streaming, async workload, scheduler, or background task.

`story.js` may export a pure `deriveState()` function for browser-based tests. Keep initialization, geometry measurement, state selection, and DOM rendering as a handful of small functions in that module. Split it only if implementation demonstrates a real second responsibility that cannot stay readable. Do not add a state-management package or a separate JS testing runtime.

**Documentation Contract**
Documentation is a required public handoff, not optional polish or a new runtime feature. All seven files below now exist. The repository is initialized on `main` and the public GitHub remote has been created; the handoff records publication/check outcomes. Keep each document's responsibility clear.

| File                                    | Availability / Required Content                                                                                                                                                                                                                                       |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md`                             | Available. Canonical contributor instructions, required reading, product/source/security invariants, checks, working discipline, and completion gate.                                                                                                                 |
| `CLAUDE.md`                             | Available. Thin entry point to `AGENTS.md`, not a competing policy.                                                                                                                                                                                                   |
| `README.md`                             | Available. Detailed local/testing/editing/deployment/recovery runbook, configuration, privacy, file map, and art attribution. Distinguishes procedures from observed results.                                                                                         |
| [docs/architecture.md](architecture.md) | Available. Technical design, contracts, decisions, validation plan, and required documentation/completion gate. Keep actual test results in the handoff rather than presenting design targets as measured results.                                                    |
| [docs/story.md](story.md)               | Available. Complete sanitized narrative, chronology, emotional arc, human/project inventories, source classifications, and disagreements, not merely the short website copy. Preserve this existing context when curating the 11 chapters; no chat or PDF dependency. |
| `docs/handoff.md`                       | Available. Actual results, environment/coverage, corrections, decisions, publication/deployment status, and next steps. No secrets or unearned deployment claims.                                                                                                     |
| `docs/retrospective.md`                 | Available. Evidence-based lessons and remaining verification limits; no additional process machinery.                                                                                                                                                                 |

Read order: `AGENTS.md`, `README.md`, `docs/architecture.md`, `docs/story.md`, `docs/handoff.md`, then `docs/retrospective.md`; `CLAUDE.md` points into that order. Approved source/numeric-claim and all-low opening-stat decisions supersede older draft omission suggestions. Owner-supplied chronology is not document corroboration. Use the story for the complete biography/disagreement ledger, this file for technical contracts, and the handoff for observed delivery status; do not shorten the full source narrative to the runtime selection.

**Completion Gate**
Another session must be able to continue from the public project alone, without the conversation or private PDFs. Before marking the implementation complete:

1. All seven documentation files above exist with substantive, mutually consistent content and working relative links; no required section is a placeholder. The canonical instructions and README make the next reading/editing/testing steps discoverable.
2. `docs/story.md` retains the complete sanitized account and source disagreements. Selected website claims keep their provenance, including Profile's top 0.01%, the owner's 110%/sole-student recollection, IEEE top ten, and Salesforce `2019`.
3. README commands match the actual files and let a fresh checkout run and test locally without PDFs or Cloudflare credentials. Deployment prerequisites remain explicit rather than fabricated as already provisioned.
4. `docs/handoff.md` records actual test commands/results, failures and unrun checks, known blockers, repository/deployment state, and exact next steps. `docs/retrospective.md` records brief learnings from completed work. No unrun browser, accessibility, container, or NAS check is labeled passed.

The local documentation, content, HTTP, browser, and container gates have recorded evidence in the handoff. Actual NAS/public transport, physical-device/screen-reader checks, representative mobile timing, and production recovery are still release/operator gates; they are not implied by a green local suite.

**Content Contract**
Use `schema_version: 2` for authored content and the inert game projection. This release replaces six stats and fictional badge names with five stats and actual milestones. There is no persisted data to migrate. Unknown client versions or malformed projections disable the live HUD and preserve readable HTML. Authoring order determines chapters/events; period labels do not manufacture timestamps.

| Field              | Contract                                                                                                                                                                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `schema_version`   | Exactly integer `2`; reject old/unknown versions rather than adding a speculative migration layer.                                                                                                                                                                                   |
| `sources`          | Map of public source IDs to `{kind}`: `owner-brief` is `owner-supplied`; `resume`, `profile`, and `supplied-documents` are `supplied-document`. Use the last only where the lead extract does not identify a specific PDF. No raw PDF content, private paths, or confidential notes. |
| `stat_definitions` | Ordered list of `{key, label, compact_label, description}` for exactly the five keys below.                                                                                                                                                                                          |
| `initial`          | `{stats, badges, region_id, landmark_id, mood}`: full five-stat map, no earned milestones, Goa opening landmark, and `bright` mood.                                                                                                                                                  |
| `badges`           | Ordered list of `{id, label, description, art_key}`. Unique IDs; names are game symbolism unless they directly name a supplied role.                                                                                                                                                 |
| `regions`          | Ordered list of `{id, label, art_key, width, height, landmarks}`. IDs are `goa`, `pune`, `san-jose`, and `bay-area`; `landmarks` maps IDs to `{x, y}` coordinates inside the SVG viewBox. Coordinates are artwork geometry, not geographical data.                                   |
| `chapters`         | Eleven ordered records: unique `id`, `region_id`, `period_label`, `heading`, and ordered `cards`. One card each except two in chapter 09.                                                                                                                                            |
| `cards`            | Unique `id`, `heading`, plain-text `body`, zero to three plain-text `facts`, `source_refs`, and one `event`. No raw HTML, Markdown execution, links, or template expressions.                                                                                                        |
| `event`            | `stats_after`: a complete integer map; `grant_badges`: zero or more known unique IDs; `landmark_id`: a known landmark in the chapter region; `mood`: an allowlisted art state such as `bright`, `quiet`, or `fog`.                                                                   |

Example of one complete chapter record within the larger document:

```json
{
  "id": "automation",
  "region_id": "pune",
  "period_label": "Later HSBC chapter / 2014-2017",
  "heading": "Underused, not forgotten",
  "cards": [
    {
      "id": "automation-unlocked",
      "heading": "Make the repetitive part disappear",
      "body": "The bank utilities stopped stretching me. Automation became a way to make the work more useful.",
      "facts": [
        "The Lean Six Sigma Green Belt project saved 2,000+ hours.",
        "A proposal to adopt GitHub was rejected.",
        "Strong GRE and TOEFL results helped open the next route."
      ],
      "source_refs": ["owner-brief", "supplied-documents"],
      "event": {
        "stats_after": {
          "coding": 6,
          "enthusiasm": 3,
          "vitality": 7,
          "charisma": 6,
          "experience": 4
        },
        "grant_badges": ["green-belt"],
        "landmark_id": "automation-mill",
        "mood": "quiet"
      }
    }
  ]
}
```

At startup, validate exact required keys/types, bounded text lengths, IDs matching `[a-z][a-z0-9-]*`, uniqueness, source references, region/landmark references, badge grants, and all stat ranges. Limits: 128 KiB for the JSON file, 64 characters for IDs/labels, 100 for headings, 600 for each body, and 220 for each fact/description. Reject booleans where integers are required. Enforce exactly 11 chapters and this release's card/badge counts; additions require coordinated schema/template/test changes. Reject nonfinite coordinates, coordinates outside the viewBox, unknown mood/art keys, and missing referenced assets. A malformed public content file is a deployment error, not something the browser should guess how to repair.

Each event is identified by its card ID and flattened in chapter/card order. Python derives a complete `badges_after` prefix for each event from all grants through that event. A badge can be granted only once in the story. The public game projection is `{schema_version, initial, events}`. Its initial state is `{stats, badges, region_id, position: {x, y}, mood}`; each event is `{id, chapter_id, region_id, position: {x, y}, mood, stats_after, badges_after}`. Resolve landmarks to bounded coordinates on the server. The projection excludes prose and source-review notes. The same prepared records supply semantic per-card stat summaries, badge text, and the HUD.

Serialize this small projection into a quoted inert HTML data attribute using Jinja's `tojson | forceescape` combination, for example `data-game="{{ game_payload | tojson | forceescape }}"`. Read it with `JSON.parse(element.dataset.game)`. Never hand-build JSON or interpolate it into JavaScript source. The only script element loads the local module via `src`; there is no inline executable script or JSON-fetch endpoint. The browser defensively validates the projection and its correspondence with DOM marker IDs before enabling the live HUD.

**State Contract**
The root `achievements` list is separate from stat events. Records have `{id, era, period_label, heading, body, source_refs, links}` and a 1-64 entry bound; the current regression set contains 21 grouped highlights. Sort by the documented newest-first era order, retaining authored order within an era. Undated items are separate, not assigned GitHub-derived biography dates. `links` maps at most three bounded labels to owner GitHub URLs, the exact forcedotcom contribution URL, or `https://youtu.be/ogItgrO9GSg?t=221`. Root sources include catalog-only `github: {kind: public-repository}`. Main cards retain their original biographical source IDs. This is not institutional verification or a security audit of linked projects.

Main `body` allows exactly `\n\n` between one to eight nonempty paragraphs, within 600 characters total. This permits seven independent GEC beats without merging unrelated events. The template renders the six beats after GEC's opening paragraph as a semantic list, with no extra checkpoints or authored markup. Other controls, empty paragraphs, and bad types are rejected. Projection prepares escaped paragraphs/contextual links; no raw HTML, executable Markdown, `Markup`, or `|safe` is introduced.

The catalog, notes, and links render in the first HTML response, outside the short story's ending. They are not fetched at runtime, hidden behind controls, or included in the game projection. The template includes the separately owner-authorized LinkedIn and email/mailto links. No new mutable route, remote asset, or persistence is introduced.

Stats use integers from 0 through 10 in fixed order. Display `value / 10` plus decorative segmented pips. The owner removed the introductory disclaimer; the fictional interpretation stays in contributor documentation, not a replacement lecture in the UI.

| Key          | Full / Compact Label | Fictional Interpretation                                                                                                                             |
| ------------ | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `coding`     | Coding / Code        | How stretched and actively exercised the coding muscle feels in this chapter. A dip is not forgotten knowledge.                                      |
| `enthusiasm` | Enthusiasm / Spark   | Appetite for the current quest, not a claim about a clinical condition.                                                                              |
| `vitality`   | Health / HP          | Available adventure energy. "Enough battery for another side quest" is appropriate; medical claims are not.                                          |
| `charisma`   | Charisma / Charm     | Confidence collaborating, teaching, and leading.                                                                                                     |
| `experience` | Experience / XP      | Accumulated engineering/life experience. Absolute, bounded, and nondecreasing through authored time; not years or a claim that learning is finished. |

These are the retuned version-two snapshots, explicitly game balance. The owner's latest correction asks for humility and room to grow: the final sheet is Coding 8, Enthusiasm 10, Health 8, Charisma 7, Experience 7, with only Enthusiasm full. Earlier Charisma/Experience and post-SJSU Coding are rebalanced rather than manufacturing a loss of ability in the final chapter. Experience remains nondecreasing. Illness and workload may lower energy without erasing skills, charisma, or accumulated experience; COVID reflects a sustainable adjustment rather than a collapse. Coding still reaches 10 at SJSU as previously requested, a historical peak in coding intensity rather than mastery. The schema and state-selection rules are unchanged. Any future rebalance must update this table and the independent tests together.

| Checkpoint                | Coding | Enthusiasm | Health | Charisma | Experience | New Milestone                                                |
| ------------------------- | ------ | ---------- | ------ | -------- | ---------- | ------------------------------------------------------------ |
| Opening                   | 0      | 1          | 1      | 1        | 0          | None                                                         |
| `first-script`            | 1      | 6          | 8      | 2        | 1          | `first-game`: First game                                     |
| `school-unlocked`         | 3      | 8          | 8      | 5        | 2          | `house-captain`: House Captain                               |
| `unexpected-detour`       | 3      | 5          | 3      | 5        | 2          | `cs-percentile`: National top 0.01%, for the academic result |
| `college-unlocked`        | 6      | 9          | 7      | 6        | 3          | `hackathon-wins`: 7 hackathon wins                           |
| `java-unlocked`           | 7      | 8          | 7      | 6        | 4          | `java-training`: Java training #1                            |
| `automation-unlocked`     | 6      | 3          | 7      | 6        | 4          | `green-belt`: Green Belt: 2,000+ hours                       |
| `sjsu-unlocked`           | 10     | 9          | 8      | 7        | 5          | `teaching-assistant`: Prof. Paul's TA                        |
| `developer-ally-unlocked` | 8      | 10         | 8      | 7        | 5          | `google-internship`: Google Hardware/Nest intern             |
| `cloud-unlocked`          | 8      | 9          | 8      | 7        | 6          | `release-automation`: Months to minutes                      |
| `fog-arrives`             | 8      | 7          | 6      | 7        | 6          | None; mood is now `quiet`                                    |
| `bots-unlocked`           | 8      | 9          | 7      | 7        | 6          | `bots-reliability`: Bots at 99.99%                           |
| `continuing-unlocked`     | 8      | 10         | 8      | 7        | 7          | `principal`: Principal engineer                              |

There are twelve checkpoints and eleven actual milestones across eleven chapters. Card and milestone IDs are separate namespaces. The opening is exactly `0, 1, 1, 1, 0`, not a childhood health assessment. Experience never decreases. The academic result is granted where it is stated, never as a prize for being ill. Automancy/Side Quests and invented milestone titles are retired; no compatibility aliases or duplicate end-of-page badge ledger remain.

Absolute `stats_after` snapshots, not additive deltas, are authoritative. If a small `+3` or `-2` annotation is desired, calculate it as the difference between adjacent authored snapshots; never apply it to the current DOM value. Do not silently clamp invalid authored stats: reject them at validation. Only numerical scroll interpolation is clamped.

At checkpoint `k`, display its five stats and complete `badges_after` prefix. Prefix counts, including opening, are `0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 10, 11`. Rewinding removes later grants; re-entry never duplicates a milestone. Client validation also rejects non-prefix grants and decreasing Experience. Nothing is persisted in cookies, browser storage, URL parameters, or sessions.

**Scroll Contract**
Checkpoint geometry belongs to the readable document, not a synthetic scroll timeline or a percentage of the whole page. There is one untransformed in-flow marker at the top of each reveal card, directly associated with its heading. Markers remain in the same DOM order as the flattened events. Do not use the sticky theater, changing badge height, or animated transforms to measure story progress.

Definitions, all in CSS pixels:

```text
H       = document.documentElement.clientHeight
S       = max(0, document.scrollingElement.scrollHeight - H)
y       = clamp(window.scrollY, 0, S)
T       = 16 on desktop;
          mobile HUD bottom + 12 when the dock is fixed;
          16 when using the nonfixed accessibility fallback
F       = T + 0.35 * (H - T)
C       = y + F
A[i]    = marker[i].getBoundingClientRect().top + window.scrollY
k       = greatest i for which A[i] <= C, or -1 if none
stats   = initial.stats if k == -1 else events[k].stats_after
badges  = [] if k == -1 else events[k].badges_after
```

`F` is the reading line, 35% down the unobscured reading area. Equality belongs to the later checkpoint. There is no direction-dependent hysteresis, "once" flag, accumulated XP, velocity, random input, wall clock, or previous-state dependency in this decision. Twelve markers need only a short linear scan, not an index library.

`A` must be strictly increasing. If geometry is unavailable, invalid, or mismatched with content, do not activate the enhancement. Make the opening section approximately at least `70svh` tall and keep the first marker below the initial reading line. Give the last card/closing horizon at least one small viewport of combined content and breathing room after its marker so the final checkpoint can reach the reading line. Test `A[0] > F` at the top and `A[last] <= S + F` at the bottom. Do not paper over unreachable endpoints with special-case "End means final" state that disagrees with the visible card.

Between checkpoints, presentation may use:

```text
u = clamp((C - A[k]) / (A[k + 1] - A[k]), 0, 1)
```

When the next checkpoint shares a region, interpolate the chapter object between the two authored landmark coordinates. Round positions to the artwork's logical pixel grid. Movement frames use `floor(u * 12) % 4`; odd frames add a one-pixel vertical step. Rewinding therefore runs the exact same visual frames backward. Between different regions, hold at the current landmark and cut to the next region/object at its checkpoint. Before the first and after the last event, hold the relevant object. A region cut is enough; do not build a camera-transition framework.

All discrete state, including mood and chapter object, is selected by `k`. Values and badges change immediately, without count-up tweens, spring effects, or delayed toasts. Reduced-motion mode keeps discrete changes but uses a static object at the current landmark and no interpolation or movement frames.

Achievement reactions use 32 separately measured rows: eleven story-badge rows and 21 catalog groups. Select the latest preceding row and normalize distance over the lesser of 180 CSS pixels or the next interval. Object lift is `round(sin(pi * phase) * 8)` logical SVG pixels with two static sparks while phase is below one; the matching compact-HUD object lifts by at most three pixels. Every pose remains a pure function of reading position. Rewinding gives the same pose; no timed queue or idle loop exists. Reduced motion clears reactions and movement immediately. These rows never mutate stats or grant extra badges.

Browser controller lifecycle:

1. Load the module normally with `type="module"`; parse the inert projection, bind existing nodes, and validate the marker/event mapping. CSS and HTML already provide a readable fallback.
2. Establish the responsive HUD reservation before measuring markers. If enabling dock mode changes layout, keep the live sheet concealed until a second measurement/derivation uses that final layout. Read geometry, derive state, then write the DOM; only after successful initialization label the HUD as live. Never calculate a fixed dock's clearance from its former normal-flow document position.
3. A passive document `scroll` listener marks work pending and schedules at most one `requestAnimationFrame` callback. This batches reads/writes with paint; it is not claimed to throttle events to a lower frequency. Do not run an idle animation loop.
4. Ordinary scrolling uses cached marker positions and reads the current scroll offset. Update text and badge attributes only when `k` changes; update bounded SVG presentation attributes only as needed. Never change the natural height of a story card as a side effect of becoming active.
5. Mark geometry dirty on window resize, relevant `visualViewport` resize, document-font readiness, and `ResizeObserver` notifications for the story/HUD. Recalculate after images load, with intrinsic dimensions already reserved. If ResizeObserver is unavailable, use resize/load fallbacks.
6. Re-derive on `pageshow`, including bfcache restoration, and on returning to visibility. Respect the browser's default scroll restoration; do not scroll to zero. A drag from top to bottom, a native fragment jump, or find-in-page must work without visiting intermediate checkpoints.
7. A reduced-motion preference change updates the rendering mode immediately without resetting the current state. Resize/reflow derives state from the new reading geometry, not from an old chapter percentage.
8. On an initialization or controller failure, remove live/enhanced state, cancel pending work, and leave the complete readable story and per-card snapshots. Reset the sheet to the opening snapshot with its static caption, or hide the live sheet if resetting fails; never label stale mid-story values as opening or current stats. Show only a short static fallback note, not a modal, spinner, or mandatory retry control.

Do not call `preventDefault()` on wheel, touch, or keyboard events. The owner-approved side-arrow alias may call `scrollBy` for an unmodified Right/Left key, using a smooth fixed 40px down/up step so existing reading-position-derived object movement responds with the same feel as native arrow scrolling. Reduced motion makes this step immediate. The alias must ignore editable controls and disable itself when the document has real horizontal overflow. Apart from that narrow alias, do not set scroll positions, change `history.scrollRestoration`, add mandatory scroll snap, enable smooth scrolling, move the document with transforms, or create an internally scrolling game container. IntersectionObserver may be used for an optional cosmetic optimization, but its callbacks are not the source of truth for state.

**Responsive Layout**
Use one document scroller. Base HTML/CSS is a complete story with a static character-sheet caption and in-flow illustrations. Determine column widths before JS runs. The owner's snapshot-removal revision makes stat equivalents assistive-only with enhancement; measure the final enhanced geometry, and remeasure if fallback restores their footprint. Do not change a card's height when it becomes current.

| Mode                                         | Layout And Clearance Contract                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| At least `64rem` wide with sufficient height | A two-column story/theater grid. The prose column uses `minmax(0, ...)`; the theater column has a top-right HUD row and a separate landscape row below it. The theater wrapper uses `position: sticky`, `top: 1rem`, and `align-self: start` across the journey. No HUD is laid over a building, chapter object, or text. The HUD remains top-right throughout the story, including the closing horizon. |
| Narrow screens                               | Single-column story with in-flow landscapes. The compact HUD displays five stats across at normal phone text size, labels above numbers and pips. Its font-relative grid wraps when text grows; it yields to normal flow above the height limit. No large pinned theater or shrinking text to hide defects.                                                                                              |
| Short landscape viewport or enlarged text    | Use compact mode based on available dimensions, not user-agent sniffing. If the compact HUD still exceeds 25% of the usable viewport height, put the HUD back in normal flow rather than shrinking text or hiding stats. Readability is the explicit exception to persistence.                                                                                                                           |
| No JavaScript / failed enhancement           | Label any displayed sheet "Opening stats; chapter snapshots follow." It is not presented as a live reading-position display. Every chapter's actual stats and badge grants are available in the semantic story. No empty theater or blocking loader.                                                                                                                                                     |
| Reduced motion                               | Keep stat/badge progression and readable story. Use instant scene/object changes, no route interpolation/reveal translation, and no CSS transitions or smooth scrolling.                                                                                                                                                                                                                                 |
| Print                                        | Single-column complete story, periods, facts, stat summaries, and badges. Remove sticky/fixed positions and unnecessary repeated decorative theater art.                                                                                                                                                                                                                                                 |

In mobile dock mode, reserve the dock's full footprint at the beginning of the document; set `scroll-padding-top` and marker `scroll-margin-top` to its measured height plus a 12px gap. Include `env(safe-area-inset-top)`, left/right safe areas, and normal page padding. Use an opaque cream dock with a clear lower border. Text may pass behind the dock as it leaves the reading area, as with an ordinary page header, but every line must be scrollable into an unobscured reading area and each checkpoint heading must be clear of the dock at activation. Do not claim that padding at the top alone prevents all mid-scroll obstruction: the reading-line clearance and end-space checks are required too.

Use `ResizeObserver` to measure actual HUD height when labels wrap or text size changes. It may set a bounded numeric CSS custom property through `element.style.setProperty()` for reserved space and scroll offsets. Do not serialize an entire inline style string. Avoid feedback loops: badge acquisition must not change HUD dimensions, and the measurement write must not change the HUD's own width. Reserve all 11 badge slots from the beginning; unearned slots are neutral empty outlines, not fake achievements. A fixed-size rack and tabular numerals prevent stat changes from moving thresholds.

Body and story must never have fixed heights or hidden vertical overflow. Use `svh` for stable scene sizing, with a conventional `vh` fallback, and avoid repeatedly resizing the document as mobile browser chrome expands or collapses. Put clipping only on the decorative landscape frame, not on ancestors that would interfere with sticky positioning or hide prose. Do not use `overflow-x: hidden` on the whole page to conceal a width bug.

Test widths 320, 375, 390, 768, 1024, and 1440 CSS pixels; include a short landscape viewport, notched-device safe areas, 200% text enlargement, and 400% desktop zoom/reflow. Numeric stats must remain legible, the final badge rack must not overflow, the chapter object must remain inside its scene, and all story content must have a usable reading area.

**Accessibility Contract**

- Use `lang="en"`, a zoom-permitting viewport meta tag, one `h1`, a `main` landmark, ordered chapter sections with `h2` headings, and `h3` card headings. Visible text is real HTML in chronological reading order.
- Render period labels and all supporting facts on the server. Use actual `<time datetime>` values only where the supplied precision is valid; freeform period labels need not pretend to be machine dates.
- The HUD is an `aside` with five definition-list entries. Numeric text is authoritative; decorative pips are `aria-hidden`. These are read-only meters, not interactive sliders or an application role.
- Keep dynamic HUD updates `aria-live="off"`. The owner removed visible snapshot sections; semantic per-card stat equivalents remain visually hidden during enhancement and readable by assistive technology. They are visible without JS, on enhancement failure, and in print. No text is removed from the HTML or delayed for motion.
- Milestone slots are nonfocusable list items. Earned milestones have meaningful labels; unearned slots are assistive-hidden. Full milestone descriptions are server-rendered beside their story passages, visually hidden but available to assistive technology. There is no duplicate final ledger or hover-only meaning.
- Mark duplicate decorative theater artwork and chapter objects `aria-hidden="true"` and `focusable="false"`. Give in-flow illustrations concise alt text only if they convey something not already in the adjacent prose; otherwise use empty alt text.
- Do not add tabindex, key handlers, focus traps, pointer cursors, or link-like underlines to noninteractive cards. There is no repeated navigation block requiring a skip-link control; the main landmark and heading navigation are available immediately.
- Target WCAG AA contrast: 4.5:1 for ordinary text and 3:1 for large text and meaningful graphical indicators. Never distinguish rising/falling stats solely with red and green.
- Keyboard scrolling, find-in-page, selection, reduced motion, forced colors, and screen-reader reading order are release checks, not optional polish.

**HTTP Contract**
There is no client-facing state API. Queries do not customize the story and are not reflected in output or logged. No uploads, authentication, admin interface, feedback form, redirects based on user input, or mutable endpoints are present.

| Route                            | Methods / Response                             | Behavior                                                                                                                                                                                                                                                                                   |
| -------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/`                              | GET, HEAD; `200 text/html; charset=utf-8`      | Complete story, local resource URLs, title/description, and fixed canonical metadata for `https://pranavprem.com/`. HEAD returns the same headers without the body. Use `Cache-Control: no-cache` so HTML is revalidated, not cached immutably.                                            |
| `/healthz`                       | GET, HEAD; `200 application/json`              | Exactly `{"status":"ok"}` with `Cache-Control: no-store`. Indicates the application is responding with validated content loaded; does not claim DNS, Cloudflare, artwork rendering, or the public hostname are healthy. No versions, paths, environment, uptime, or diagnostics.           |
| `/static/<path:filename>`        | GET, HEAD; correct file MIME                   | Flask/Werkzeug safe-directory serving rooted only at `app/static`, plus membership in the approved asset inventory. Normal conditional/range semantics are acceptable. Use ETag/Last-Modified and short public caching, initially `max-age=3600`; do not mark unversioned names immutable. |
| Unknown path / asset             | `404 text/html`                                | Small readable error: "That trail is not on this map. The story begins at pranavprem.com." No clickable recovery UI, path echo, or filesystem details.                                                                                                                                     |
| Unsupported method               | `405` with `Allow`                             | Explicitly support GET/HEAD only; disable automatic OPTIONS if necessary so the contract is consistent. No state changes.                                                                                                                                                                  |
| Invalid host / oversized request | `400` / `413`, or earlier proxy/WSGI rejection | Generic bounded response; never reflect the offending input.                                                                                                                                                                                                                               |
| Unexpected rendering error       | `500 text/html`                                | "The story could not load. Try reloading later." Minimal error template independent of story data; no traceback or environment in the response.                                                                                                                                            |

Use Flask's safe static implementation rather than joining a request path to an arbitrary directory or using `send_file` on a user-supplied path. At startup, build a small allowlisted asset inventory: approved `.css`, `.js`, `.svg`, `.png`, `.webp`, `.ico`, and, only if later approved, local `.woff2` files. Reject symlinks, hidden path components, unexpected extensions, and resolved paths outside the static root. Requests outside that inventory return 404. Never expose the repository root, `docs`, JSON source, PDFs, dotfiles, or `/run/secrets` through a catch-all route.

Use fixed local paths for templates/content and allowlisted art keys resolved with `url_for('static', ...)`. Do not accept template names, file paths, URLs, hostnames, or JSON content from request input. Set `MAX_CONTENT_LENGTH=1024` and conservative Gunicorn request-line/header limits. Since unread bodies do not necessarily trigger Flask's size check, explicitly reject a declared Content-Length above 1024 with 413 at the request boundary. These GET-only routes do not parse or use request bodies. Early WSGI rejections are not guaranteed to carry Flask's response headers.

**Security Contract**
Set headers centrally for Flask responses, including static files, health, and handled errors. Keep the local and production CSP equally strict; only production HTTPS policy differs.

```text
Content-Security-Policy:
  default-src 'none';
  script-src 'self';
  script-src-attr 'none';
  style-src 'self';
  style-src-attr 'none';
  img-src 'self';
  font-src 'self';
  connect-src 'none';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'none';
  form-action 'none';
  frame-src 'none';
  worker-src 'none';
  media-src 'none'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cross-Origin-Resource-Policy: same-origin
```

Send the CSP as one HTTP header value; line breaks above are for documentation. Do not use `'unsafe-inline'`, `'unsafe-eval'`, wildcard hosts, data/blob sources, inline event handlers, inline executable bootstrap code, or an inline `<style>` block. No nonce infrastructure is necessary. Use external CSS, fixed classes/data attributes, textContent, and numeric SVG presentation attributes for rendering. Limited direct CSSOM property assignment for measured geometry is allowed; `setAttribute('style', ...)` and `style.cssText` are not. Test this distinction under the enforced CSP in all target engines.

Jinja autoescaping remains on, all template attributes are quoted, and content does not use `|safe` or `Markup`. JS never uses `innerHTML`, `eval`, dynamic imports from data, or user-controlled selectors. SVGs are reviewed as active-capable files: no scripts, event attributes, `foreignObject`, remote references, embedded external fonts, or executable URLs, even if an image embedding mode would usually suppress execution.

Set Flask `TRUSTED_HOSTS` to exact names: production `pranavprem.com` and loopback `127.0.0.1` for the container health probe; local mode adds `localhost`. Do not trust wildcard hosts or request-supplied forwarded headers. Configure the tunnel origin HTTP Host Header as `pranavprem.com`. Leave ProxyFix out: there is no need for visitor IPs or inferred external URLs. Gunicorn should not broadly trust forwarded headers either. Canonical metadata comes from fixed configuration, never `request.host`.

Cloudflare owns the HTTP-to-HTTPS redirect. The origin intentionally receives HTTP over a private bridge; an app-level `request.is_secure` redirect would risk a loop. In production send `Strict-Transport-Security: max-age=31536000` after public TLS has been verified. Do not initially add `includeSubDomains` or preload, which would make promises about other hostnames. Omit HSTS in local HTTP mode.

The application creates no session or cookies and needs no Flask secret key. CSRF/authentication mechanisms are not applicable to the current read-only surface; adding a form or mutable endpoint would require a new design review. No SQL, shell interpolation, outgoing URL fetch, or file upload boundary exists. Do not add CORS or CSP reporting endpoints.

Disable access logs containing visitor IPs, full URLs, headers, referrers, or user agents. Application error records should contain a fixed error code, safe exception category, and an operator correlation ID, not request data or arbitrary exception strings. Keep connector logs operational, never debug-level, and verify their privacy with a synthetic query/header canary before enabling retained logs. If the pinned connector emits request data at the selected level, disable its retained logs with `logging: {driver: none}` rather than storing them unredacted; use container state and Cloudflare tunnel status for routine operations. For safe retained logs, configure bounded rotation, initially 5 MB x 2 files per service. No browser telemetry, console dumps of story data, analytics beacons, third-party error reporting, or performance collection.

Cloudflare necessarily processes network metadata as the hosting transport. This is not an analytics integration, but do not advertise "no third party ever sees a request." Disable optional Web Analytics, Browser Insights/beacons, Rocket Loader, email obfuscation, and other HTML/JS injection for this hostname. Review challenge/JavaScript-detection settings so normal visits do not receive injected code or require clicking through a challenge; retain infrastructure DDoS protection. Do not relax CSP to accommodate optional edge features. Verify the public response, not only the origin.

Supply-chain and isolation controls address the remaining practical OWASP risks: pinned dependencies/images, small request limits, bounded logs/resources, no public admin surface, least-privilege secrets, strict static serving, and reviewed public content. Container isolation is defense in depth, not a substitute for a patched NAS and restricted Docker administration.

**Deployment Contract**
Use Docker Compose v2 on a Linux NAS. Determine whether the NAS is `linux/amd64` or `linux/arm64` before choosing image manifests. No architecture is assumed here. Pin the Python base and `cloudflare/cloudflared` to tested releases and verified digests; do not fabricate a digest or deploy floating `latest`. Use cloudflared's documented `TUNNEL_TOKEN` environment input only in the connector.

The app image installs only exact runtime requirements, preferably with hashes, during build. Use explicit `COPY` instructions for requirements and `app/`, never `COPY . .`. A deny-by-default `.dockerignore` allows only those build inputs and the Dockerfile. Do not send PDFs, docs, tests, Git history, `.env`, NAS configuration, or secrets to the build context. Run as a fixed unprivileged UID/GID such as `10001:10001`, own application files by root and make them readable but not writable by that UID, and set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1`.

The image's exec-form command runs Gunicorn on `0.0.0.0:8000`, with two sync workers, a 30-second timeout, a 20-second graceful timeout, and `--worker-tmp-dir /tmp`. No development server, reloader, PID/log files in the app directory, runtime package installation, or persistent volume is needed. Standard output/error are the operational log destinations, subject to the privacy rules above.

Suggested base `compose.yaml` contract:

```yaml
services:
  portfolio:
    build: .
    user: "10001:10001"
    init: true
    read_only: true
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    tmpfs:
      - /tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777
    environment:
      PORTFOLIO_ENV: production
    expose: ["8000"]
    networks: [origin]
    restart: unless-stopped
    stop_grace_period: 30s
    mem_limit: 256m
    cpus: 1.0
    pids_limit: 64
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2); raise SystemExit(0 if r.status == 200 else 1)"
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "5m"
        max-file: "2"

networks:
  origin:
    internal: true
```

Production `compose.tunnel.yaml` contract, merged explicitly. The real file supplies the verified `2026.8.3` image digest as an overridable default; the example below leaves image selection explicit:

```yaml
services:
  cloudflared:
    image: "${CLOUDFLARED_IMAGE:?Set a tested cloudflare/cloudflared tag and digest}"
    user: "65532:65532"
    command:
      - tunnel
      - --no-autoupdate
      - --loglevel
      - warn
      - --metrics
      - 127.0.0.1:2000
      - run
    environment:
      TUNNEL_TOKEN: "${CLOUDFLARED_TOKEN:?Set the dedicated tunnel token in Portainer}"
    depends_on:
      portfolio:
        condition: service_healthy
    read_only: true
    cap_drop: [ALL]
    security_opt: ["no-new-privileges:true"]
    tmpfs:
      - /tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777
    networks: [origin, egress]
    restart: unless-stopped
    stop_grace_period: 40s
    mem_limit: 256m
    cpus: 0.5
    pids_limit: 64
    logging:
      driver: none

networks:
  egress: {}
```

The numeric connector identity is an intended nonroot identity, not a claim that every image tag has been tested with it. Verify the pinned image supports this UID, can read its CA bundle and token, and runs with a read-only root and no capabilities on the actual NAS. Do not add `NET_RAW`, `NET_ADMIN`, privileged mode, host networking, Docker socket mounts, or root as a workaround for optional ICMP-proxy warnings. This tunnel needs only HTTP origin access.

The app joins only the `internal` origin network; the connector also joins a normal egress network for DNS and outbound tunnel traffic. An internal-only connector cannot reach Cloudflare. `expose` documents the app port; it is not a firewall. Neither service has production `ports`, and the NAS/router needs no inbound port-forward for the website. Do not share these networks with unrelated NAS services. `internal: true` is not a complete security boundary against the Docker host or a compromised connector: enforce NAS firewall/segmentation policy and verify access to management interfaces is blocked.

Permit connector egress to the current documented Cloudflare tunnel destinations on TCP/UDP 7844 and to the intended DNS resolver. QUIC uses UDP and HTTP/2 fallback uses TCP. Restrictive firewalls should use Cloudflare's maintained destination list, not copied stale IPs from this design. Image pulls and builds are separate host/build-time network needs. No runtime app egress is required. The connector's outbound-capable network must not become an unrestricted route into private NAS administration or other LAN services.

Token lifecycle and ownership:

1. Create a remotely managed tunnel in the Cloudflare dashboard for the owner-controlled domain. The connector token is scoped to that tunnel; do not provision an account-wide certificate or API key to either container.
2. The owner accepts authenticated Portainer stack metadata as the operational boundary for this single-administrator Docker Standalone deployment. Set raw `CLOUDFLARED_TOKEN` only in the protected stack environment. Restrict Portainer accounts, sessions, API keys, backups, and Docker administration accordingly.
3. Compose maps `CLOUDFLARED_TOKEN` only to cloudflared's officially supported `TUNNEL_TOKEN` environment variable. The owner explicitly accepts the resulting connector environment-metadata exposure within the restricted Portainer/Docker administration boundary. The app receives no token.
4. For command-line recovery, store the variable only in an administrator-controlled external env file with restrictive permissions and pass it through `--env-file`. Do not export it interactively, use the checkout's automatic `.env`, or enable shell tracing.
5. Do not put a token literal in Compose YAML, Git, an image layer, command arguments, screenshots, logs, public issues, or support output. A Docker/Portainer administrator can retrieve connector environment metadata; restrict that administrator boundary accordingly.
6. Verify the connector using container state and the Cloudflare dashboard without printing the token or dumping stack/container environments. Missing, empty, or revoked values must fail startup or authentication.
7. Rotate a potentially exposed token in Cloudflare, update the protected Portainer variable or external env file, and redeploy the connector. Keep backups encrypted and restricted, separate from source backups.

Remote routing is configured in Cloudflare, not in a local `config.yml`: publish only `pranavprem.com` to `http://portfolio:8000`, set the origin HTTP Host Header to `pranavprem.com`, and leave HTTP/2-to-origin off. The hostname route covers `/`, `/healthz`, and approved static paths without rewriting prefixes. Unmatched hostnames/routes should end in the tunnel's 404 behavior, not a wildcard NAS route. Do not create private-network routes or a Cloudflare Access login gate for this public portfolio. Optional `www` behavior is deferred until explicitly chosen.

DNS for the apex points through the Cloudflare-managed tunnel route, not to a public NAS IP. Enable public edge TLS and an edge HTTP-to-HTTPS redirect. Plain HTTP is acceptable only for the final private Docker bridge hop. Do not add `noTLSVerify` or deploy a separate Nginx/ACME stack for this topology.

Suggested `compose.local.yaml` contract:

```yaml
services:
  portfolio:
    ports: ["127.0.0.1:8000:8000"]
    environment:
      PORTFOLIO_ENV: development
      PORTFOLIO_HSTS: "0"

networks:
  origin:
    internal: false
```

Local mode retains Gunicorn, nonroot operation, read-only files, capabilities restrictions, and strict CSP, but accepts localhost and omits HSTS. The explicit noninternal local bridge avoids reliance on host port publication into internal networks across Docker/NAS versions. It is never included in production. Rebuild after edits for the simplest workflow; if a source mount is later needed, mount only `app/` read-only, never the PDF-containing workspace root.

```sh
# Local: no connector service or Cloudflare variable/secret is evaluated.
docker compose -f compose.yaml -f compose.local.yaml up -d --build portfolio

# Production: env file is outside the checkout and contains paths/image metadata.
docker compose --project-name portfolio --env-file /absolute/protected/portfolio.env -f compose.yaml -f compose.tunnel.yaml config --quiet
docker compose --project-name portfolio --env-file /absolute/protected/portfolio.env -f compose.yaml -f compose.tunnel.yaml up -d --build --wait portfolio cloudflared
```

The split is intentional: profiles on a single production file can still cause interpolation of required token variables during local configuration parsing. Two small explicit overrides avoid that ambiguity without adding runtime services. Do not name the local file `compose.override.yaml`, which could be loaded accidentally on the NAS.

`depends_on: service_healthy` orders initial startup only. Docker restart policies restart exited processes, not merely unhealthy containers. The connector handles reconnection after an app restart; a wedged live app may need operator intervention after Gunicorn timeouts. Do not add an auto-heal container with access to the Docker socket. Use the NAS's existing operational facilities and Cloudflare tunnel status. Do not add a shell/curl healthcheck to the minimal connector image on the assumption it contains those tools.

For releases, run tests, build a release-tagged app image, inspect the image contents and effective Compose config, deploy, and verify both the public root and `/healthz`. Retain the previous image/tag and reviewed content for rollback; no database migration or volume restore exists. Tunnel outage cannot be repaired by a Flask error page. A single NAS and connector are intentionally a small-site availability tradeoff, not high availability.

**Failure Modes**

| Failure                                                   | Visitor Behavior                                                       | Operator Action                                                                                                                                 |
| --------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Invalid story/schema/reference                            | New app instance fails startup; no half-valid story                    | Error identifies a safe field/card ID and required correction. Fix content, run validation, rebuild; keep or restore the previous image.        |
| Missing required static asset                             | Startup/build validation fails                                         | Restore the original approved asset; do not hotlink a replacement.                                                                              |
| Individual browser image failure                          | Text, stats, reserved scene space, and remaining art stay usable       | Inspect asset status and MIME/cache behavior; browser failure is not a reason to hide the story.                                                |
| Missing/blocked/broken JavaScript                         | Complete readable story and static chapter stats                       | A small fallback note is sufficient. No retry modal or infinite loading state.                                                                  |
| Invalid client geometry / unexpected rendering error      | Disable enhancement, preserve semantic content                         | Reproduce viewport/zoom/layout condition; do not log visitor data.                                                                              |
| Flask exception                                           | Generic 500 page with safe headers                                     | Use safe error category/correlation ID; fix and redeploy.                                                                                       |
| Missing or revoked token                                  | Tunnel does not connect; origin may still be healthy                   | Check protected Portainer input, connector-only `TUNNEL_TOKEN`, and dashboard status; rotate/redeploy if required, never print credentials.     |
| Connector cannot resolve `portfolio` or wrong origin Host | Public origin error or 400 while app health passes                     | Check shared origin network, `http://portfolio:8000`, and fixed HTTP Host Header.                                                               |
| NAS/tunnel/DNS/edge outage                                | Cloudflare error or connection failure, not an app-controlled fallback | Check NAS power/network, container state, egress/DNS, public hostname configuration, and Cloudflare status. No offline/service-worker promise.  |
| Version/cache mismatch                                    | Browser should fall back safely if the projection version is unknown   | Revalidate HTML, replace assets together, purge affected edge assets if needed, or roll back. Avoid immutable caching of unversioned resources. |

**Test Plan**
Use pytest with Flask's test client for Python/HTTP tests and Python Playwright for browser tests. Playwright and its browsers are development/CI tools only; no Node/npm service or browser binaries ship in the app image. The implemented tools are Ruff for Python and pinned ESLint/Prettier plus local axe-core for browser checks; there is no frontend build pipeline. Keep malformed/private-boundary fixtures synthetic, not extracted from the private PDFs.

| Area                    | Required Cases                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Content contract        | Exactly the intended chapter/event/badge counts; unique IDs; all source refs; correct region order; supported schema; no duplicate grants; integer 0-10 values; reject booleans, NaN, out-of-bounds landmarks, unknown assets, overlong text, missing fields, and symlink assets.                                                                                                                                |
| Editorial integrity     | Preserve the CS-specific national top 0.01%, 110%/sole-student account, owner-supplied dengue/month-in-hospital account without invented timing/details, top-ten IEEE wording, 2019 joining year, Google inside the MS, Green Belt-only hours, and confirmed second place at PayPal. Assert rejected copy/low-value projects stay absent, the core stays below 900 words, and the UI disclaimer is not restored. |
| Snapshot semantics      | Assert the version-two table, opening `0, 1, 1, 1, 0`, five-key order, monotonic Experience, milestone prefixes `0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 10, 11`, and actual milestone IDs. COVID keeps earlier grants and coding competence; the CS result is an academic grant, not an illness prize.                                                                                                                 |
| Pure JS state           | Import the exported selector in a real browser. At every threshold test just below, exact equality, and just above; repeat positions in randomized order. A given geometry/cursor must produce identical stats/badges regardless of prior calls. Test negative/overscrolled input, empty/invalid inputs at the validation boundary, and large jumps.                                                             |
| Real scrolling          | Scroll down through all checkpoints, back to opening, then jump to the end and back. Compare both text and decorative pips/slots. Test repeated crossings, scrollbar dragging, native vertical keyboard scrolling, the bounded reversible side-arrow alias and object response, horizontal-overflow bypass, native fragments, find-in-page, reload at mid-story, bfcache restoration, and hidden-tab return.     |
| Geometry                | Verify first/last reachability; changing viewport, zoom, text wrapping, or image timing remeasures correctly. Checkpoint headings sit below the mobile dock at activation, and all card text can enter an unobscured reading area. Acquiring all badges never changes card positions or HUD height. No update feedback loop or busy idle rAF.                                                                    |
| Progressive enhancement | JS disabled, module 404, malformed projection, CSS disabled, individual image 404, unsupported observer API, reduced motion at load and toggled later, and print. Full story text and chapter stats remain accessible in every applicable fallback.                                                                                                                                                              |
| Responsive visuals      | Chromium, Firefox, and WebKit at listed widths, short landscape, safe areas, text enlargement, and zoom/reflow. No horizontal overflow, clipped facts, HUD/art collision, unreadable values, or inaccessible closing content. Check actual iOS Safari/Android scrolling before launch because desktop emulation does not reproduce all browser-chrome behavior.                                                  |
| Accessibility           | Semantic outline and main landmark, reading order, named stats, earned badge descriptions, no fake interactive roles/tab stops, no live-region spam, contrast, forced colors, and no required hover/click. Manual VoiceOver or NVDA pass; use a locally installed audit tool if desired, not a CDN-injected script.                                                                                              |
| HTTP/security           | GET/HEAD, 404/405/400/413/500, cache policy, health body, MIME/nosniff, CSP on successful and handled-error responses, no Set-Cookie/CORS, invalid Host rejection, and forwarded-header spoofing. Inject synthetic HTML/attribute/script terminators into test content and confirm it stays inert in text/data attributes.                                                                                       |
| Static boundary         | Encoded traversal, double encoding, dotfiles, private-file-shaped paths, secret paths, disallowed extensions, directory URLs, and symlink escapes all fail. Inspect artifact paths; never open private PDFs to construct a fixture.                                                                                                                                                                              |
| Browser privacy/CSP     | Enforce CSP, collect violations locally in tests, assert all requests are same-origin and no fetch/beacon/WebSocket activity occurs while scrolling, check cookies/storage stay empty, and ensure no optional Cloudflare script appears in public HTML. Check safe numeric CSSOM/SVG updates in all three engines.                                                                                               |
| Container/deployment    | Build without private build-context inputs; inspect image file list and history; no token in layers/env/command; nonroot IDs; read-only root; only tmpfs writable; all caps dropped; no host ports in production; app has no secret/egress network. Test local startup with no token variables or file. Test missing/unreadable token failure without displaying it.                                             |
| Operational behavior    | Start app before connector, restart app, restart connector, simulate loss of egress, restore connectivity, verify public HTTP redirect/HTTPS/health/static behavior, test secret rotation/recreation, and confirm the previous image can be redeployed. Test synthetic sensitive query/header canaries do not enter retained logs.                                                                               |
| Documentation handoff   | Apply the completion gate using only public project files: all seven docs are substantive, links resolve, README commands match the implementation, the full sanitized story and disagreements remain, and handoff results distinguish tested, failed, and not-run work. No dependency on chat history, PDFs, or private credentials for local continuation.                                                     |

Performance targets are release budgets to measure, not results already achieved: initial HTML/CSS/JS/art below approximately 750 KB transferred after compression, JS below 20 KB compressed, CSS below 30 KB compressed, and original SVG scene complexity kept small. Set intrinsic image dimensions to target CLS below 0.1. Target LCP below 2.5 seconds under a documented mobile test profile and avoid scroll tasks longer than 50 ms. A representative midrange device should scroll smoothly without animation work while idle. Prefer deleting visual complexity over adding workers, animation libraries, or speculative caching systems.

**Implementation Order**

1. Establish public/private ignore rules and an allowlisted Docker build context before initializing or staging the already-approved public repository. Add the canonical contributor entry points and README, preserve the existing full story and its source classifications, and maintain handoff status as work proceeds.
2. Implement content loading/validation, Flask routes/headers, and the complete semantic Jinja story. Prove no-JS readability, static safety, and the content snapshots first.
3. Author the four landscapes, chapter objects, and badge art; implement the warm editorial CSS and responsive base layout without scroll interception.
4. Add the pure state selector, document markers, passive/rAF controller, fixed-size HUD/badge rack, and deterministic SVG rendering. Prove reversibility and fallback behavior before embellishing motion.
5. Implement and test the hardened image and explicit local/tunnel Compose overrides. Verify the NAS architecture, Portainer stack-secret behavior, and restricted administration before enabling the public hostname.
6. Run lint/format checks and unit, HTTP, browser, accessibility, privacy, and deployment checks. Review final implementation against this contract, record actual outcomes/deviations in `docs/handoff.md`, and complete the documentation gate and brief retrospective.
7. Publish only reviewed public artifacts to the owner-approved public repository after the checks. Deploy, smoke-test the public origin, and update the README and handoff with pinned images, rollback instructions, and actual deployment status. This architecture-only revision performs none of these publication/deployment actions.

**Open Risks**

| Risk Or Decision                   | Default / Required Follow-Up                                                                                                                                                                                                                                                                      |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Documentation maintenance          | All seven docs exist. Keep operational results and the complete story current so another session can continue without chat or PDFs.                                                                                                                                                               |
| Public autobiographical wording    | The story and numeric claims are authorized. Preserve first-person recollections, supplied-document attribution, and compassionate wording; avoid invented precision or expansion into confidential details, not the requested claims themselves.                                                 |
| Source confidence                  | The lead read both PDFs with explicit permission. Resume/Profile are supplied-document evidence, not external verification; disagreements remain in `docs/story.md`. No repeat permission request or PDF read is required to use the sanitized handoff.                                           |
| NAS compatibility                  | NAS CPU, Docker/Compose version, available memory, firewall policy, and Portainer/Docker administration model are unknown. Validate before selecting final image digests or declaring the deployment tested.                                                                                      |
| Cloudflare ownership/configuration | Zone ownership, DNS/TLS, remote tunnel, protected Portainer token variable, edge injection settings, and permitted egress are not provisioned by this draft. `www` is out of scope until chosen.                                                                                                  |
| Mobile persistence tradeoff        | A large sticky theater plus a full HUD would consume the reading area. This design intentionally uses in-flow mobile landscapes and permits a nonfixed HUD at extreme zoom/short heights. Validate with the owner in a visual prototype rather than hiding text to preserve the desktop metaphor. |
| Original art quality/IP            | The original landscapes and inline chapter objects were authored and visually reviewed locally. Physical-device legibility and any future commercial/license/trademark decisions remain separate checks.                                                                                          |
| Small-site availability            | One NAS and connector can be unavailable during power/network failure or release replacement. No database simplifies recovery but does not provide high availability.                                                                                                                             |
| Dependency/edge drift              | Pin and periodically update tested releases. Recheck Cloudflare token-environment behavior, injected features, logs, and Portainer interpolation semantics against the deployed versions.                                                                                                         |
| Repository state                   | Public visibility is owner-approved. Local Git is initialized on `main` and `github.com/pranavprem/portfolio` exists. The handoff records commit/push and hosted CI outcomes. Never stage the workspace wholesale.                                                                                |

None of these risks requires implementing a CMS, database, event bus, frontend framework, analytics system, or larger deployment platform. They are documentation completion, faithful source treatment, targeted browser/NAS validation, and operational configuration checks.

**Research References**
Official guidance consulted on 2026-09-06. These links document technology behavior, not biographical evidence. They are documentation references only; the finished application does not fetch them or render them as clickable UI.

- Flask, Gunicorn deployment: https://flask.palletsprojects.com/en/stable/deploying/gunicorn/ . Supports the production WSGI server choice and nonroot/nonpublic-origin binding approach.
- Flask, security considerations: https://flask.palletsprojects.com/en/stable/web-security/ . Autoescaping, resource limits, security headers, and `TRUSTED_HOSTS` inform the HTTP boundary.
- Cloudflare, remote tunnel creation: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/create-remote-tunnel/ . Published hostname routes are managed remotely and point to an explicit origin service.
- Cloudflare, tunnel run parameters: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/run-parameters/ . Documents `TUNNEL_TOKEN`, no-autoupdate, logging risks, and protocol behavior.
- Cloudflare, origin parameters: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/origin-parameters/ . Documents HTTP Host Header and the distinction between HTTP and HTTPS origins.
- Cloudflare, tunnel firewall requirements: https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/tunnel-with-firewall/ . Documents outbound TCP/UDP 7844 and maintained destination lists.
- Docker, networks: https://docs.docker.com/reference/compose-file/networks/ . Documents internal network isolation and explicit multi-network membership.
- Docker, service environments: https://docs.docker.com/reference/compose-file/services/#environment . Portainer's protected stack input is mapped only to cloudflared's supported `TUNNEL_TOKEN`; it is not a Docker secret store.
- Docker, service lifecycle/security: https://docs.docker.com/reference/compose-file/services/ . Documents health-dependent startup, nonroot users, read-only filesystems, capabilities, resource limits, and log rotation configuration.
- MDN, document scroll event: https://developer.mozilla.org/en-US/docs/Web/API/Document/scroll_event . Scroll handlers must stay cheap; rAF alignment is not a frequency throttle.
- MDN, reduced motion: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion . OS preference must remove nonessential motion rather than merely slow it down.
- MDN, CSP style attributes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src-attr . Distinguishes blocked inline style strings from direct CSSOM property updates.
