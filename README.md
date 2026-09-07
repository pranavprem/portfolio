**Pranav Prem**
A life in side quests: a warm, original pixel-game autobiography for `pranavprem.com`, built with Python rather than a frontend application platform.

The point is to meet a person, not browse a resume with animations. The route follows curiosity in Goa, an unwanted detour, college independence, Java expertise and boredom in Pune, renewed challenge at SJSU, discovering developer productivity at Google Hardware/Nest, useful Salesforce work and burnout, and present-day enthusiasm for building helpful agentic systems. Hobbies, small projects, humor, and ordinary human limits belong alongside professional milestones. The ending is an open path, not a victory screen or a contact funnel.

Source repository: `https://github.com/pranavprem/portfolio` (public, owner-approved). The application is implemented and tested locally: 143 Python/content/HTTP tests and 99 browser cases across Chromium, Firefox, and WebKit pass. The hardened Docker app builds and runs on loopback. **The public domain is not deployed by this checkout:** Cloudflare tunnel provisioning and actual NAS verification remain operator steps. See [the handoff](docs/handoff.md) for dated evidence, publication status, and remaining checks.

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

**The Experience**

- Native vertical document scrolling is the only application interaction. Down advances; up rewinds. There are no visible links, buttons, menus, forms, downloads, clickable badges, contact controls, or hover-only story reveals. Documentation links and HTML resource/canonical `<link>` elements are not website navigation.
- Wheel, touch, trackpad, scrollbar, keyboard scrolling, selection, find-in-page, zoom, and browser navigation remain native. There is no scroll hijacking, mandatory snapping, custom game keyboard input, or horizontal game scroller.
- Eleven chapters span four original regions: Goa, Pune, San Jose, and the Bay Area. Chapter 09 has separate contribution and burnout cards, giving twelve checkpoints. The closing horizon and ledger are not a twelfth chapter.
- A top-right desktop character sheet sits above the landscape. Narrow screens use in-flow landscapes and a compact HUD. Readability takes priority over fixed positioning on short or heavily enlarged viewports. Automated width/text-reflow checks pass; actual phone safe areas and native zoom still need device review.
- Every paragraph, fact, chapter stat snapshot, and badge ledger is server-rendered. Without JavaScript, the complete story remains available and the sheet is labeled as opening stats, not live progress. Reduced motion retains discrete chapter/stat changes without walking interpolation. Nothing should move while scrolling is idle.
- Cream paper, green ink, amber details, system serif headings, segmented meters, an original traveler, and an original companion provide the game language. No borrowed game assets, employer logos, remote fonts, sound, combat, or game proficiency are involved.

The six integer meters run from 0 through 10. They are fictional narrative shorthand, not medical measurements, certifications, or objective assessments. The Health concept uses the internal key `vitality`; do not introduce a seventh meter.

| JSON Key     | Full / Compact Label | Opening | Meaning                                                                  |
| ------------ | -------------------- | ------- | ------------------------------------------------------------------------ |
| `coding`     | Coding / Code        | 0       | How stretched the coding muscle feels; a dip is not forgotten knowledge. |
| `enthusiasm` | Enthusiasm / Spark   | 1       | Appetite for the current quest.                                          |
| `vitality`   | Health / HP          | 1       | Playful adventure energy, never a clinical score.                        |
| `charisma`   | Charisma / Charm     | 1       | Confidence collaborating, teaching, and leading.                         |
| `automancy`  | Automancy / Auto     | 0       | Making repetitive work disappear.                                        |
| `sidequests` | Side quests / Quests | 1       | Room for experiments and hobbies, not a project count.                   |

The eleven story badges, in grant order, are First Script, C/C++ Unlocked, House Captain, Python Passport, Java Topper, Time Returned, Cloud Scholar, Developer Ally, Chat Alchemist, Bot Builder, and Principal. The opening has zero earned badges. All eleven HUD slots are reserved, but future badges must not appear earned. Badges are noninteractive story symbols; some labels name real roles, not official game awards.

