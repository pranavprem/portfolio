**Implementation Retrospective**
Recorded 2026-09-06 after implementation and local verification. This is an engineering record, not a claim of completed NAS/public deployment.

**What Worked**

- The full sanitized story was preserved separately from the eleven runtime chapters. That kept hobbies, source disagreements, motivations, and omitted projects available without republishing the private PDFs or making the owner repeat himself.
- Server-rendered prose and absolute snapshots made progressive enhancement practical. Python tests verify the exact data; browser tests independently verify thresholds, reversible badge prefixes, jumps, restoration, and failure modes.
- Native scrolling, one small JavaScript module, system fonts, and original SVG kept runtime dependencies and privacy boundaries small. Node/axe/Playwright are developer tools only.
- Explicit local and tunnel Compose overrides let the app build and run without a Cloudflare secret while keeping production port publication disabled. The pinned Python app and connector binary both ran under their intended nonroot identities locally.

**What Was Corrected**

- The first architecture draft did not capture the expanded AI-ready documentation requirement and proposed opening stats that were not all low. The review added the documentation gate and the exact opening `0, 1, 1, 1, 0, 1`.
- A template-only 110% callout invented an extra-credit explanation. It was removed without suppressing the owner's actual maximum-possible/sole-student account. A rendered-copy regression now covers it. Review templates and captions as well as JSON.
- The initial three-engine browser run found two real defects: overflow/overlapping stats at 200% text enlargement on a 320px viewport, and an unreadable pinned sheet in a 200px-high desktop viewport. Responsive grids, wrapping inventory/headings, and a measured normal-flow theater fallback fixed them. No text shrinking, hidden page overflow, or skipped test was used.
- Several drafting-stage documents described future files after those files existed. The integrated handoff now owns observed status; architecture examples are not deployment evidence.
- An actual image-content probe found local Python caches that a directory exception had re-included in Docker's build context. Explicit per-directory deny rules and per-file exceptions fixed it. The rebuilt image has exactly 14 approved runtime files; CI repeats this check. An attractive allowlist is not proof of its effective behavior.
- Fresh Ubuntu CI exposed a native-input test synchronization assumption not seen on macOS: a chapter changes before End/Home scrolling necessarily finishes. Tests now wait for real page edges before sending the next input and position the wheel pointer inside the page. Do not change application scroll behavior to compensate for a test driver.

**Evidence**
The final local application run passed 143 Python/content/HTTP tests and 99 browser cases across Chromium 151, Firefox 153, and WebKit 26.5. All initially failing viewport regressions passed in all engines. Ruff, dependency audit, Docker build/startup, health and isolation checks are recorded with their precise scope in [handoff.md](handoff.md). Hosted CI/publication results are recorded there when observed, not assumed here.

**Next Lessons**

- Keep the unusual viewport regressions. Normal desktop and phone screenshots would not have exposed both defects.
- Continue to distinguish native browser zoom, real phone safe areas, and assistive-technology testing from desktop Playwright emulation and axe. Those manual release checks remain open.
- Do not turn a healthy app or a working `cloudflared --version` into a claim of a connected tunnel. Actual Portainer secret provisioning, public DNS/TLS/redirect behavior, connector log privacy, network isolation, and recovery must be checked by the deployment operator.
- Retain one canonical contributor entry point and the full source ledger. Add no new orchestration machinery, model policy, frontend framework, or compatibility layer merely to make future continuation possible.

**Editorial Revision**
The owner's feedback exposed a different failure from code correctness: accurate prose can still sound robotic, apologetic, and tedious. The rewrite removed repeated lessons/disclaimers, made the 110%-to-TA sequence explicit, corrected the motivations and COVID framing, and retained the full source account separately. The core now measures 893 words; the 56-entry catalog is optional rather than competing with the five-minute story.

The main-story budget initially failed at 979 words. Cutting redundant prose/captions, rather than changing the limit, brought it under 900. Catalog headings initially overflowed at doubled text size; wrapping fixed that without hiding page overflow. All 67 scroll reactions, both themes, authorized links, and accessible fallback content then passed in the expanded suite: 160 Python tests and 117 browser cases.

Reviewing all 49 public repo descriptions helped with relevance, but does not justify claiming every linked project is secure, maintained, or independently authored. Preserve the distinction. The earlier ignored `.env` with a placeholder token-file path was scaffolding, not a connected tunnel; the later owner decision accepts authenticated Portainer `CLOUDFLARED_TOKEN` metadata mapped only to cloudflared's `TUNNEL_TOKEN`. The five-perspective review and candid tone/deployment concerns are in [review.md](review.md).

