**Contributor Contract**
This is Pranav Prem's original, warm pixel-game autobiography: a complete server-rendered scroll essay enhanced by a reversible character sheet and landscape. It is not a resume dashboard, combat game, contact funnel, or frontend platform. Preserve the existing visual language and the human story, including uncertainty, hobbies, boredom, illness, burnout, and current joy.

The owner explicitly requires documentation sufficient for another human or AI to continue without chat history, private PDFs, or asking him to repeat his full story. That is a delivery requirement, not optional polish. This file is the canonical contributor instruction set; `CLAUDE.md` only points here.

**Required Reading**
Read in this order before editing:

1. This file.
2. [README.md](README.md): purpose, actual file map, local/testing commands, configuration, deployment, recovery, privacy, and art licensing.
3. [docs/architecture.md](docs/architecture.md): full approved technical design, state/scroll/security contracts, rationale, test matrix, and completion gate.
4. [docs/story.md](docs/story.md): complete sanitized account, chronology, human/project inventories, source classifications, discrepancies, and unknowns.
5. [docs/handoff.md](docs/handoff.md): observed implementation/check/deployment status, current deviations, and next tasks.
6. [docs/retrospective.md](docs/retrospective.md): evidence-based implementation lessons and remaining verification limits.

Then inspect the actual files relevant to the task. Architecture examples are not proof of implementation or additional biographical evidence. Historical "not yet implemented" statements in the approved docs describe their drafting sessions. The handoff owns current observed status; code/config own actual behavior, which must still be checked against approved requirements. Record deviations rather than silently treating code as new permission.

**Story Authority**

- Keep `docs/story.md` as the complete public-safe narrative/source ledger. `app/content/story.json` is only the curated runtime selection. Do not replace the long account with the eleven website chapters or make future contributors recover omitted context from chat.
- The lead already read the private PDFs with the owner's permission and supplied sanitized evidence. Do not reopen, parse, modify, embed, serve, or commit them. Use the public-safe docs. Do not seek permission again for the already-authorized story or numeric claims.
- Distinguish `owner-supplied`, `supplied-document`, editorial wording, and `game-fiction`. Preserve card `source_refs`: `owner-brief`, `resume`, `profile`, and `supplied-documents` only. The last is for extracts without a specific PDF attribution. None implies independent institutional verification.
- The approved architecture's owner clarifications supersede older omission/permission suggestions: include Profile's national top 0.01% Class 12 CS result and the first-person 110%, maximum-possible, sole-student recollection. Never invent an exact school rank/board, extra-credit mechanism, course identity, or all-time university record.
- Publish IEEE Xtreme as national top ten because Profile says seventh and Resume eighth. Publish Salesforce joining year `2019` because January/March disagree. Preserve both source claims in the full ledger; do not invent a reconciliation.
- Architecture's supplied Chat 2019-2021, burnout 2020-2021, and Copilot 2023 chronology remains owner-supplied, not document corroboration. Keep Google Hardware/Nest inside the MS period. Do not infer product transfers from promotion dates, birth year from ages, exact GRE/TOEFL scores, illness/recovery details, or confidential implementation.
- Attribute 2,000+ hours only to the Green Belt project, not TasKing or all automation. Preserve present-day enthusiasm, drive, knowledge, and team understanding explicitly in prose. Humor targets chores and self-importance, not illness or burnout.
- Inspect template-only copy as well as JSON. `index.html` contains milestone callouts, opening/ending prose, and captions; `story.js` repeats region captions. A JSON-only review can miss invented claims. The original unsupported grading explanation was corrected and now has a rendered-copy regression test.
- Ask a single focused question only when a genuinely new decision depends on unknown information. Otherwise use the supplied broader wording. Never ask for the full story again or invent missing precision.

**Product Invariants**

