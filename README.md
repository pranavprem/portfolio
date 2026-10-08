**Pranav Prem**
A life in side quests: a warm, original full-screen pixel-game autobiography for `pranavprem.com`, built with Python rather than a frontend application platform.

The point is to meet a person by playing through his story, not browse a resume with animations. The main story is at most 900 visible words: games in Goa, the mosquito boss fight, college, HSBC, SJSU, Google, Salesforce Bots/Copilot/Agentforce, and personal agent/homelab/printing projects back in San Jose. Paragraph-sized dialogue beats keep distinct events separate. The Quest log collects 13 main-story summaries and 11 optional discoveries in chronological story order, with links back to their scenes. The voice is direct and dryly funny, without a lesson after every event or repeated reward paragraphs.

Source repository: `https://github.com/pranavprem/portfolio` (public, owner-approved). The Quest log implementation was published as `7f9e6fbd77530ea9570652e06c1207546769980a` and passed all four exact-SHA CI jobs. A documentation-only follow-up records that evidence in [the handoff](docs/handoff.md). Code publication is not a Portainer redeployment: public asset verification, HTTP redirect/HSTS, NAS isolation/recovery, and physical-device checks remain operator gates.

The later San Jose home-scene and work/home-copy revisions are local working-copy changes, not yet committed or deployed. Their checks and new 16-file runtime boundary are recorded in the handoff; the older release's hosted CI is not evidence for these changes.

**Read First**
The owner explicitly requires a complete, AI-agent-ready handoff so he never has to repeat his full story. These documents have different jobs:

| Document                                     | Responsibility                                                                                                                                                          |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)                       | Canonical contributor instructions and invariants. Start here before changing the project.                                                                              |
| [README.md](README.md)                       | Actual file map, setup, editing, checks, and operational runbook.                                                                                                       |
| [docs/architecture.md](docs/architecture.md) | Full approved technical design, rationale, contracts, test matrix, and completion gate. It is a separate full document, not replaced by this README.                    |
| [docs/story.md](docs/story.md)               | Complete sanitized narrative, chronology, emotional arc, projects, hobbies, awards, provenance, and source disagreements. Never replace it with the short website copy. |
| [docs/handoff.md](docs/handoff.md)           | Current implementation, observed checks, outstanding work, and decisions the next lead needs.                                                                           |
| [CLAUDE.md](CLAUDE.md)                       | Thin entry point to the same contributor instructions, not a second policy.                                                                                             |

[docs/retrospective.md](docs/retrospective.md) records implementation lessons and remaining limits. Historical observations in the source ledger are evidence notes, not current deployment status; use the handoff for that. No conversation history or private PDF is needed to continue.

[docs/review.md](docs/review.md) contains the current Python, whimsical-engineer, recruiter, hiring-manager, and direct-wellwisher review, including the remaining tradeoffs rather than only praise.

**The Experience**

- Enhanced mode is a full-viewport chapter adventure. Start/Continue/Back buttons, Left/Right arrows, Enter/Space, and horizontal touch swipes advance or rewind paragraph-sized dialogue beats. The main game does not use document scrolling.
- Text is part of the game scene: each screen combines the current landscape, chapter object, period, heading, dialogue, reward, and controls. All five stat bars stay visible in the HUD, including while the Quest log is open. Place captions no longer repeat object names. There are no branching choices, combat, timers, saved progress, forms, downloads, hover-only reveals, or remote embeds.
- Eleven authored glints reveal scene popups: GEC extras, games/CyanogenMod, Green Belt/CI-CD, Coldplay, Opportunity Hack, MS/research detail, Google tools, promotions, awards, gaming, and a separate hobby list. Each is a native labeled 48px button; the popup leaves dialogue visible and Escape/Close restores focus. Some scenes have two non-overlapping glints. Optional facts appear once in the game and are summarized again only in the Quest log. There are no catalog-only discoveries or repeated reward paragraphs.
- College has four required dialogue beats rather than seven: independence, Python/PyCon, hackathons, and academic standing. Department leadership, Zuari, and the paper remain separate paragraphs in the GEC discovery, with reviewed project links. Automation has two required beats rather than three; Green Belt's savings paragraph is optional and no longer repeated in a reward block. Stats/milestone grant points are unchanged, and no discovery must be opened to continue.
- The Quest log records main chapters at their final beat and easter eggs only after their popup is found. Entries stay in the journal when revisiting earlier moments. Clicking a heading returns to its story screen or reopens its original popup, without changing history/URLs or stats. The journal lasts only for this page visit; reload clears it. All 24 summaries and all discovery content remain in no-JS/failure/print output. Broad/undated source labels stay broad rather than acquiring guessed dates.
- Eleven chapters span Goa, Pune, San Jose, and San Francisco. Chapter 09 has separate contribution and sustainable-COVID-cadence cards, giving twelve stat checkpoints. The ending and optional catalog are not new chapters.
- Desktop uses a scene/dialogue split; mobile stacks the scene and dialogue above a fixed thumb-control row. Both fit the usable `100dvh` viewport, include safe-area padding, and preserve at least 48px control targets. Dialogue scrolls internally only under text enlargement, unusually short viewports, or long optional overlays.
- Every paragraph, fact, achievement, link, and stat equivalent is server-rendered. JavaScript only selects screens/beats and updates presentation. No-JS, invalid-projection, resource-failure, and print modes expose the complete document with in-flow landscapes and semantic snapshots.
- Eleven original objects follow the chapters: controller, backpack, compass, laptop, Java mug, automation gear, books, toolkit, cloud terminal, bot console, and agent nodes. Objects move between authored landmarks; milestone rewards use one bounded hop and static sparks. The owner's new mosquito/COVID encounters are a narrow exception to the earlier no-living-sprites rule: original decorative symbols make a single pass of at most two seconds on scene entry. They do not imply a COVID infection, gate navigation, or simulate damage. Reduced motion shows static symbols and disables other effects.
- Dark mode follows `prefers-color-scheme` without a toggle or storage. Original art includes the NCS elephant, a multi-building GEC campus, and Salesforce Tower. Work chapters end in San Francisco (`bay-area`), then the epilogue returns to a separate San Jose home illustration with a gaming corner, printer bench, home controls, and homelab. It is symbolic art, not a real house/floor plan or device specification.
- The ending keeps the final stats while its marker moves from the front path to the homelab and printer as dialogue advances. Separate gaming and hobby discoveries sit on the monitor and original guitar. The hobby list ends with "Making lists. You may have noticed." Back and Quest log jumps restore the correct work/home scene; reduced motion makes the same visual changes without transitions. No new chapter or stat checkpoint was added.
- "For my wages..." introduces paid CRM/agent-platform work; "But for fun..." introduces the personal homelab and house projects. The owner-described mostly defunct/not-running local-AI repositories no longer appear in runtime copy or links. Their qualified history remains in the full source ledger; a public repository is not proof of current operation.
- Cream paper, green ink, amber details, system serif headings, segmented meters, and original chapter objects provide the game language. No living avatar, mascot, borrowed game assets, employer logos, remote fonts, sound, combat, or game proficiency is involved.
- The 3D-printing ending uses `I'm 40% PLA` beside a tiny original generic pixel robot, without an explicit voice cue. It does not copy or load Futurama artwork.