An environment-sourced Compose secret initially looked like a way to satisfy the Portainer workflow without container environment exposure. Docker Compose v5.5 parsed it but rejected container creation for the read-only cloudflared service because only a file source was supported there. Keeping the read-only root and using cloudflared's documented `TUNNEL_TOKEN` input was the smaller, working choice after the owner explicitly accepted Portainer/Docker metadata exposure. A synthetic probe confirmed only the connector receives that environment value; no real token was displayed or stored in the repository.

**Final Curation**
The owner correctly called out that a comprehensive inventory was still too much of a GitHub dump. It is now 21 grouped highlights, not 56 scroll stops. Class-project detail remains in the source ledger but no longer dilutes the public presentation. Eras provide newest-first grouping without fake dates. The main story is 887 words in one to three mini-paragraphs per card; contextual links avoid making readers hunt through the appendix.

Late owner details were preserved rather than guessed: dengue and a month in hospital, the mosquito boss fight, NCS's elephant, the smaller GEC buildings, Salesforce Tower, the exact Coldplay/Oxfam timestamp, and the return to San Jose. The unscoped availability percentage was removed from public copy. All 170 Python tests and 117 browser cases passed after these changes; actual NAS, public tunnel, real-device, and recovery checks remain open.

**Version Two Lessons**
The next feedback showed that "facts present" is not a sufficient editorial review. Independent events had been merged into awkward implied connections, and the review had called tone issues resolved too early. New regressions check separate GEC/Green Belt beats and the mosquito-before-dengue order. Audience judgments are now explicitly provisional, not justified by CI.

The owner replaced the six-stat model with five stats and actual milestones. That required coordinated JSON/schema/JS/CSS/fixture changes, not merely removing a row. Version two now rejects retired keys, old projections, invalid badge prefixes, and decreasing Experience. Invalid initial projection data is no longer rendered as a fallback HUD.

The compact mobile HUD stacks labels above values, so a former horizontal-only collision test produced false positives; actual rectangle intersection is now checked. The core initially exceeded the reading budget at 947 words, then 903; copy was cut rather than increasing the 900-word limit. The final local result is 175 Python tests and 123 browser cases passing. The compact bullet appendix and removed duplicate ledger reduce presentation clutter without deleting source history or assistive equivalents.

**Quieter Layout**
The owner still found the version-two page dense and messy. Meeting a word budget and grouping the appendix did not address the many competing labels, frames, and repeated explanations. Removing masthead/hero subtitles, world/chapter banners, HUD level/class labels, coordinates, and extra scene captions let the original art and prose do more of the work. A narrower desktop measure, more chapter spacing, and GEC's independence paragraph followed by six bullets preserve the independent facts rather than merging them again. Shorter optional summaries do not replace the full source ledger.

The visible main count dropped from 900 to 857 without changing the main narrative paragraphs. Chromium captures at 1440 x 1000 and 390 x 844 were inspected for opening, college, current work, and the bonus section, including both themes. This is evidence about those captures, not proof of subjective owner satisfaction or physical-device behavior.

The first full layout suite passed 123 cases and failed three: the old short-desktop test considered only the reduced HUD height, not the padded theater that correctly fell back to normal flow. The regression now checks the complete footprint and 200px -> 400px -> 200px recovery; no application behavior was weakened. Final results: 175 Python/content/HTTP tests and 126 three-engine browser cases passed. The rebuilt Docker page passed health, three-engine smoke, and exact 14-file/nonroot/read-only application checks. Real-device, screen-reader, native-zoom, NAS, public transport, and recovery gates remain open.

**Tempered Ending**
The owner pointed out a mismatch between an open-ended story and its almost-maxed final sheet. The final values are now `8, 10, 8, 7, 7`: only Enthusiasm is full. Reducing only the last Experience value would have violated its nondecreasing contract; earlier Experience and Charisma values and post-SJSU Coding were rebalanced rather than patched in the renderer. The previous SJSU Coding 10 remains a chapter-specific intensity peak. No new disclaimer, invented decline, or claim about measured ability was needed.

The fix stayed in authored snapshots and their independent expectations, with no schema or runtime-code change. Existing tests now explicitly protect the final room to grow and retained SJSU peak. All 175 Python tests and 126 browser cases passed again; the rebuilt Docker page showed matching numbers and pips in all three engines at 1440px and 390px. Health and the exact 14-file/nonroot/nonwritable-app boundary passed. This reinforces that game balance is an editorial decision whose visual message needs review alongside the prose.

**Voice And Motion Pass**

The next owner review showed that correcting structure and reducing chrome still did not make every line sound personal. A whole-site pass replaced detached résumé captions with direct first-person wording and preserved specific supplied humor rather than adding generic quips. It also corrected the dengue timing, HSDI name and nominee age, removed the duplicate mosquito setup and rejected CyanogenMod line, focused the Google progression, and rendered the Bender/PLA joke as text without franchise artwork. Rendered-copy tests matter because headings, milestone descriptions, and template-only endings can drift even when chapter bodies are correct.

