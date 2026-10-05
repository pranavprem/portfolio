**Current Handoff**
Latest working copy: the version-two story is now presented as a full-screen chapter adventure rather than a scroll essay. The redesign is implemented and locally verified but is uncommitted, has no exact-SHA hosted CI result, and is not deployed publicly.

**What Changed**

- Enhanced mode owns the usable `100dvh` viewport. The document no longer scrolls for story progression.
- Desktop uses a landscape/dialogue split. Mobile stacks HUD, landscape, dialogue, and a fixed thumb-control row.
- Start/Continue/Back buttons navigate paragraph-sized dialogue beats. Left/Right arrows, Enter/Space, and horizontal touch swipes provide equivalent controls.
- Back rewinds within the current dialogue before returning to the prior event at its final beat.
- A visible Inspect hotspot toggles optional facts and contextual project links inside the current game scene.
- Stats and the 21-item Quest log are bounded overlays. Escape closes them and restores focus; the Quest log makes the game shell inert while open.
- New screens move keyboard focus to their heading. Shortcuts ignore interactive/editable targets and modified keys.
- The title uses the opening snapshot, twelve event screens use indices `0..11`, and the epilogue holds the final event snapshot.
- Eleven inanimate chapter objects remain: controller, backpack, compass, laptop, Java mug, automation gear, books, toolkit, cloud terminal, bot console, and agent nodes. No traveler, companion, avatar, or mascot was restored.
- Scene objects move between authored landmarks with a short stepped transition. A milestone appears on the final dialogue beat with one bounded object hop and static sparks. Reduced motion removes transitions/reactions.
- The optional “Bender voice” cue was removed. The ending now says only “I'm 40% PLA.” beside the original generic robot.

**Fallback And Content**

The first server response still contains the complete story, all discoveries, links, per-card stat equivalents, milestone descriptions, ending, and optional catalog. JavaScript does not create prose. No-JS, invalid projection, failed script/stylesheet/art, and print modes restore the semantic document with in-flow landscapes.

The story/provenance contract is otherwise unchanged:

- Main dialogue remains within the 900-word editorial budget.
- Eleven chapters and twelve stat checkpoints remain fixed; chapter 09 has two events.
- Final stats remain Coding 8, Enthusiasm 10, Health 8, Charisma 7, Experience 7.
- Eleven real milestones and 21 optional grouped highlights remain.
- The detailed Einstein Bots/Copilot/Agentforce account, source qualifications, private-PDF boundary, current projects, and authorized links remain intact.
- `docs/story.md` remains the complete public-safe source ledger; runtime JSON is only the curated selection.

**Local Verification**

Environment: macOS arm64, Python 3.13.14, pytest 9.1.1, Node 24.20.0/npm 11.19.0, Playwright 1.62.0 with Chromium 151.0.7922.34, Firefox 153.0, and WebKit 26.5. Docker client/server 29.7.2 and Compose 5.5.0 were used for the final local container check.

| Check                                                                               | Actual outcome                                                                                                       |
| ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `npm run lint`                                                                      | Passed after scoped Prettier formatting of CSS/JS.                                                                   |
| `.venv/bin/ruff check .`                                                            | Passed.                                                                                                              |
| `.venv/bin/ruff format --check .`                                                   | Passed after formatting the rewritten browser test.                                                                  |
| `.venv/bin/pytest -m 'not browser'`                                                 | **177 passed**, no selected skips.                                                                                   |
| `.venv/bin/pytest -m browser --browser chromium --browser firefox --browser webkit` | **108 passed**, 36 per engine, no selected skips.                                                                    |
| Local Compose parsing                                                               | Base + local passed.                                                                                                 |
| Production Compose parsing                                                          | Base + tunnel passed with an explicitly synthetic token.                                                             |
| Local container rebuild                                                             | `portfolio-portfolio-1` rebuilt and became healthy.                                                                  |
| Runtime boundary                                                                    | Exactly 15 approved files; UID/GID 10001; app content nonwritable; `/tmp` writable; no PDFs/secrets/env/cache files. |
| Local health                                                                        | `http://127.0.0.1:8000/healthz` returned `{"status":"ok"}`.                                                          |
| Local release assets                                                                | Current digest-versioned CSS/JS and strict application security headers were served.                                 |

Browser coverage now exercises:

- every forward event transition and exact snapshot/badge prefix
- dialogue-beat progression and rewind behavior
- Inspect discovery toggling
- keyboard guards and horizontal touch swipes
- Stats and Quest log visibility, inert state, Escape, and focus restoration
- 320x568, 390x844, 768x1024, and 1440x1000 viewport fit
- at least 48px game-control targets and no page/horizontal scrolling
- no-JS and failed JS/CSS/art behavior
- ten malformed projection cases
- reduced motion, forced colors, text enlargement, print, and selection
- axe WCAG A/AA checks in light/dark at mobile/desktop sizes
- CSP, same-origin requests, empty cookies/storage, and no idle animations