- Native vertical document scrolling is the only site interaction. No visible anchors, buttons, menus, forms, downloads, contact CTA, clickable cards/badges, hover-only content, custom game keys, or mandatory choices. Documentation links and resource/canonical metadata are allowed; visitor controls are not.
- Preserve wheel/touch/trackpad/scrollbar and native keyboard scrolling, history, selection, find-in-page, zoom, and assistive-technology navigation. No `preventDefault()` input interception, scripted scroll positioning, modified scroll restoration, smooth/snap enforcement, horizontal game scroller, or transform-driven document timeline.
- All prose, facts, six-stat chapter snapshots, and badge descriptions remain semantic server-rendered HTML without JavaScript. Text must never await motion, a checkpoint visit, or a completed animation. Failure leaves readable storybook mode, not a stale live HUD, blocking loader, modal, or retry control.
- Fixed stat order is `coding`, `enthusiasm`, `vitality`, `charisma`, `automancy`, `sidequests`. Values are absolute integers 0-10. The current display mapping is Health/HP for `vitality`, not a separate Health meter. Opening values are exactly `0, 1, 1, 1, 0, 1` with zero earned badges.
- `stats_after` and cumulative `badges_after` snapshots are authoritative, never additive mutations of previous UI state. Same reading geometry/position means the same chapter, scene, mood, stats, badge prefix, and walking frame regardless of direction, prior visits, reload, or large jump.
- There are eleven chapters, twelve checkpoints, and eleven badges. Chapter 09 has two cards; closing horizon/ledger is not another chapter. Reserve all HUD slots at opening, with zero future badges visually or accessibly presented as earned. Burnout keeps earlier badges; rewinding before a grant removes it. No duplicated grants, persistence, random/time-based state, or future job/achievement invention.
- State selection uses ordered in-flow card markers and the reading line 35% down the unobscured viewport. Equality belongs to the later checkpoint. Measure real document geometry, not sticky art or percentage of page height. Preserve first/last reachability and remeasure after reflow, viewport/font/image changes, pageshow, and restoration.
- Motion is local, bounded, reading-position-derived, and reversible. Passive scroll schedules at most one pending rAF; it is paint batching, not a claimed event-frequency throttle. No idle loop, autonomous bobbing, flashing, sound, count-up animation, springs, confetti, or delayed badge state. Reduced motion uses immediate discrete changes and static poses, including when toggled mid-story.
- Desktop HUD is top-right with art beneath it. Mobile has compact stats and in-flow landscapes, not a huge pinned theater. Reserve fixed-HUD clearance and all badge space, include safe areas, and keep every line readable. If a dock exceeds 25% of usable viewport height, normal flow beats unreadable persistence. Do not shrink text or hide overflow to conceal layout defects.
- Keep numeric `n / 10` text authoritative, decorative pips/art noninteractive and hidden from assistive technology, dynamic HUD `aria-live="off"`, and semantic per-card equivalents. Verify heading order, contrast, forced colors, print, no-JS/reduced-motion reading, and real mobile/zoom behavior. Automated accessibility tooling is not the whole review.

**Implementation Boundaries**
Keep the runtime small: Python 3.13, Flask/Jinja/Gunicorn, local JSON, CSS, one vanilla JS module, original local SVG, and system fonts. No runtime Node, framework, game engine, canvas/WebGL requirement, database, CMS, background service, analytics, remote content, or cloud dependency beyond Cloudflare transport. Developer Node/Playwright/axe tooling does not justify a frontend build pipeline.

Key editing locations are `app/__init__.py` for HTTP/config/security, `app/content.py` for validation/projection/static inventory, `app/content/story.json` for curated content/state, `app/templates/` for semantic rendering and inline art, and `app/static/` for CSS/JS/original landscapes. The README maps deployment and tooling files. Do not invent helper layers or compatibility paths without a concrete need.

Validation intentionally fixes this release's counts, keys, order, source kinds, text limits, moods, art references, and 320 x 180 geometry. Reject invalid numbers, booleans-as-integers, duplicate JSON keys, out-of-bounds landmarks, symlinks, or missing assets rather than clamping/repairing authored data. Adding a chapter/stat/badge/region requires explicit scope approval and coordinated changes to validation, templates, JS/CSS assumptions, architecture, source mapping, and exact-count/snapshot/browser tests. A relaxed assertion alone is not the feature.

**Security Boundaries**

- Public approval covers reviewed source, sanitized biography, and original art, not PDFs, private contact PII, precise personal/NAS locations, confidential employer details, tokens, or private notes. Preserve `.gitignore` PDF/secret exclusions and the deny-by-default `.dockerignore` allowlist. Never `COPY . .`, serve the repository root, or mount the PDF-containing workspace into the app.
- Validate external input at HTTP/static boundaries. Keep GET/HEAD-only routes, startup content validation, bounded request sizes, generic errors, fixed canonical origin, exact trusted hosts, and approved static inventory plus safe-directory serving. No arbitrary path/template/URL execution, broad forwarded-header trust, ProxyFix, CORS, sessions, or request-derived redirects.
- Keep Jinja autoescaping and inert quoted `tojson | forceescape` projection data. No `|safe`, `Markup`, inline executable script/style, event attributes, `innerHTML`, eval, remote runtime requests, or CSP relaxation. Numeric CSSOM measurements and SVG attributes are narrowly allowed and must work under enforced CSP in all target engines.
- Review SVGs for active content, external references, and copied franchise/employer material. Original artwork and factual company names do not imply trademark clearance or endorsement. No explicit project license is chosen; public visibility and dependency licenses do not authorize assigning one.
- Do not print/log tokens, environment dumps, visitor IPs/URLs/queries/headers, or arbitrary exception messages. Keep app error records bounded and sanitized. Connector log retention stays off until synthetic canary checks prove the pinned version safe; never enable debug as a shortcut. Cloudflare processes transport metadata even though the application has no analytics or tracking storage.
- Production uses only `compose.yaml` + `compose.tunnel.yaml`, app and connector together, no published ports. Local uses only base + `compose.local.yaml` with `127.0.0.1:8000`. Never expose Flask development/debug mode publicly.
- The tunnel token is an external file mounted only into connector UID/GID `65532:65532`; `CLOUDFLARED_TOKEN_FILE` is a path, never the value. File-backed Compose secrets depend on real host ACLs/UID mapping. No world-read/777, root, extra capabilities, Docker socket, or secret-in-env workaround. Desktop behavior does not prove NAS permissions. Recreate after token rotation.
- Cloudflare routes `pranavprem.com` to `http://app:8000` with origin HTTP Host Header `pranavprem.com`; it owns the HTTPS redirect. Enable `PORTFOLIO_HSTS=1` only after public TLS/redirect verification, without includeSubDomains/preload. No optional edge JS injection or click-through requirement. Restrict connector egress, including DNS and Cloudflare UDP/TCP 7844, from unrelated NAS administration.
- Review practical OWASP risks, dependency/image pins, privacy, and least privilege for every material change. NAS hardening, verified image manifests, and Docker restrictions are not substitutes for actual runtime checks.