State is a pure function of reading position. Each card supplies an absolute six-stat `stats_after` snapshot; Python prepares its complete cumulative `badges_after` prefix. The browser selects the last checkpoint at or above a reading line 35% down the unobscured reading area. Equality selects the later checkpoint. It never adds XP to previous DOM state. Large jumps, reload restoration, and repeated crossings must give the same result. Burnout preserves earlier achievements; rewinding before a badge's grant removes it. Nothing is saved in cookies, browser storage, a session, or a database.

**Small System**

```text
Public browser -- HTTPS --> Cloudflare edge
                             |
                      outbound-established tunnel
                             |
                      cloudflared connector
                             |
                    HTTP http://app:8000
                    private Docker origin bridge
                             |
                    Gunicorn -> Flask -> Jinja
                             |
                  validated local story.json

HTML + local CSS/JS/SVG -> reading-position enhancement in the browser
No scroll state is sent back to the server.
```

Runtime is Python 3.13, Flask, Jinja, and Gunicorn, with one small vanilla JavaScript module. There is no runtime Node/npm, frontend build step, framework, database, CMS, queue, analytics, remote API, or cloud service dependency except Cloudflare for public transport. Installing dependencies and pulling images are build/development network operations, not runtime application services. Node 24+ and Python Playwright are development-only tools.

| HTTP Surface     | Contract                                                                                                                                                                            |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/`              | GET/HEAD, complete HTML, fixed canonical `https://pranavprem.com/`, `Cache-Control: no-cache`.                                                                                      |
| `/healthz`       | GET/HEAD, `{"status":"ok"}` with a trailing newline on GET, `Cache-Control: no-store`.                                                                                              |
| `/static/<path>` | GET/HEAD, approved inventory under `app/static/` only; conditional serving and `max-age=3600`, not immutable caching.                                                               |
| Errors           | Generic handled 400/404/405/413/500 pages with security headers and no reflected request details; unsupported methods retain `Allow`. Earlier Gunicorn/proxy rejections can differ. |

There is no public state API, authentication, admin endpoint, upload, or contact form. Requests do not customize the story. Content and templates are loaded/validated at startup, not fetched or reparsed per visitor.

**File Map**

| Path                                                                       | Edit Or Inspect For                                                                                                                                       |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app/__init__.py`                                                          | `create_app()`, exact trusted hosts, HTTP routes, security/cache headers, bounded requests, safe application/Gunicorn exception logging.                  |
| `app/content.py`                                                           | JSON validation, `ContentValidationError`, public game projection, static inventory.                                                                      |
| `app/content/story.json`                                                   | Curated runtime prose, source references, six meters, eleven badges, region geometry, and absolute event snapshots. Not the full narrative archive.       |
| `app/templates/base.html`                                                  | Metadata, local resources, document shell.                                                                                                                |
| `app/templates/index.html`                                                 | Server-rendered story, HUD, inline traveler/companion, per-card snapshots, ledger, and additional editorial copy. Some copy is here, not in JSON.         |
| `app/templates/error.html`                                                 | Independent, noninteractive error page.                                                                                                                   |
| `app/static/story.css`                                                     | Warm visual language, responsive HUD/theater, reduced motion, forced colors, print.                                                                       |
| `app/static/story.js`                                                      | Exported `deriveState()`, projection/marker checks, geometry, passive scroll/rAF controller, DOM/SVG rendering, fallback. Region captions also live here. |
| `app/static/art/`                                                          | Original `goa.svg`, `pune.svg`, `san-jose.svg`, `bay-area.svg`, and `favicon.svg`.                                                                        |
| `requirements.txt`, `requirements-dev.txt`                                 | Exact, hash-locked Python runtime and development dependency closures. The dev lock includes runtime dependencies.                                        |
| `pyproject.toml`                                                           | Ruff and pytest configuration; the `browser` marker is registered here.                                                                                   |
| `package.json`, `package-lock.json`, `eslint.config.js`, `.prettierignore` | Development-only ESLint, Prettier, and local `axe-core`. Jinja templates are excluded from Prettier.                                                      |
| `Dockerfile`, `.dockerignore`                                              | Pinned Python image, runtime-only installation, startup validation, explicit copies and deny-by-default build context.                                    |
| `compose.yaml`                                                             | Hardened app and internal origin network; no published port.                                                                                              |
| `compose.local.yaml`                                                       | Explicit loopback-only development override; no connector or token requirement.                                                                           |
| `compose.tunnel.yaml`                                                      | Pinned nonroot connector, outbound network, file-backed secret, no retained connector logs or published ports.                                            |
| `.env.example`, `.gitignore`                                               | Nonsecret configuration example and private/development file exclusions.                                                                                  |

`tests/conftest.py` supplies independent expected snapshots, content fixtures, and an ephemeral loopback server. `test_content.py`, `test_http.py`, and `test_browser.py` exercise the authored-data boundary, public HTTP surface, and real-browser behavior. `.github/workflows/ci.yml` runs lint/Python checks and three separate browser-engine jobs with read-only permissions and commit-pinned actions. Hosted CI status is recorded in the handoff separately from local results.

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
docker compose -f compose.yaml -f compose.local.yaml up -d --build --wait app
docker compose -f compose.yaml -f compose.local.yaml ps
```

