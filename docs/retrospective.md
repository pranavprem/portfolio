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

**Evidence**
The final local application run passed 143 Python/content/HTTP tests and 99 browser cases across Chromium 151, Firefox 153, and WebKit 26.5. All initially failing viewport regressions passed in all engines. Ruff, dependency audit, Docker build/startup, health and isolation checks are recorded with their precise scope in [handoff.md](handoff.md). Hosted CI/publication results are recorded there when observed, not assumed here.

**Next Lessons**

- Keep the unusual viewport regressions. Normal desktop and phone screenshots would not have exposed both defects.
- Continue to distinguish native browser zoom, real phone safe areas, and assistive-technology testing from desktop Playwright emulation and axe. Those manual release checks remain open.
- Do not turn a healthy app or a working `cloudflared --version` into a claim of a connected tunnel. Actual NAS ACLs, protected token provisioning, public DNS/TLS/redirect behavior, connector log privacy, network isolation, and recovery must be checked by the deployment operator.
- Retain one canonical contributor entry point and the full source ledger. Add no new orchestration machinery, model policy, frontend framework, or compatibility layer merely to make future continuation possible.
