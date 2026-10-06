**Current Handoff**
The current work is the chronological, revisitable Quest log revision, including the accumulated HUD, encounter, voice, and pacing changes after `7b5339e`. The owner explicitly authorized commit and push after verification. That does not authorize or establish a Portainer/public redeployment. Publication and exact-SHA CI evidence are recorded below when observed.

**Current Experience**

- The full-screen linear adventure retains eleven chapters, twelve stat checkpoints, five always-visible meters, and the final `8, 10, 8, 7, 7` sheet. Start/Continue/Back, guarded keyboard input, and horizontal swipes work without document-scroll progression.
- College has four main beats; leadership, Zuari, and the paper are optional. Automation has two main beats; Green Belt and separate CI/CD savings are optional. The school story explicitly places computer science in 11th/12th grade and says **being house captain** introduced leadership, speaking, and debate.
- Optional prose appears once in a scene popup and is summarized again only in the Quest log. Repeated main-scene reward paragraphs are removed. Milestones keep their decorative feedback and absolute prefix; their descriptions are in the log. No discovery changes stats or gates the route.
- There are eleven discoveries: GEC extras; early games/CyanogenMod; Green Belt/CI-CD; Coldplay; Opportunity Hack; MS/research detail; Google tools; career titles; awards; current gaming/hobbies; local AI. Catalog-only details now have actual scene sources. Opportunity Hack is no longer repeated beside SpartanBot in the main dialogue.
- The log is called **Quest log** and contains 24 chronological records: one summary per event card, the epilogue, and the eleven discoveries. Main entries unlock at the last dialogue beat. Discoveries unlock only when their popup is opened. In-memory reached/found sets retain the journal on Back or log jumps; reload clears it.
- Each log heading returns to its validated story screen or reopens its original popup. It does not change the URL/history, lose journal entries, grant stats, or follow arbitrary selectors. Native internal links work in fallback HTML. External project/video links remain separate.
- Multiple native 48px glints can share a scene. Positions are validated numeric data; tests verify alignment, separation, popup bounds, scroll access, and exact focus restoration. The log stays below the HUD and dims only the scene/dialogue area. Popups retain visible dialogue.
- The original 1600ms mosquito and 1800ms pandemic-symbol encounters remain decorative and nonblocking. Reduced motion shows static symbols and cannot restart an encounter on preference restoration. No animation-end event is required for navigation.
- No traveler, companion, avatar, copied franchise asset, new runtime dependency, network request, storage, or server route was added. Scene captions show only the place. The original robot and owner's PLA, retail-therapy, mosquito, opinions, academic-result, and gaming-fund jokes remain.

**Content Model**
`app/content/story.json` now owns card `summary` fields, `epilogue_summary`, and eleven `discoveries` with their own body, summary, target, period, position, sources, and reviewed links. The old independent `achievements` catalog and card `facts` fields are removed. Python derives all log records, preventing orphan log-only content. Badge `quest_id` references are checked against their original grant card.

The prose-free stat projection remains version 2. Main bodies and discoveries allow at most 600 characters and eight nonempty paragraphs; summaries allow 350. No compatibility layer or persistence migration exists. Every popup, summary, stat equivalent, and milestone description remains semantic server HTML, including no-JS, invalid data, CSS/JS failure, and print modes.

Coldplay retains its supplied age-22 label and appears near the Pune narrative. This is not a claim of filming in Pune or an inferred calendar year. Grouped awards and undated projects retain broad labels. The full public-safe narrative/source ledger in `docs/story.md` is preserved; the original private PDFs were not reopened.

**Local Evidence**
Environment: macOS arm64, Python 3.13.14, pytest 9.1.1, Node 24.20.0/npm 11.19.0, Playwright 1.62.0 with Chromium 151.0.7922.34, Firefox 153.0, and WebKit 26.5. Docker client/server 29.7.2 and Compose 5.5.0 are the recorded local container environment.

| Command / Check                                                                     | Observed Outcome                                                                               |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `npm run lint`                                                                      | Passed ESLint and Prettier.                                                                    |
| `.venv/bin/ruff check .` and `.venv/bin/ruff format --check .`                      | Passed.                                                                                        |
| `.venv/bin/pytest -m 'not browser'`                                                 | 202 passed, no selected skips.                                                                 |
| `.venv/bin/pytest -m browser --browser chromium --browser firefox --browser webkit` | 177 passed, 59 per engine, no selected skips.                                                  |
| Local container build/start                                                         | Rebuilt with base + local Compose and became healthy.                                          |
| Runtime boundary                                                                    | 15 approved files, UID/GID 10001, read-only app content, writable `/tmp`; no new runtime file. |
| Main-story word budget                                                              | 748 words in the existing rendered-copy check, below 900.                                      |
| Public scanner self-test                                                            | Synthetic signature/path checks passed; it reports counts only.                                |