Open `http://127.0.0.1:8000/`. No `.env`, token, or Cloudflare variable is needed because the tunnel file is not loaded. Port 8000 is published only on loopback. Stop the Python development server first if it already owns that port.

This runs Gunicorn with the same nonroot/read-only hardening as production. Re-run the `up` command after edits; there is no source bind mount or automatic rebuild. To stop and remove this local stack:

```sh
docker compose -f compose.yaml -f compose.local.yaml down
```

Never add `compose.local.yaml` to production, rename it to an automatically loaded override, or bind-mount the PDF-containing workspace into a container.

**Configuration**
All four values in `.env.example` are nonsecret configuration or file paths. The tunnel token itself has no environment-variable setting in this deployment.

| Name                     | Allowed / Default Value                                                                           | Effect                                                                                                                                                                                                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PORTFOLIO_ENV`          | `development` or `production`; direct Python defaults to `development`.                           | Production trusts `pranavprem.com` and `127.0.0.1`; development also trusts `localhost`. The literal `local` is invalid. Base Compose hardcodes `production`; the local override hardcodes `development`. An env-file value does not override those Compose literals. |
| `PORTFOLIO_HSTS`         | Exactly `0` or `1`; default `0`.                                                                  | Only production plus `1` adds `Strict-Transport-Security: max-age=31536000`. The local override forces `0`. Enable only after verifying public HTTPS and the edge redirect.                                                                                           |
| `CLOUDFLARED_TOKEN_FILE` | No default; an absolute protected host file path, required only when loading the tunnel override. | Compose mounts that file read-only at `/run/secrets/cloudflared_token` in `cloudflared` alone. This variable is a path, never a token value.                                                                                                                          |
| `CLOUDFLARED_IMAGE`      | Optional reviewed release tag plus verified digest; pinned default shown below.                   | Selects the connector image. Do not replace it with floating `latest` or an unverified digest.                                                                                                                                                                        |

The app does not load `.env` itself, and `python-dotenv` is not a dependency. Direct Python uses process environment. Compose uses `.env` or an explicit `--env-file` for interpolation, not as a blanket container environment import. Existing shell variables can take precedence over env-file interpolation; check the intended deployment configuration in a clean operator shell.

For production, use an administrator-controlled env file outside the checkout, for example `/absolute/protected/portfolio.env`, with these nonsecret values. Replace the placeholder path with the actual private host path; do not paste credentials into it:

```dotenv
PORTFOLIO_ENV=production
PORTFOLIO_HSTS=0
CLOUDFLARED_TOKEN_FILE=/absolute/protected/cloudflared-token
CLOUDFLARED_IMAGE=cloudflare/cloudflared:2026.8.3@sha256:51c9cefcb4569df44e1ad403ab1d3d8065aa8e84339bcfc6aee75502e1140339
```

The first line documents intent; base Compose already sets that mode. The last line may be omitted to use the identical pinned default in `compose.tunnel.yaml`. Paths are not credentials but can expose NAS details; keep the actual env file out of Git. No Flask secret key, Cloudflare account API key, visitor tracking ID, or database URL is needed.

**NAS Prerequisites**
Production targets a Linux NAS with Docker Compose v2 and either `linux/amd64` or `linux/arm64`. Determine the actual CPU, Engine/Compose versions, available memory, rootless/user-namespace configuration, ACL behavior, and firewall policy first. `x86_64` usually corresponds to amd64; `aarch64` to arm64. Do not force an incompatible `platform` or assume a 32-bit NAS is supported.

The Python base is pinned to `python:3.13.15-slim-bookworm@sha256:ed86c82274b3c69b52fb5820f358f0bd7df0b603332063cb5c6e32bd220c3e6e`. The connector pin is shown above. Their multi-architecture manifest verification is recorded in the Dockerfile/Compose comments and `.env.example` on 2026-09-06, including amd64/arm64 support. This pass inspected those references, not a fresh registry query. Manifest support is not execution evidence: neither actual NAS architecture, NAS permissions, nor a live tunnel has been tested by this documentation pass.

The app runs as `10001:10001`, with root-owned read-only application files, two synchronous Gunicorn workers, a small `/tmp` tmpfs, all capabilities dropped, and no-new-privileges. It joins only the internal origin network and has no persistent volume. The connector runs as `65532:65532` with similar restrictions and joins both origin and outbound egress networks. Resource limits and lifecycle settings are in Compose; validate them on the NAS rather than granting root or privileged access when something fails.

No production host ports are published. Dockerfile `EXPOSE` and Compose `expose` document the internal port; they are not host-port publication or a complete firewall. No router inbound port forwarding is required. Allow the connector DNS access and outbound UDP/TCP 7844 to Cloudflare's current documented tunnel destinations. QUIC uses UDP; HTTP/2 fallback uses TCP. Restrict access from the connector network to NAS management and unrelated LAN services. The Docker host/administrator remains privileged; an internal bridge is not isolation from the host itself.

**Create The Tunnel**
Prerequisites are owner-controlled Cloudflare zone/DNS access for `pranavprem.com`, active edge TLS, and an operator who can securely provision the tunnel file. No token was supplied for this documentation task; the following is a runbook, not a record of completed dashboard work.

1. In the Cloudflare dashboard's tunnel/connectors area, create a remotely managed Cloudflare Tunnel for this portfolio. Dashboard labels can change; use the Cloudflared connector type, not a private-network route. Do not execute a wizard command containing a token literal.
2. Obtain the token for this specific tunnel through the protected dashboard workflow and place it in the external file described below. Do not provision an account-wide certificate, API key, or local ingress `config.yml`.
3. Add a published application/public hostname route for exactly `pranavprem.com`, covering the whole path without prefix rewriting. Service type is HTTP and service URL is `http://app:8000`, not the NAS address, `localhost`, or HTTPS.
4. Under origin HTTP settings, set **HTTP Host Header** to `pranavprem.com`. Leave HTTP/2-to-origin off. Do not add `noTLSVerify`; this private origin hop is intentionally HTTP. The connector resolves `app` on the shared Compose network.
5. Let the dashboard create the proxied tunnel DNS route for the apex. Resolve conflicting apex A/AAAA/CNAME records as appropriate; DNS must route through the tunnel, not reveal a public NAS IP. Do not add wildcard hostnames or NAS-management routes. `www` behavior is not chosen and must not be guessed.
6. Enable public edge HTTPS and an edge HTTP-to-HTTPS redirect for the hostname. Do not add a Flask `request.is_secure` redirect: the HTTP bridge hop would risk a redirect loop. There is no need for another Nginx/ACME service.
7. Disable optional HTML/JavaScript injection for this hostname: Rocket Loader, Web Analytics, Browser Insights/beacons, email obfuscation, and similar transformations. Review challenge and JavaScript-detection rules so ordinary visits do not require injected code, a login, or a click-through challenge. Keep infrastructure DDoS protection; do not weaken CSP to accommodate optional edge features.
8. Publish only the intended hostname route, with unmatched routes returning the tunnel's 404 behavior. Do not place a Cloudflare Access login gate on this public story. Verify the actual public response after startup, including local assets and the absence of injected scripts.