The five read-only meters use absolute integers from 0 through 10. They are narrative shorthand, not medical measurements, years, or certifications. Health uses internal key `vitality`; Experience uses `experience`. Automancy and Side Quests have been removed as stats. The title and hobby references to side quests remain part of the story.

The final sheet deliberately leaves room to grow: **Coding 8, Enthusiasm 10, Health 8, Charisma 7, Experience 7**. Only Enthusiasm is full at the ending. Earlier Charisma/Experience and post-SJSU Coding are rebalanced accordingly; Experience never decreases. The owner's earlier SJSU Coding 10 remains a historical peak in coding intensity, not a claim of complete mastery.

| JSON Key     | Full / Compact Label | Opening | Meaning                                                                    |
| ------------ | -------------------- | ------- | -------------------------------------------------------------------------- |
| `coding`     | Coding / Code        | 0       | How stretched the coding muscle feels; a dip is not forgotten knowledge.   |
| `enthusiasm` | Enthusiasm / Spark   | 1       | Appetite for the current quest.                                            |
| `vitality`   | Health / HP          | 1       | Playful adventure energy, never a clinical score.                          |
| `charisma`   | Charisma / Charm     | 1       | Confidence collaborating, teaching, and leading.                           |
| `experience` | Experience / XP      | 0       | Accumulated engineering/life experience; never decreases in authored time. |

The eleven milestones are First game, House Captain, National top 0.01%, 7 hackathon wins, Java training #1, Green Belt: 2,000+ hours, Prof. Paul's TA, Google Hardware/Nest intern, Months to minutes, Bots at 99.99%, and Principal engineer. Each is an actual supplied achievement or role. None is a trophy for illness; the percentile is granted where that academic result is stated. Slots are reserved from opening, with no future milestone shown as earned.

Stat state is a pure function of the selected event index. Each card supplies five absolute `stats_after` values; Python prepares the complete cumulative `badges_after` prefix. The title uses opening state, twelve event screens select indices `0..11`, and the epilogue holds the final stats while using its own San Jose home scene. Dialogue position and the page-local journal never mutate stats. Experience accumulates even when energy dips; the COVID adjustment does not portray a collapse in coding ability or health. Nothing is saved in cookies, storage, sessions, URLs, or a database.

Authored content and the inert client projection now use `schema_version: 2`. Retired stat keys, old versions, and decreasing Experience fail validation. A malformed or incompatible client projection hides the live HUD and leaves the complete server-rendered story/stat equivalents. There is no persisted-data migration or compatibility layer.

**Small System**

```text
Public browser -- HTTPS --> Cloudflare edge
                             |
                      outbound-established tunnel
                             |
                      cloudflared connector
                             |
                 HTTP http://portfolio:8000
                    private Docker origin bridge
                             |
                    Gunicorn -> Flask -> Jinja
                             |
                  validated local story.json

HTML + local CSS/JS/SVG -> chapter-adventure enhancement in the browser
No game state is sent back to the server.
```

Runtime is Python 3.13, Flask, Jinja, and Gunicorn, with one small vanilla JavaScript module. There is no runtime Node/npm, frontend build step, framework, database, CMS, queue, analytics, remote API, or cloud service dependency except Cloudflare for public transport. Installing dependencies and pulling images are build/development network operations, not runtime application services. Node 24+ and Python Playwright are development-only tools.

| HTTP Surface     | Contract                                                                                                                                                                            |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/`              | GET/HEAD, complete HTML, fixed canonical `https://pranavprem.com/`, `Cache-Control: no-cache`.                                                                                      |
| `/healthz`       | GET/HEAD, `{"status":"ok"}` with a trailing newline on GET, `Cache-Control: no-store`.                                                                                              |
| `/static/<path>` | GET/HEAD, approved inventory under `app/static/` only; rendered URLs carry a deterministic content digest while responses retain conditional serving and `max-age=3600`.            |
| Errors           | Generic handled 400/404/405/413/500 pages with security headers and no reflected request details; unsupported methods retain `Allow`. Earlier Gunicorn/proxy rejections can differ. |

There is no public state API, authentication, admin endpoint, upload, or contact form. Requests do not customize the story. Content and templates are loaded/validated at startup, not fetched or reparsed per visitor.

**File Map**