**Checks And Commands**
Run from the checkout root. Full setup/runbook and prerequisites are in the README. Minimal local setup/start, without public/debug binding:

```sh
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-dev.txt
unset FLASK_DEBUG
export PORTFOLIO_ENV=development
export PORTFOLIO_HSTS=0
.venv/bin/flask --app app:create_app run --host 127.0.0.1 --port 8000
```

Use Node 24+ for the following development tools only:

```sh
npm ci
npm run lint
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -m 'not browser'
.venv/bin/playwright install chromium firefox webkit
.venv/bin/pytest -m browser --browser chromium --browser firefox --browser webkit
```

`npm run lint` is ESLint plus Prettier; `npm run format` formats Prettier-supported files and `.venv/bin/ruff format .` formats Python. Jinja is intentionally excluded from Prettier. Use scoped formatting in a shared/limited-scope worktree. `axe-core` is a pinned npm dev dependency for local browser accessibility tests, never a production/CDN script. Tests live in `tests/`; CI lives in `.github/workflows/ci.yml`. Missing tests, skipped engines, or installed dependencies are not passing evidence.

Local container check:

```sh
docker compose -f compose.yaml -f compose.local.yaml config --quiet
docker compose -f compose.yaml -f compose.local.yaml up -d --build --wait app
```

Cover happy paths, malformed data/requests, source integrity, exact absolute snapshots and badge prefixes, threshold equality/random-order rewinds, no-JS/failure/reduced-motion behavior, CSP/privacy/static boundaries, three browser engines, responsive HUD clearance, zoom/text/forced-colors/print, and safe container configuration. Record commands, actual outcomes, environment/browser versions, failures, skips, and unrun checks in the handoff. Never label a design target, manifest inspection, localhost health, or running connector as a tested NAS/public deployment.

**Working Discipline**
The main session owns orchestration and integration. The current owner instruction is **do not spawn agents**. Perform architecture consideration, architecture review, implementation, testing, code/security review, architecture conformance, handoff, and evidence-based retrospective as sequential roles in the main session. A documentation-only assignment does not authorize application edits or a retrospective file outside its allowed paths.

If a future owner-authorized task permits a team, the main session may coordinate only team tools actually available in that environment, with scoped responsibilities and reviewed results. Teammates do not orchestrate more teammates. When those tools are absent or disallowed, perform the roles sequentially; do not invent tool names, claim imaginary reviews, or block progress waiting for unavailable machinery. Do not introduce per-model instructions or competing policy files.

Prefer the smallest correct change following current conventions. Use `apply_patch` for manual edits when available, otherwise a normal scoped editor; formatting tools are for intended files only. Use typed errors, clear names, and rare comments explaining non-obvious reasons. Avoid speculative abstractions, compatibility layers, dead code, unrelated refactors, and new dependencies.

Inspect before editing and preserve unrelated work, including concurrent changes, staging state, private files, and PDFs. Never reset, revert, overwrite, or clean another contributor's work. Stop for a directly conflicting concurrent edit; otherwise continue within scope. Do not initialize Git, stage, commit, amend, push, or publish unless the current task explicitly authorizes it. The initial setup request authorizes a public repository and initial publication; do not assume that grants blanket permission for future tasks. Inspect only intended public artifacts for secrets and private paths; never stage the workspace wholesale. Roll back deployments using a separate known-good commit checkout, not destructive reset or guessed cherry-picks.

**Completion Gate**
Update affected operational docs when behavior changes, preserve the full story/source ledger, and keep all four entry/handoff docs mutually consistent with the full architecture. `CLAUDE.md` must remain thin. Required project delivery also includes a factual `docs/retrospective.md`; create it only in an appropriately scoped task after actual work/checks.

Do not mark the project complete until the architecture's documentation/content/security/browser/container gates are supported by recorded results. Resolve known source-copy deviations, add/review the actual tests and CI, and document remaining Cloudflare/NAS/operator prerequisites without secrets. A contributor must be able to understand, run locally, edit, test, and resume the work from public files alone. Do not ask the owner to reconstruct context the project was explicitly required to preserve.