Official operational references: [remote tunnel creation](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/get-started/create-remote-tunnel/), [origin parameters](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/origin-parameters/), and [current firewall requirements](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/tunnel-with-firewall/). These are documentation links, not runtime dependencies.

**Protect The Token**
Use a dedicated administrator-controlled directory outside every checkout and build context. With a secure editor or credential-provisioning workflow, store only the raw tunnel token in the host file, not the dashboard's entire Docker command or a `TUNNEL_TOKEN=` assignment. Avoid editor backups/swap files in unprotected locations. Never put the token value in environment variables, CLI arguments, shell history, Compose YAML, Git, images, screenshots, logs, or public support requests. Do not print it with `cat`, dump container environments, or collect secret contents for troubleshooting.

Ordinary rootful Linux file-backed Compose secrets are read-only bind mounts, not encrypted secret storage. Host ownership and permissions matter. For a verified, non-remapped Linux Docker installation, one possible arrangement is a root-owned protected directory and a root-owned token file readable only by the connector's protected group:

```sh
sudo chmod 0700 "/absolute/protected"
sudo chown root:65532 "/absolute/protected/cloudflared-token"
sudo chmod 0440 "/absolute/protected/cloudflared-token"
```

These are example permission changes for an already provisioned, dedicated directory/file, not commands to run against an arbitrary shared NAS directory. Another valid mapping can be owner `65532:65532` with file mode `0400`, beneath an administrator-protected host directory. Do not grant unrelated users membership in the readable group. Confirm the actual NAS ACLs and user mapping before selecting either recipe.