| Path                                                                       | Edit Or Inspect For                                                                                                                               |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app/__init__.py`                                                          | `create_app()`, exact trusted hosts, HTTP routes, security/cache headers, bounded requests, safe application/Gunicorn exception logging.          |
| `app/content.py`                                                           | JSON validation, `ContentValidationError`, public game projection, static inventory.                                                              |
| `app/content/story.json`                                                   | Main prose/summaries, eleven discoveries and milestones, source references, and absolute snapshots. Not the full narrative archive.               |
| `app/templates/base.html`                                                  | Metadata, local resources, document shell.                                                                                                        |
| `app/templates/index.html`                                                 | Story, HUD, inline art, assistive stat/milestone equivalents, compact highlights, and template-only copy.                                         |
| `app/templates/error.html`                                                 | Independent, noninteractive error page.                                                                                                           |
| `app/static/story.css`                                                     | Full-viewport desktop/mobile game layout, HUD/overlays, reduced motion, forced colors, print.                                                     |
| `app/static/story.js`                                                      | Exported `deriveState()`, projection/marker checks, dialogue/chapter controls, swipe/keyboard input, overlays/focus, DOM/SVG rendering, fallback. |
| `app/static/art/`                                                          | Original city scenes, the ending's `san-jose-home.svg`, `pla-robot.svg`, and `favicon.svg`.                                                       |
| `requirements.txt`, `requirements-dev.txt`                                 | Exact, hash-locked Python runtime and development dependency closures. The dev lock includes runtime dependencies.                                |
| `pyproject.toml`                                                           | Ruff and pytest configuration; the `browser` marker is registered here.                                                                           |
| `package.json`, `package-lock.json`, `eslint.config.js`, `.prettierignore` | Development-only ESLint, Prettier, and local `axe-core`. Jinja templates are excluded from Prettier.                                              |
| `Dockerfile`, `.dockerignore`                                              | Pinned Python image, runtime-only installation, startup validation, explicit copies and deny-by-default build context.                            |
| `compose.yaml`                                                             | Hardened app and internal origin network; no published port.                                                                                      |
| `compose.local.yaml`                                                       | Explicit loopback-only development override; no connector or token requirement.                                                                   |
| `compose.tunnel.yaml`                                                      | Pinned nonroot connector, outbound network, protected Portainer token mapping, no retained connector logs or published ports.                     |
| `.env.example`, `.gitignore`                                               | Configuration shape and private/development file exclusions; no real token is committed.                                                          |

`tests/conftest.py` supplies independent expected snapshots, content fixtures, and an ephemeral loopback server. `test_content.py`, `test_http.py`, and `test_browser.py` exercise the authored-data boundary, public HTTP surface, and real-browser behavior. `.github/workflows/ci.yml` runs lint/Python checks and three separate browser-engine jobs with read-only permissions and commit-pinned actions. Hosted CI status is recorded in the handoff separately from local results.

`tools/check_public.py` is development/release tooling, excluded from the runtime image. It checks staged Git blobs or every commit in a revision range for prohibited private-file paths, symlinks/submodules, structured credential signatures, and private home-directory paths. It reports counts, never matched values, and does not open untracked PDFs or `.env` files. Synthetic self-tests verify the implemented rules; this is not an exhaustive PII/secret detector. Review the intended diff manually as well.

**Local Python**
Prerequisites: a supported Python 3.13 interpreter, `uv`, and a shell opened at the checkout root. `uv` can provision Python where supported. Neither Docker nor Cloudflare credentials nor Node is needed to serve the page locally.

```sh
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python --require-hashes -r requirements-dev.txt
unset FLASK_DEBUG
export PORTFOLIO_ENV=development
export PORTFOLIO_HSTS=0
.venv/bin/flask --app app:create_app run --host 127.0.0.1 --port 8000
```

Read `http://127.0.0.1:8000/` in a local browser. Stop with Ctrl+C. This command deliberately has no debugger or reloader; restart it after edits to JSON, templates, or Python. Never bind the development server publicly, use `--debug`, or enable `FLASK_DEBUG`. Werkzeug's development access logs are not the production privacy setup; use only synthetic/local requests, without sensitive query strings or headers.

In a second terminal, a basic origin check is:

```sh
curl --fail --silent --show-error http://127.0.0.1:8000/healthz
curl --fail --silent --show-error --head http://127.0.0.1:8000/
```

A successful health response means the process is responding after startup validation. It does not prove artwork, browser state, accessibility, DNS, public TLS, or the tunnel works. Local results for these different boundaries are recorded separately in the handoff.

**Local Docker**
Use Docker Engine or Docker Desktop with a current Compose v2 supporting `--wait`. Run from the checkout root:

```sh
docker compose -f compose.yaml -f compose.local.yaml config --quiet
docker compose -f compose.yaml -f compose.local.yaml up -d --build --wait portfolio
docker compose -f compose.yaml -f compose.local.yaml ps
```

Open `http://127.0.0.1:8000/`. No `.env`, token, or Cloudflare variable is needed because the tunnel file is not loaded. Port 8000 is published only on loopback. Stop the Python development server first if it already owns that port.

This runs Gunicorn with the same nonroot/read-only hardening as production. Re-run the `up` command after edits; there is no source bind mount or automatic rebuild. To stop and remove this local stack:

```sh
docker compose -f compose.yaml -f compose.local.yaml down
```

Never add `compose.local.yaml` to production, rename it to an automatically loaded override, or bind-mount the PDF-containing workspace into a container.

**Configuration**
Three settings are nonsecret. `CLOUDFLARED_TOKEN` is the raw tunnel credential and is required only when loading the production tunnel override.