The side scene needed stronger feedback, but not a timer-driven game loop. Alternating limbs, static dust, companion steps/tail movement, and a bounded companion hop were added as pure functions of reading position. The first implementation could have combined the ordinary two-pixel companion step with the four-pixel reaction hop; suppressing the ordinary step during a reaction keeps the authored four-pixel reaction bound honest. Reduced motion clears every new detail, and idle scrolling still schedules no continuing work.

The revised prose first measured 901 words. Removing one unnecessary intensifier preserved the smart-colleagues point and brought the rendered main story to exactly 900 rather than weakening the limit. Final local results are 176 Python/content/HTTP tests and 126 browser cases across Chromium, Firefox, and WebKit. Representative Chromium captures at 1440 x 1000 and 390 x 844 covered the opening, Google, dengue, and ending; they support layout review but not owner approval, real-device behavior, or motion quality judgment. The rebuilt Docker page passed health, three-engine mobile enhancement/final-stat smoke, and the exact 14-file/nonroot/nonwritable-app boundary.

**Salesforce And Personal Systems Revision**

The next correction was about technical hierarchy, not adding more jargon. Slack had become the earned Bots milestone even though it was a small public-API contribution. Replacing that milestone with Bots at 99.99% and separating Chat's data-center-to-AWS move from Bots' later Heroku-to-multisubstrate customer-traffic migration restored the actual shape of the work. Copilot and Agentforce also needed distinct jobs: communicating with a configurable agent versus giving customers a platform to build agents that evolved through topics/actions into Atlas/AgentScript and broader runtime capabilities.

Adding that detail pushed the rendered story from 900 to 970 words. Chapter-level measurement showed the right response was not to compress the new account back into buzzwords; trimming repetition in older school, HSBC, Google, Chat, and COVID passages retained their approved beats. Restoring the established "Copilot by 2023" anchor produced an 896-word story at that stage. Assertions now protect both the presence and the scope of Argo CD, 99.99%, public API, 100%-traffic migration, Copilot, Atlas/AgentScript, the capability list, and context-aware team tooling.

The personal continuation follows the same engineering impulse: OpenClaw and Hermes maintain each other, Morpheus gates credentials through human approval, and the homelab supplies Home Assistant/media/memory/local-AI infrastructure. Reviewing public repository metadata helped choose Morpheus, OpenMemory, Qdrant NAS, and Neo Services without reopening the rejected repository dump. A public README is still not a security audit, and the website exposes no credentials, private Hermes code, configuration, identifiers, or precise location.

The owner supplied a recognizable Bender PNG for the PLA joke, but inspection found a baked checkerboard rather than transparency and a conflict with the existing no-copied-franchise-art boundary. After an explicit choice, the PNG was removed and a tiny original generic pixel robot was added. That one asset required coordinated static inventory, Docker allowlist, CI file-count, SVG-safety, rendering, and documentation updates. The later side-arrow request became a narrow reversible scroll alias rather than a second game-state system: after an 80px immediate step proved jittery, it was retuned to a smooth 40px step matching native arrow feel, with an immediate reduced-motion fallback. It never cancels input, ignores editable controls, and yields to real horizontal overflow. Final results are 176 non-browser tests and 132 three-engine browser cases; the rebuilt image is healthy with exactly 15 approved files.

**Service Naming Follow-Up**

The generic Compose service name `app` was technically valid but made the Cloudflare origin `http://app:8000` unnecessarily vague during deployment. Renaming the service to `portfolio` required changing the base/local/tunnel Compose merge keys, connector dependency, CI commands, trusted-host regression, operator commands, failure guidance, and canonical documentation together. The public hostname and Flask trusted-host policy did not change; `portfolio` is private Docker DNS and remains rejected as an HTTP Host header.

Both local and synthetic-token production configurations parsed successfully after the rename. The rebuilt `portfolio-portfolio-1` container became healthy, resolved `portfolio` on the origin network, and retained the 15-file, UID/GID 10001, read-only application boundary. All 176 non-browser tests and 132 browser cases passed. Public checks still reached the prior Squarespace page at that point, which reinforced that healthy local containers and valid tunnel configuration are not evidence of a completed DNS/public cutover.

**Object Marker Revision**

The traveler and creature companion were technically original and deterministic, but neither followed from the owner's actual story. The unexplained creature in particular read as random decoration. The owner chose a stricter rule: no living sprites, only objects that identify each life phase. Eleven small original markers now progress from controller and backpack through study/work tools to cloud, bot, and agent systems.

The smaller conceptual model also removed limb, tail, dust, and follower-offset logic. One chapter-selected object follows the existing route, takes a one-pixel position-derived step, and performs the existing bounded achievement hop; the compact HUD mirrors it. Exact object order, same-position determinism, reduced motion, CSP-safe local SVG fragments, and absence of the rejected living sprite nodes are regression-tested.