For file sources, Compose secret `uid`, `gid`, and `mode` attributes do not repair host permissions. A root-owned `0600` token can be unreadable to the connector. Never solve that with `chmod 777`, world-read permission, root execution, extra capabilities, host networking, or a Docker socket mount. Docker Desktop bind-mount behavior does not prove the same permissions will work on a Linux NAS; rootless Docker, user namespaces, NFS/SMB shares, and vendor ACLs require their own least-privilege mapping.

Verify existence, nonzero size, ownership/mode/ACL metadata, and connector startup without displaying contents. The app must have no token mount. Rotate an exposed/revoked token in Cloudflare, securely replace the host file, then **recreate** the connector. A restart alone can keep a bind mount attached to the old inode after an atomic file replacement. Keep any secret backup encrypted, restricted, and separate from public-source backups.

**Production Run**
From the reviewed release checkout, use a stable Compose project name, the external env file, and exactly the base plus tunnel files. Start both services explicitly:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml config --quiet
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml up -d --build --wait app cloudflared
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
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml build --pull app
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml up -d --wait app cloudflared
```

4. Recheck app health, tunnel status, public root/health/assets, TLS redirect, CSP, and a down/up browser journey. Record actual outcomes in the handoff. Brief downtime is possible; one NAS and one connector are not high availability.

To roll back, prepare another separate checkout at the recorded **known-good full commit**, or use the retained untouched release checkout. Do not rewrite the active worktree with `git reset --hard`, overwrite unrelated work, or cherry-pick a guessed inverse of changes. Review that release's Compose files against the current protected env/token, then run the full production `up -d --build --wait app cloudflared` command from that checkout with the same `--project-name portfolio`. Re-verify public behavior. If rebuilding is unavailable, use the retained app image with an explicitly reviewed image-selection override; merely tagging an image does not make the existing `build: .` Compose file select it. Test that emergency path before relying on it.

There is no database, migration, uploaded media, or persistent app volume to restore. Back up reviewed public source/content/art, lockfiles, release/image identifiers, and protected operational configuration. Do not archive the whole local workspace into the public backup: it contains private originals and development artifacts. Token recovery is a separate restricted/encrypted backup or Cloudflare re-provisioning workflow. Preserve dashboard routing/security settings in protected operator records, not secret-bearing screenshots in Git.

After token rotation, force recreation rather than only restart:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml up -d --force-recreate --wait app cloudflared
```