| Name                | Allowed / Default Value                                                         | Effect                                                                                                                                                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PORTFOLIO_ENV`     | `development` or `production`; direct Python defaults to `development`.         | Production trusts `pranavprem.com` and `127.0.0.1`; development also trusts `localhost`. The literal `local` is invalid. Base Compose hardcodes `production`; the local override hardcodes `development`. An env-file value does not override those Compose literals. |
| `PORTFOLIO_HSTS`    | Exactly `0` or `1`; default `0`.                                                | Only production plus `1` adds `Strict-Transport-Security: max-age=31536000`. The local override forces `0`. Enable only after verifying public HTTPS and the edge redirect.                                                                                           |
| `CLOUDFLARED_TOKEN` | No default; the raw token for the dedicated remotely managed portfolio tunnel.  | Compose maps this Portainer/host input only to cloudflared's supported `TUNNEL_TOKEN` environment variable. The app receives no token.                                                                                                                                |
| `CLOUDFLARED_IMAGE` | Optional reviewed release tag plus verified digest; pinned default shown below. | Selects the connector image. Do not replace it with floating `latest` or an unverified digest.                                                                                                                                                                        |

The app does not load `.env` itself, and `python-dotenv` is not a dependency. Direct Python uses process environment. Compose uses `.env` or an explicit `--env-file` for interpolation, not as a blanket container environment import. Existing shell variables can take precedence over env-file interpolation; check the intended deployment configuration in a clean operator shell.

For command-line production, use an administrator-controlled env file outside the checkout, for example `/absolute/protected/portfolio.env`, with mode `0600`. Provision it through a secure editor or credential workflow without putting the token in shell history. Portainer users should set the same values in the authenticated stack environment instead.

```dotenv
PORTFOLIO_ENV=production
PORTFOLIO_HSTS=0
CLOUDFLARED_TOKEN=<raw tunnel token>
CLOUDFLARED_IMAGE=cloudflare/cloudflared:2026.8.3@sha256:51c9cefcb4569df44e1ad403ab1d3d8065aa8e84339bcfc6aee75502e1140339
```

The first line documents intent; base Compose already sets that mode. The last line may be omitted to use the identical pinned default in `compose.tunnel.yaml`. Keep the production env file out of Git, backups intended for public source, screenshots, logs, and support output. `.env.example` documents the variable name but never contains a token. No Flask secret key, Cloudflare account API key, visitor tracking ID, or database URL is needed.

**NAS Prerequisites**
Production targets a Linux NAS with Docker Compose v2 and either `linux/amd64` or `linux/arm64`. Determine the actual CPU, Engine/Compose versions, available memory, rootless/user-namespace configuration, ACL behavior, and firewall policy first. `x86_64` usually corresponds to amd64; `aarch64` to arm64. Do not force an incompatible `platform` or assume a 32-bit NAS is supported.

The Python base is pinned to `python:3.13.15-slim-bookworm@sha256:ed86c82274b3c69b52fb5820f358f0bd7df0b603332063cb5c6e32bd220c3e6e`. The connector pin is shown above. Their multi-architecture manifest verification is recorded in the Dockerfile/Compose comments and `.env.example` on 2026-09-06, including amd64/arm64 support. This pass inspected those references, not a fresh registry query. Manifest support is not execution evidence: neither actual NAS architecture, NAS permissions, nor a live tunnel has been tested by this documentation pass.

The app runs as `10001:10001`, with root-owned read-only application files, two synchronous Gunicorn workers, a small `/tmp` tmpfs, all capabilities dropped, and no-new-privileges. It joins only the internal origin network and has no persistent volume. The connector runs as `65532:65532` with similar restrictions and joins both origin and outbound egress networks. Resource limits and lifecycle settings are in Compose; validate them on the NAS rather than granting root or privileged access when something fails.

No production host ports are published. Dockerfile `EXPOSE` and Compose `expose` document the internal port; they are not host-port publication or a complete firewall. No router inbound port forwarding is required. Allow the connector DNS access and outbound UDP/TCP 7844 to Cloudflare's current documented tunnel destinations. QUIC uses UDP; HTTP/2 fallback uses TCP. Restrict access from the connector network to NAS management and unrelated LAN services. The Docker host/administrator remains privileged; an internal bridge is not isolation from the host itself.

**Create The Tunnel**
Prerequisites are owner-controlled Cloudflare zone/DNS access for `pranavprem.com`, active edge TLS, and an operator who can securely provision the tunnel token. No token belongs in the repository; the following dashboard steps contain no credential values.

1. In the Cloudflare dashboard's tunnel/connectors area, create a remotely managed Cloudflare Tunnel for this portfolio. Dashboard labels can change; use the Cloudflared connector type, not a private-network route. Do not execute a wizard command containing a token literal.
2. Obtain the token for this specific tunnel through the protected dashboard workflow. Enter it only into the authenticated Portainer stack variable or protected external production env file described below. Do not provision an account-wide certificate, API key, or local ingress `config.yml`.
3. Add a published application/public hostname route for exactly `pranavprem.com`, covering the whole path without prefix rewriting. Service type is HTTP and service URL is `http://portfolio:8000`, not the NAS address, `localhost`, or HTTPS.
4. Under origin HTTP settings, set **HTTP Host Header** to `pranavprem.com`. Leave HTTP/2-to-origin off. Do not add `noTLSVerify`; this private origin hop is intentionally HTTP. The connector resolves `portfolio` on the shared Compose network.
5. Let the dashboard create the proxied tunnel DNS route for the apex. Resolve conflicting apex A/AAAA/CNAME records as appropriate; DNS must route through the tunnel, not reveal a public NAS IP. Do not add wildcard hostnames or NAS-management routes. `www` behavior is not chosen and must not be guessed.
6. Enable public edge HTTPS and an edge HTTP-to-HTTPS redirect for the hostname. Do not add a Flask `request.is_secure` redirect: the HTTP bridge hop would risk a redirect loop. There is no need for another Nginx/ACME service.
7. Disable optional HTML/JavaScript injection for this hostname: Rocket Loader, Web Analytics, Browser Insights/beacons, email obfuscation, and similar transformations. Review challenge and JavaScript-detection rules so ordinary visits do not require injected code, a login, or a click-through challenge. Keep infrastructure DDoS protection; do not weaken CSP to accommodate optional edge features.
8. Publish only the intended hostname route, with unmatched routes returning the tunnel's 404 behavior. Do not place a Cloudflare Access login gate on this public story. Verify the actual public response after startup, including local assets and the absence of injected scripts.

Official operational references: [remote tunnel creation](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/create-remote-tunnel/), [origin parameters](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/origin-parameters/), and [current firewall requirements](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/tunnel-with-firewall/). These are documentation links, not runtime dependencies.