Coverage includes exact absolute snapshots and badge prefixes, every main dialogue and completion point, unique discovery prose outside the log, found-only optional entries, every log return target, retained journal on backtracking, reload reset, guarded forged/invalid navigation metadata, popup reachability, target separation, no URL/history mutation, source integrity, escaped hostile text, all fallback modes, reduced motion, CSP/privacy, forced colors, 200% text enlargement, and light/dark axe checks.

Earlier failures during this pass came from tests still expecting the removed 21-item catalog and six old popup IDs. Those tests were replaced with independent 24-record/11-discovery expectations and new behavior checks, not weakened to accept missing content. A further review made the reached/found sets authoritative for jumps rather than trusting a mutable visibility class. The pure-state browser test now imports the already-loaded versioned module so it respects real module-cache identity instead of initializing a second game instance.

**Visual Review**
Main-session Chromium captures at 390x844 and 1440x1000 dark mode covered the Coldplay popup and chronological Quest log. The updated popup header keeps its period/title beside Close to leave room for the cameo link on mobile. The journal uses short summaries, distinct Story/Discovery labels, and explicit return links. The HUD remains visible above the modal.

Reproduce with the README's local container/server flow. In Playwright, navigate to `/`, use the actual advance button until `#journey[data-screen-index="6"]`, click `[data-discovery="coldplay"]`, capture with `page.screenshot()`, close with Escape, and open `[data-action="toggle-quests"]`. Click `#quest-coldplay [data-action="revisit"]` and verify the original popup reopens without a URL fragment. Screenshots are local review artifacts, not source/build inputs or proof of physical-device approval.

All main beats fit at tested 390x844 and desktop sizes. Short 320x568 and long optional popups use internal scrolling with tested end-of-content/control reachability. Physical iOS/Android browser chrome, native zoom, real touch feel, and screen-reader behavior remain separate manual checks.

**Security And Review**
The main session performed design, implementation, testing, code/security review, conformance, and retrospective sequentially without agents. No new blocking local finding is known. Jinja escaping, inert projection data, strict CSP, exact hosts, read-only methods, static allowlisting, request limits, generic errors, and app/connector separation are unchanged.

`tools/check_public.py` was added as a reproducible release guard before new fixtures. It scans staged Git blobs and every commit in a publication range, refuses private paths before opening blobs, and does not read local PDFs or environment files. CI has full-history range coverage. Its implemented signature/path checks are not an exhaustive PII audit; the public diff must still be reviewed manually. No private-input classifier or private-PDF scan is claimed.

**Publication**

- Last previously published baseline: `7b5339e94b77518afa956f7896e9b445401d6b3f`, with successful run [37338483892](https://github.com/pranavprem/portfolio/actions/runs/37338483892).
- The current task authorizes publishing the reviewed accumulated work. Its new commit/SHA and hosted CI result are not implied by the older baseline's green run.
- The production stack remains `portfolio`, repository `https://github.com/pranavprem/portfolio.git`, reference `refs/heads/main`, and exactly `compose.yaml` + `compose.tunnel.yaml`. Do not use `compose.local.yaml` in Portainer or expose `CLOUDFLARED_TOKEN`.
- Public deployment was not performed in this task. Historical public checks on 2026-10-04 saw HTTP `200` rather than a redirect and a Python-user-agent edge `403`. Do not mistake those historical responses for today's deployed SHA. Keep HSTS off until the real redirect/TLS check passes.

**Remaining Gates**

1. Confirm exact-SHA hosted CI for the release and pull/redeploy that revision through the existing Portainer Git stack when authorized.
2. Verify public digest-versioned assets, chapter/discovery/log behavior, health/security headers, and absence of optional edge injection/challenges.
3. Configure and verify HTTP-to-HTTPS redirect before enabling exactly `Strict-Transport-Security: max-age=31536000`.
4. Check physical phones, safe areas, native zoom, screen readers, and representative performance.
5. Verify NAS CPU/Compose behavior, connector firewall isolation, rollback/reconnection, token rotation, outage handling, and protected backups.

No database or application volume needs migration. `www` behavior and a project/art license remain unchosen.