Docker's restart policy restarts exited processes, not merely unhealthy containers. A wedged live app needs diagnosis/operator action; do not introduce an auto-heal service with Docker socket access.

**Troubleshooting**
Use synthetic requests, container state, the exact safe health response, filesystem metadata, and dashboard tunnel status. Do not collect token contents, visitor query/header canaries containing real PII, raw environment dumps, private documents, or debug logs.

| Symptom                                             | Check And Safe Correction                                                                                                                                                                                                                                                        |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ContentValidationError` or build/startup fails     | Fix the named public JSON field or missing/unsafe asset. Full snapshots, exact release counts, plain text limits, and safe inventory rules are deliberate. Do not bypass validation to get a green container; restore the previous release if needed.                            |
| Invalid environment value                           | Use `development`/`production` and HSTS `0`/`1`. `PORTFOLIO_ENV=local` is invalid. Check shell overrides and remember Compose modes are hardcoded.                                                                                                                               |
| Local port unavailable                              | Stop another loopback server using port 8000; use either Flask or local Docker, not both. Production intentionally has no localhost-published port. Do not add the local override to troubleshoot a public deployment.                                                           |
| App unhealthy                                       | Inspect `ps` health state and safe application error categories; check startup validation, memory/PID limits, and read-only/tmpfs configuration. A healthy process does not guarantee rendered art or a working tunnel.                                                          |
| HTTP 400 with healthy loopback probe                | Check Host routing. Production accepts only `pranavprem.com` and `127.0.0.1`; `app`, a NAS IP, and `www` are not trusted hosts. Set the tunnel's origin HTTP Host Header to `pranavprem.com`, not a wildcard in Flask. Do not add ProxyFix or trust arbitrary forwarded headers. |
| Tunnel config demands `CLOUDFLARED_TOKEN_FILE`      | Supply the absolute protected file path in the external env file. A token was not provided with the project. Local work needs only base + local Compose and no dummy credential.                                                                                                 |
| Token missing, empty, unreadable, or revoked        | Check the file and read-only mount metadata, actual UID/GID 65532 mapping, host ACLs, and tunnel identity. Correct least-privilege access or rotate/recreate through Cloudflare. File-secret YAML mode fields and world-read permission are not fixes.                           |
| Disconnected tunnel / Cloudflare 1033               | Check the connector process, credential lifecycle, NAS connectivity, and dashboard connector status. If not connected, origin health cannot make the public route available.                                                                                                     |
| Tunnel connected but origin error / 502             | Verify both services share the origin network and the route is exactly HTTP `http://app:8000`, with the fixed Host header and no path rewriting. `localhost` inside the connector is not the app.                                                                                |
| DNS error or wrong site                             | Check the active Cloudflare zone, proxied apex tunnel record, conflicting records, hostname route, and propagation. Do not point DNS at a public NAS IP or invent `www` behavior.                                                                                                |
| QUIC timeouts or reconnect loops                    | Check DNS and current Cloudflare destination rules for outbound UDP 7844 and TCP 7844 fallback. The connector needs the egress network; the app does not. ICMP-proxy warnings do not justify NET_RAW, NET_ADMIN, root, or privileged mode for this HTTP tunnel.                  |
| CSP failures, challenge page, or unexpected scripts | Inspect public HTML/network behavior against the local origin. Disable optional edge injection/challenges for normal visits; do not add `unsafe-inline`, `unsafe-eval`, remote script domains, or click-through UI.                                                              |
| No connector logs retained                          | Intentional: `logging: driver: none` remains until a synthetic privacy canary verifies the pinned connector. Use state and dashboard diagnostics. Never enable debug logging or retain request-bearing output just to get more information.                                      |
| Scene/HUD falls back or shows old assets            | Confirm JS/CSS/SVG responses and CSP, revalidate HTML, and account for the one-hour unversioned asset cache. Purge affected edge assets if needed. Preserve readable fallback; do not force a stale live HUD, storage reset, or scroll-to-top behavior.                          |
| Browser tests missing/fail to collect               | Confirm `tests/`, the `browser` marker, dev dependencies, and installed Playwright engines. The fixtures start their own loopback server. Zero collected tests, missing executables, or an unrun suite are not passes.                                                           |