**Protect The Token**
The owner accepts authenticated Portainer stack metadata and Docker container environment metadata as the secret-management boundary for this single-administrator NAS. Set `CLOUDFLARED_TOKEN` in Portainer, not in Compose YAML, Git, an image, a command argument, chat, screenshots, logs, or public support output. Restrict Portainer accounts, API keys, sessions, backups, and the Docker socket as administrator-equivalent access.

Compose maps the Portainer variable only to cloudflared's officially supported `TUNNEL_TOKEN` environment variable. The app receives no token. An administrator who can inspect the connector or stack can retrieve the token; this is an explicit owner-accepted tradeoff for the selected deployment. The connector remains nonroot and read-only, has no capabilities or Docker socket, retains no logs, and is the only service with the credential.

Command-line operators should keep `CLOUDFLARED_TOKEN` in the protected external env file used with `--env-file`, not export it interactively or place it in the checkout's automatic `.env`. Avoid shell tracing and environment dumps. Rotate an exposed/revoked token in Cloudflare, replace the Portainer stack variable or protected env-file value, and force a connector redeployment. Keep any token backup encrypted, restricted, and separate from public-source backups.

**Portainer Git Stack**
For Docker Standalone, deploy from the public repository rather than pasting a merged file. Current Portainer Git stacks accept additional Compose paths, preserving the reviewed two-file production split and repository build context.

1. In the intended Docker Standalone environment, choose **Stacks**, **Add stack**, then **Git repository**. Name the stack `portfolio`.
2. Set the repository URL to `https://github.com/pranavprem/portfolio.git`, repository reference to `refs/heads/main`, and Compose path to `compose.yaml`. Authentication is unnecessary for this public repository.
3. Under **Additional paths**, add `compose.tunnel.yaml`. This is equivalent to the reviewed `-f compose.yaml -f compose.tunnel.yaml` order. Never add `compose.local.yaml`.
4. Add `CLOUDFLARED_TOKEN` and enter the raw token for this dedicated tunnel. Leave `CLOUDFLARED_IMAGE` unset to use the pinned default, or set it to the exact tag-plus-digest from `.env.example`. Set `PORTFOLIO_HSTS=0` for the first deployment. Compose performs the `TUNNEL_TOKEN` mapping; do not add another token variable manually or paste the token into Compose YAML.
5. Leave relative-path volumes off; the stack has no application volume. Leave GitOps updates and forced redeployment off for the first release so the reviewed commit can be verified before automation is enabled.
6. Deploy the stack. Require both `portfolio-portfolio-1` and `portfolio-cloudflared-1` to remain running, the application to become healthy, and the Cloudflare dashboard to report the connector connected. The connector intentionally retains no logs.

Portainer supplies `CLOUDFLARED_TOKEN` to Compose, which maps it only to cloudflared's `TUNNEL_TOKEN`. The app receives only its fixed production mode and HSTS setting.

**Production Run**
From the reviewed release checkout, use a stable Compose project name, the external env file, and exactly the base plus tunnel files. Start both services explicitly:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml config --quiet
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml up -d --build --wait portfolio cloudflared
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml ps
```

Validate before deployment that the effective configuration has no `ports`, no app secret/egress network, no unintended mounts, and the pinned images/nonroot identities. `config --quiet` checks configuration/interpolation without printing it; it does not prove file readability or tunnel authentication.

The app healthcheck verifies the exact loopback `/healthz` response. `depends_on: service_healthy` orders initial connector startup. The connector has no Docker healthcheck: `--wait` can establish that it is running, not that Cloudflare/DNS/public HTTPS works. There is no assumption that the minimal connector image contains a shell or `curl`.

After the dashboard reports a connected tunnel, run synthetic public checks from outside the NAS:

```sh
curl --silent --show-error --head http://pranavprem.com/
curl --fail --silent --show-error --head https://pranavprem.com/
curl --fail --silent --show-error https://pranavprem.com/healthz
curl --fail --silent --show-error --head https://pranavprem.com/static/story.js
```

Require the HTTP response to redirect to `https://pranavprem.com/`, a valid public certificate without `-k`, a 200 story and health response, correct asset MIME/cache behavior, and the strict CSP on the public response. Inspect the rendered page/network locally for edge-injected scripts or challenges. A local origin success cannot establish these conditions.

Only after those TLS/redirect checks succeed, set `PORTFOLIO_HSTS=1` in the protected env file and re-run the production `up` command. Confirm the public header is exactly `max-age=31536000`, without `includeSubDomains` or preload. Local mode still omits HSTS. Previously cached HSTS persists in browsers; turning off the switch does not instantly undo that promise, so preserve working HTTPS through rollback.

For planned shutdown, using the same files/project/env:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml down
```

This deliberately takes the public site offline. Do not use `down` as a prerequisite for routine replacement, and do not remove retained rollback images.

**Updates And Recovery**
The base Compose file uses `build: .` and has no release-tagged `image:` setting. Its generated app image name is not a durable rollback identifier. Record the full reviewed commit, tested configuration, dependency/image pins, and built app image ID for each release; retain/tag or export the known-good image before replacing it. There is not yet a verified known-good release in this handoff.

1. Prepare a separate clean release checkout at the intended reviewed commit. Leave the existing deployment checkout and unrelated local work intact. Run the checks below on a development/CI machine; the NAS does not need npm to operate the image.
2. Reconfirm pinned manifests, the `.dockerignore` allowlist, image contents, nonroot/read-only behavior, and effective production networking. Keep the previous release checkout and locally tagged/exported app image available.
3. From the new checkout, pull the pinned connector and rebuild the app, then use the same stable project name and protected env file to replace the two services:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml pull cloudflared
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml build --pull portfolio
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml up -d --wait portfolio cloudflared
```

4. Recheck app health, tunnel status, public root/health/assets, TLS redirect, CSP, and a down/up browser journey. Record actual outcomes in the handoff. Brief downtime is possible; one NAS and one connector are not high availability.