**Visual Review**

Main-session Chromium captures were inspected at 390x844 dark mobile and 1440x1000 light desktop for the title and college scenes.

- Mobile contains the HUD, complete landscape, current object, chapter dialogue, beat count, Back, and Continue in one screen.
- Desktop gives the landscape and dialogue equal game-level presence rather than placing prose below decorative art.
- The first capture exposed a startup stats-panel flash and a hidden Inspect button overridden by author CSS. Removing the close transition and enforcing `[hidden]` fixed both; recaptured title screens show neither defect.
- College dialogue is one short beat at a time. Seven independent beats remain separate without presenting a wall of text.
- These captures support local visual review, not physical-phone/browser-chrome approval.

**Code And Security Review**

- No new server route, dependency, remote asset, secret access, storage, analytics, or CSP relaxation was added.
- The inert projection remains prose-free and autoescaped in a quoted data attribute.
- Runtime code does not use `innerHTML`, eval/string execution, fetch, WebSocket, beacon, cookies, or browser storage.
- Navigation indices are bounded. Touch input uses distance and direction checks. Keyboard input ignores modified and interactive/editable targets.
- Closed overlays are inert and assistive-hidden. The Quest log prevents background interaction while open.
- The app remains GET/HEAD-only with exact trusted hosts, bounded requests, allowlisted static serving, generic errors, sanitized logs, deterministic asset digests, and strict application headers.
- The Docker app remains nonroot/read-only with no secret access and no production host port.
- Remaining risks are manual device/screen-reader validation, deployment correctness, Cloudflare redirect/HSTS sequencing, NAS network isolation, and recovery practice.

**Architecture Conformance**

The final implementation matches the revised [architecture](architecture.md): full-screen linear screens, server-rendered fallback, absolute event snapshots, no persistence, guarded buttons/keyboard/swipes, optional discoveries/overlays, mobile-first viewport fit, original object-only art, reduced motion, and unchanged HTTP/security boundaries.

Intentional simplifications:

- There is no avatar movement or collision system. The user selected a chapter adventure over direct movement.
- The current Inspect hotspot has a consistent screen position rather than authored per-scene coordinates. It still reveals scene-specific content.
- Dialogue may internally scroll only when enlargement or viewport constraints require it; normal tested phone sizes fit the active beat.

**Repository And Deployment State**

- Branch: `main`; remote: `https://github.com/pranavprem/portfolio.git`.
- Last known pushed commit before this redesign: `714ab78dfcfb649f1ec9d9dc42107c86fde32d5c` (`feat: stack game stage above story`).
- Exact hosted run for that older commit passed: [37175855753](https://github.com/pranavprem/portfolio/actions/runs/37175855753).
- This chapter-adventure redesign is currently uncommitted and therefore has no hosted CI run.
- On 2026-10-04, a browser-like HTTPS request returned `200` but still served the previous unversioned JS/CSS and masthead-era layout. It does not contain this redesign or an HSTS header. A default Python `urllib` user agent received an edge `403`, so bot/challenge behavior also needs rechecking after deployment.
- Plain HTTP returned `200` instead of redirecting on the same check. Keep `PORTFOLIO_HSTS=0`.
- The Portainer stack uses repository `https://github.com/pranavprem/portfolio.git`, reference `refs/heads/main`, and exactly `compose.yaml` plus `compose.tunnel.yaml`. Never add `compose.local.yaml` or expose the tunnel token.

**Remaining Work**

1. Obtain explicit authorization before committing/pushing this redesign; project instructions do not permit an implicit commit.
2. Run hosted CI for the exact resulting SHA and require all four jobs to pass.
3. Pull/redeploy that revision in the existing Portainer Git stack without changing or exposing `CLOUDFLARED_TOKEN`.
4. Verify public HTML uses the new digest-versioned CSS/JS and that public bytes match the deployed commit.
5. Verify public chapter navigation, mobile rendering, `/healthz`, CSP/security headers, and absence of edge-injected scripts/challenges.
6. Configure and verify Cloudflare HTTP-to-HTTPS redirect. Only then set `PORTFOLIO_HSTS=1` and verify exactly `max-age=31536000`.
7. Run physical iOS Safari/Android checks for safe areas/browser chrome, native zoom, touch swipes, and representative performance.
8. Run a real screen-reader pass and rehearse rollback, connector reconnection, token rotation, egress outage, and protected backups.
9. Verify NAS CPU/Compose behavior and connector firewall isolation, including inability to reach unrelated NAS administration.

No database or app volume requires migration. `www` behavior and an open-source/art license remain intentionally unchosen.