If the origin must be probed without publishing a port, the app container has Python:

```sh
docker compose --project-name portfolio --env-file "/absolute/protected/portfolio.env" -f compose.yaml -f compose.tunnel.yaml exec -T app python -c "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2); print(r.status, r.read().decode().strip())"
```

This prints only a synthetic status and the intentionally minimal health body, not a credential or diagnostic dump. Retained app logs are bounded to 5 MB x 2 files; custom exception loggers emit safe categories/correlation IDs. Logging privacy still requires a synthetic canary check. Do not assume all possible server/connector failures are proven private merely because the normal code is restrictive.

**Editing The Story**
Use `docs/story.md` as the complete source, `docs/architecture.md` for the approved presentation/technical contract, and `app/content/story.json` for the runtime selection. The source ledger must survive editorial shortening. Do not reopen, modify, serve, or require the private PDFs. The lead already read them with the owner's permission and preserved sanitized evidence; that does not make their claims independently verified.

The architecture's explicit owner clarifications supersede older suggestions to omit the numeric school/course results or seek permission again. Publish Profile's national top 0.01% Class 12 computer science result, without inventing an exact rank or exam board. Preserve the first-person 110%, maximum-possible, sole-student recollection without inventing an extra-credit mechanism or an all-time institutional record. Use national top ten for the conflicting IEEE seventh/eighth claims, and `2019` for the conflicting Salesforce January/March joining month. Keep both source claims in the ledger.

The approved architecture carries owner-supplied Chat 2019-2021, burnout 2020-2021, and Copilot 2023 chronology; do not relabel these as PDF corroboration. Do not derive product-transition dates from promotions, move the Google internship after the MS, infer a birth year from ages, give exact GRE/TOEFL scores, attribute the Green Belt's 2,000+ hours to TasKing, or manufacture medical/recovery details. Current enthusiasm, drive, knowledge, and team understanding belong explicitly in the prose even when a fictional meter ties an earlier 10/10.

For an ordinary copy change, edit plain text in the appropriate JSON card while preserving its `source_refs`. Also inspect template-only prose, milestone callouts, opening/ending text, and duplicated region captions in Jinja/JS; JSON is not the only current text source. Never use executable Markdown/HTML, template evaluation, `|safe`, or JavaScript injection to format a card.

Current authoring guardrails in `app/content.py` are intentionally stricter than a generic chapter engine:

- Exactly schema version integer `1`, six stat definitions in fixed order, four ordered 320 x 180 regions, eleven chapters, twelve cards/checkpoints, and eleven uniquely granted badges. Only chapter index 8 has two cards.
- Exact required object fields; IDs match `[a-z][a-z0-9-]{0,63}`. Source IDs/kinds, region/art/mood references, and ordered badge grants are validated.
- JSON is at most 128 KiB. Labels/IDs are at most 64 characters, headings 100, bodies 600, facts/descriptions 220, with at most three facts per card. Duplicate JSON keys, control characters, nonfinite numbers, and booleans masquerading as integers fail validation.
- Every event contains all six integer 0-10 values. Badges are granted once and the ledger follows first-grant order. Coordinates are finite, inside the SVG, with x between 20 and 300 to leave sprite room. Invalid authored data is rejected, not silently clamped.