To roll back, prepare another separate checkout at the recorded **known-good full commit**, or use the retained untouched release checkout. Do not rewrite the active worktree with `git reset --hard`, overwrite unrelated work, or cherry-pick a guessed inverse of changes. Review that release's Compose files against the current protected env/token, then run the full production `up -d --build --wait portfolio cloudflared` command from that checkout with the same `--project-name portfolio`. Re-verify public behavior. If rebuilding is unavailable, use the retained app image with an explicitly reviewed image-selection override; merely tagging an image does not make the existing `build: .` Compose file select it. Test that emergency path before relying on it.

There is no database, migration, uploaded media, or persistent app volume to restore. Back up reviewed public source/content/art, lockfiles, release/image identifiers, and protected operational configuration. Do not archive the whole local workspace into the public backup: it contains private originals and development artifacts. Token recovery is a separate restricted/encrypted backup or Cloudflare re-provisioning workflow. Preserve dashboard routing/security settings in protected operator records, not secret-bearing screenshots in Git.

After token rotation, force recreation rather than only restart:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml up -d --force-recreate --wait portfolio cloudflared
```

Docker's restart policy restarts exited processes, not merely unhealthy containers. A wedged live app needs diagnosis/operator action; do not introduce an auto-heal service with Docker socket access.

**Troubleshooting**
Use synthetic requests, container state, the exact safe health response, filesystem metadata, and dashboard tunnel status. Do not collect token contents, visitor query/header canaries containing real PII, raw environment dumps, private documents, or debug logs.

| Symptom                                             | Check And Safe Correction                                                                                                                                                                                                                                                              |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ContentValidationError` or build/startup fails     | Fix the named public JSON field or missing/unsafe asset. Full snapshots, exact release counts, plain text limits, and safe inventory rules are deliberate. Do not bypass validation to get a green container; restore the previous release if needed.                                  |
| Invalid environment value                           | Use `development`/`production` and HSTS `0`/`1`. `PORTFOLIO_ENV=local` is invalid. Check shell overrides and remember Compose modes are hardcoded.                                                                                                                                     |
| Local port unavailable                              | Stop another loopback server using port 8000; use either Flask or local Docker, not both. Production intentionally has no localhost-published port. Do not add the local override to troubleshoot a public deployment.                                                                 |
| App unhealthy                                       | Inspect `ps` health state and safe application error categories; check startup validation, memory/PID limits, and read-only/tmpfs configuration. A healthy process does not guarantee rendered art or a working tunnel.                                                                |
| HTTP 400 with healthy loopback probe                | Check Host routing. Production accepts only `pranavprem.com` and `127.0.0.1`; `portfolio`, a NAS IP, and `www` are not trusted hosts. Set the tunnel's origin HTTP Host Header to `pranavprem.com`, not a wildcard in Flask. Do not add ProxyFix or trust arbitrary forwarded headers. |
| Tunnel config cannot find `CLOUDFLARED_TOKEN`       | Add the raw dedicated-tunnel token to the authenticated Portainer stack environment or protected external production env file. Local work needs only base + local Compose and no dummy credential.                                                                                     |
| Token missing, empty, or revoked                    | Check that the protected Portainer stack variable exists without displaying it and that Compose mapped it to cloudflared's `TUNNEL_TOKEN`. Correct the stack value or rotate/redeploy through Cloudflare; never add the token to the app.                                              |
| Disconnected tunnel / Cloudflare 1033               | Check the connector process, credential lifecycle, NAS connectivity, and dashboard connector status. If not connected, origin health cannot make the public route available.                                                                                                           |
| Tunnel connected but origin error / 502             | Verify both services share the origin network and the route is exactly HTTP `http://portfolio:8000`, with the fixed Host header and no path rewriting. `localhost` inside the connector is not the application.                                                                        |
| DNS error or wrong site                             | Check the active Cloudflare zone, proxied apex tunnel record, conflicting records, hostname route, and propagation. Do not point DNS at a public NAS IP or invent `www` behavior.                                                                                                      |
| QUIC timeouts or reconnect loops                    | Check DNS and current Cloudflare destination rules for outbound UDP 7844 and TCP 7844 fallback. The connector needs the egress network; the app does not. ICMP-proxy warnings do not justify NET_RAW, NET_ADMIN, root, or privileged mode for this HTTP tunnel.                        |
| CSP failures, challenge page, or unexpected scripts | Inspect public HTML/network behavior against the local origin. Disable optional edge injection/challenges for normal visits; do not add `unsafe-inline`, `unsafe-eval`, remote script domains, or click-through UI.                                                                    |
| No connector logs retained                          | Intentional: `logging: driver: none` remains until a synthetic privacy canary verifies the pinned connector. Use state and dashboard diagnostics. Never enable debug logging or retain request-bearing output just to get more information.                                            |
| Scene/HUD falls back or shows old assets            | Confirm the HTML's `?v=<digest>` JS/CSS/SVG URLs, response hashes, and CSP. A digest mismatch means the release was not replaced together; purge only affected edge URLs if needed. Preserve readable fallback; do not force stale game state or a storage reset.                      |
| Browser tests missing/fail to collect               | Confirm `tests/`, the `browser` marker, dev dependencies, and installed Playwright engines. The fixtures start their own loopback server. Zero collected tests, missing executables, or an unrun suite are not passes.                                                                 |