An additional chapter, stat, region, or badge is a deliberate product/schema change, not just appending JSON. With owner approval, update validation, the architecture/story mapping, projection/client assumptions, hardcoded HUD/ledger counts, CSS slot sizing, and exact-count/snapshot/browser tests together. Preserve the no-JS equivalents and first/last checkpoint reachability. Do not loosen guardrails simply to suppress a test failure.

For art edits, use the original SVG files and inline SVG in `index.html`; region landmarks live in JSON. Keep the existing 320 x 180 scene geometry or deliberately update every consumer. Review SVG as active-capable input: no scripts, event attributes, `foreignObject`, remote references, embedded fonts, or executable URLs. Adding a runtime file may require an explicit `.dockerignore` allowlist update; broad `COPY . .` is not an acceptable shortcut.

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

- Only the reviewed public biography is published. Name, city-level chronology, authorized personal reflections, and factual employer names are intentional; private contact PII, originals/PDFs, credentials, precise personal locations, and confidential employer material are not. Do not claim this autobiographical site contains no personal information at all.
- `.gitignore` excludes PDFs case-insensitively and private/secret/development files. `.dockerignore` starts by denying everything and allows only reviewed runtime inputs. Docs, tests, Git metadata, `.env`, Node dependencies, and PDFs are excluded from the image build context. Ignore rules do not substitute for inspecting any future public artifact list.
- Flask keeps Jinja autoescaping, inert `tojson | forceescape` game data, exact trusted hosts, bounded request sizes, safe-directory static serving plus an inventory, and generic errors. No repository-root catch-all, ProxyFix, arbitrary forwarded-header trust, CORS, sessions, or secret key is needed.
- CSP denies everything by default, allows only same-origin scripts/styles/images/fonts, blocks connections/forms/frames/workers and inline execution, and is accompanied by nosniff, no-referrer, frame denial, and restricted permissions headers. Never weaken it for optional edge functionality. Numeric CSSOM geometry writes and SVG attributes require real-browser CSP tests.
- There are no application analytics, cookies, saved scroll data, third-party embeds, remote fonts, or browser telemetry. Cloudflare necessarily processes request/network metadata as transport and may retain operational/security data under the owner's account configuration. "No analytics" does not mean no third party sees requests.
- Secrets belong only to the connector's file mount. Pinned/hash-checked dependencies, least-privilege containers, restricted outbound/inbound networking, bounded logs/resources, and a patched NAS address practical supply-chain/OWASP risks. None is a promise that runtime, accessibility, privacy, or deployment tests have already passed.

**Art And Licensing**
The four SVG landscapes and favicon in `app/static/art/`, and the inline traveler, portrait, companion, and decorative SVG marks in `app/templates/index.html`, were authored from scratch for this project by the main implementation session. The original companion's working design name is Tidebit; it is not a borrowed franchise character or a claim of trademark clearance. Badge presentation currently uses local decorative glyphs and text; there are no separate eleven badge image files to attribute.

No borrowed game assets, Pokemon/Fallout sprites, franchise UI, brand logos, employer screenshots, proprietary interiors, music, or downloaded font assets are included by design. Company/product names are factual text, not endorsements. Human review of originality and legibility remains part of release review.

No explicit open-source license has been chosen for the project's code, story, or original art, and there is no root project license file at this snapshot. Do not silently assign MIT, Apache, Creative Commons, or any other license. Public source visibility is not a license or a blanket permission to reuse the biography/art. Third-party dependencies retain their own licenses; their package metadata does not license this project.