If the origin must be probed without publishing a port, the app container has Python:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml exec -T portfolio python -c "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2); print(r.status, r.read().decode().strip())"
```

This prints only a synthetic status and the intentionally minimal health body, not a credential or diagnostic dump. Retained app logs are bounded to 5 MB x 2 files; custom exception loggers emit safe categories/correlation IDs. Logging privacy still requires a synthetic canary check. Do not assume all possible server/connector failures are proven private merely because the normal code is restrictive.

**Editing The Story**
Use `docs/story.md` as the complete source, `docs/architecture.md` for the approved presentation/technical contract, and `app/content/story.json` for the runtime selection. The source ledger must survive editorial shortening. Do not reopen, modify, serve, or require the private PDFs. The lead already read them with the owner's permission and preserved sanitized evidence; that does not make their claims independently verified.

The architecture's explicit owner clarifications supersede older suggestions to omit the numeric school/course results or seek permission again. Publish Profile's national top 0.01% Class 12 computer science result, without inventing an exact rank or exam board. Preserve the first-person 110%, maximum-possible, sole-student recollection without inventing an extra-credit mechanism or an all-time institutional record. Use national top ten for the conflicting IEEE seventh/eighth claims, and `2019` for the conflicting Salesforce January/March joining month. Keep both source claims in the ledger.

Chat 2019-2021, the COVID period, and Copilot by 2023 remain owner-supplied chronology, not new PDF corroboration; exact Bots/Copilot/Agentforce transition dates remain unknown. The latest owner account scopes 99.99% availability, Argo CD/CI/CD/monitoring, the public API, and the Heroku-to-multisubstrate migration to Einstein Bots; Slack is one contribution within the API work. Copilot is the configurable-agent communication platform; Agentforce is the customer agent-building platform that evolved from topics/actions into Atlas/AgentScript and the listed current capabilities. Preserve these distinctions without inventing dates, availability windows, customer counts, API contracts, internal architecture, or guaranteed deterministic model output.

The latest owner correction also places the dengue hospital month a few weeks before Class 12 final exams and identifies HSDI's youngest Rising Star nomination at age 20; preserve those relative/scoped facts without inventing exact dates, treatment, accommodations, or a broader award scope. Do not infer transfers from promotions, move Google outside the MS, infer a birth year, invent exam scores, or attribute Green Belt hours to TasKing. Current copy explicitly names enthusiasm, drive, and passion; the earlier knowledge/team-understanding wording is retained only as source history. The full-time comparison is with an internship's fixed end date, not all project deadlines.

For an ordinary copy change, edit plain text in the appropriate JSON card while preserving its `source_refs`. Also inspect template-only prose, milestone callouts, opening/ending text, and duplicated region captions in Jinja/JS; JSON is not the only current text source. Never use executable Markdown/HTML, template evaluation, `|safe`, or JavaScript injection to format a card.

The latest whole-script pass favors explicit actors/actions over compressed resume language: "Being house captain," a sustainable pace during COVID, tools that create Jira issues, and enterprise software running in a data center. Preserve the owner's supplied jokes rather than adding a punchline or lesson to every event. Do not turn the separate SpartanBot/Opportunity Hack projects into one project or infer a missing sequence between them.

Current authoring guardrails in `app/content.py` are intentionally stricter than a generic chapter engine:

There is no independent achievement catalog. Each main card has a short `summary`; `epilogue_summary` covers the template ending. Eleven `discoveries` own their `id`, target `card_id` (or `epilogue`), heading, period label, plain-text `body`, optional `list_items`, summary, position, sources, and up to three labeled links. Python derives all 24 Quest log records from those sources in story order. Every badge's `quest_id` must resolve to a main/discovery record at its original grant point. No dates are derived from GitHub activity or ages. Only reviewed owner GitHub URLs, the public Slack contribution URL, and the exact cameo URL are allowed; `github` / `public-repository` is discovery-only.

Main-card and discovery `body` values are plain text with one to eight nonempty mini-paragraphs separated by exactly `\n\n`, at most 600 characters total. Other controls and empty paragraphs fail validation. Summaries are at most 350 characters. Python prepares `paragraphs`; Jinja escapes every segment, including contextual links. Discovery positions are finite numeric coordinates within x `48..272`, y `48..132`; browser checks verify 48px targets and separation. The visible core has a 900-word budget; preserve the full source account in `docs/story.md`.

If a discovery uses `list_items`, supply 1-12 distinct plain-text strings, each 1-100 characters with no control characters or whitespace-only entries. The body plus all item text must fit within the same 600-character discovery budget. Jinja renders an escaped `<ul>`/`<li>` list after its paragraphs, including in no-JS/print output; do not embed HTML or Markdown in a body to imitate a list. Omit the field for prose-only discoveries rather than authoring an empty list.

- Exactly schema version integer `2`, five stat definitions, four 320 x 180 regions, eleven chapters, twelve stat checkpoints, and eleven uniquely granted milestones. Only chapter index 8 has two cards.
- Exact required object fields; IDs match `[a-z][a-z0-9-]{0,63}`. Source IDs/kinds, region/art/mood references, and ordered badge grants are validated.
- JSON is at most 128 KiB. Labels/IDs are at most 64 characters, headings 100, bodies 600, summaries 350, and badge/stat descriptions 220. Duplicate JSON keys, control characters, nonfinite numbers, booleans masquerading as integers, unknown targets, and colliding quest IDs fail validation.
- Every event contains all five integer 0-10 values; Experience never decreases. Milestones are granted once in their declared order. Coordinates are finite and inside the SVG, with x between 20 and 300 for object clearance. Bad authored data is rejected, not clamped.

An additional chapter, stat, region, or badge is a deliberate product/schema change, not just appending JSON. With owner approval, update validation, the architecture/story mapping, projection/client assumptions, hardcoded HUD/ledger counts, CSS slot sizing, and exact-count/snapshot/browser tests together. Preserve the no-JS equivalents and first/last checkpoint reachability. Do not loosen guardrails simply to suppress a test failure.

For art edits, use the original SVG files and inline SVG in `index.html`; region landmarks live in JSON. Keep the existing 320 x 180 scene geometry or deliberately update every consumer. Review SVG as active-capable input: no scripts, event attributes, `foreignObject`, remote references, embedded fonts, or executable URLs. Adding a runtime file may require an explicit `.dockerignore` allowlist update; broad `COPY . .` is not an acceptable shortcut.

`epilogue_scene` supplies the fixed `san-jose` region, `san-jose-home` art key, and five absolute marker positions for the ending's five beats. Python validates and copies this prose-free scene data into the projection; the renderer leaves final stats/badges untouched. Update positions together with any deliberate change to the ending beat count. The home art is a fifth scene illustration, not a fifth geographic region, and is required in both the static inventory and Docker's explicit build allowlist. The runtime boundary is 16 files.

**Development Checks**
These commands match the current tool configuration. They are required checks, not a claim that the tester's suite or CI has passed. Run at the checkout root after the Python setup above. Install Node **24 or newer** for development only:

```sh
npm ci
npm run lint
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -m 'not browser'
```

`npm run lint` runs ESLint on `app/static/story.js`, then Prettier's repository check. `npm run format` runs `prettier --write .`; `.venv/bin/ruff format .` formats Python. Prettier deliberately excludes Jinja templates in `app/templates/`; review them and exercise rendering through Python/browser tests rather than forcing an HTML formatter through Jinja syntax. Whole-project formatters can change unrelated work: use scoped formatter paths when a task permits only particular files.

```sh
npm run format
.venv/bin/ruff format .
.venv/bin/playwright install chromium firefox webkit
.venv/bin/pytest -m browser --browser chromium --browser firefox --browser webkit
```

Playwright browser installation is a development/CI download. On a Linux test runner, install the OS libraries required by the pinned Playwright version with the appropriate administrator-approved workflow; do not add them to the app image. `npm ci` installs local `axe-core` for browser accessibility audits. It is not a CDN asset or production dependency. The browser fixture starts and stops its own ephemeral loopback Flask server with access logging disabled; do not start a separate server for pytest. GitHub CI repeats the same commands on Ubuntu; local results do not substitute for its actual run status.

Required verification includes absolute snapshots and badge prefixes at every threshold, down/up/random jumps, reload/history restoration, no-JS and failed-module fallback, reduced-motion changes, enforced CSP and same-origin-only requests, empty browser storage, safe static/request boundaries, and original art review. Test Chromium/Firefox/WebKit at 320, 375, 390, 768, 1024, and 1440 CSS-pixel widths, short landscape, safe areas, 200% text enlargement, and 400% zoom/reflow. Verify HUD clearance, stable slot/card geometry, readable numeric stats, and no idle animation loop. Automated axe checks do not replace keyboard/find/selection, contrast, forced colors, print, screen-reader, and real mobile Safari/Android review. The architecture contains the full test matrix and unmeasured performance budgets.

**Security And Privacy**

Before an authorized publication, stage only reviewed public paths, then run:

```sh
.venv/bin/python tools/check_public.py --self-test
.venv/bin/python tools/check_public.py --staged
```

After committing and before pushing, run `.venv/bin/python tools/check_public.py origin/main..HEAD`. This scans every commit to be published, not just the tip. CI scans the complete index plus the push/PR range; an initial publication scans all ancestors of `HEAD`. Never stage the workspace wholesale, suppress a finding without investigation, or treat a zero count as a substitute for reviewing the public diff.

- Only the reviewed public biography is published. Name, city-level chronology, authorized personal reflections, and factual employer names are intentional; private contact PII, originals/PDFs, credentials, precise personal locations, and confidential employer material are not. Do not claim this autobiographical site contains no personal information at all.
- The owner explicitly approved publication of `pranavprem93@gmail.com` and its mailto link, LinkedIn, and the curated public project/contribution URLs. This overrides the earlier blanket email omission, not the protection of addresses, phone numbers, private repos, tokens, or NAS details. Project links are navigation, not third-party resources loaded by the application.
- `.gitignore` excludes PDFs case-insensitively and private/secret/development files. `.dockerignore` starts by denying everything and allows only reviewed runtime inputs. Docs, tests, Git metadata, `.env`, Node dependencies, and PDFs are excluded from the image build context. Ignore rules do not substitute for inspecting any future public artifact list.
- Flask keeps Jinja autoescaping, inert `tojson | forceescape` game data, exact trusted hosts, bounded request sizes, safe-directory static serving plus an inventory, and generic errors. No repository-root catch-all, ProxyFix, arbitrary forwarded-header trust, CORS, sessions, or secret key is needed.
- CSP denies everything by default, allows only same-origin scripts/styles/images/fonts, blocks connections/forms/frames/workers and inline execution, and is accompanied by nosniff, no-referrer, frame denial, and restricted permissions headers. Never weaken it for optional edge functionality. Numeric CSSOM geometry writes and SVG attributes require real-browser CSP tests.
- There are no application analytics, cookies, saved game data, third-party embeds, remote fonts, or browser telemetry. Cloudflare necessarily processes request/network metadata as transport and may retain operational/security data under the owner's account configuration. "No analytics" does not mean no third party sees requests.
- Only the connector receives the tunnel token through the owner-approved Portainer/Docker environment-metadata boundary described above. Pinned/hash-checked dependencies, least-privilege containers, restricted outbound/inbound networking, bounded logs/resources, and a patched NAS address practical supply-chain/OWASP risks. None is a promise that runtime, accessibility, privacy, or deployment tests have already passed.

**Art And Licensing**
The four city landscapes, San Jose home scene, tiny generic PLA robot, and favicon in `app/static/art/`, and the eleven inline chapter objects, mosquito/pandemic encounters, and decorative SVG marks in `app/templates/index.html`, were authored from scratch for this project by the main implementation session. The home is a fictional cutaway inspired only by the approved hobbies/homelab story; no private photo, actual floor plan, address, hardware model, or network configuration was used. The PLA robot is not the user-supplied recognizable character PNG, which was rejected and removed because it had baked-in checkerboard pixels and conflicted with the no-copied-franchise-art boundary. Badge presentation uses local decorative glyphs and text; there are no separate eleven badge image files to attribute.

No borrowed game assets, Pokemon/Fallout sprites, franchise UI, brand logos, employer screenshots, proprietary interiors, music, or downloaded font assets are included by design. Company/product names are factual text, not endorsements. Human review of originality and legibility remains part of release review.

No explicit open-source license has been chosen for the project's code, story, or original art, and there is no root project license file at this snapshot. Do not silently assign MIT, Apache, Creative Commons, or any other license. Public source visibility is not a license or a blanket permission to reuse the biography/art. Third-party dependencies retain their own licenses; their package metadata does not license this project.
