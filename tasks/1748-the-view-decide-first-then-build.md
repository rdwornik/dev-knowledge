---
id: "[#1748]"
title: "the view: /decide first, then build"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1748] [P2][M] **the view: /decide first, then build** - a generated AS-IS view of the system, decided through /decide before it is built · Done when: (1) an ADR at status Proposed from /decide over DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md section C with every decide_checks.py check passing; (2) after the operator ratifies it, the view is built (expected: scripts/system_map.py extended into the generated AS-IS view, JSON + static HTML, live on localhost, snapshot for the artifact) and wired at batch close. · touches: `scripts/system_map.py`, `docs/decisions/`, `docs/decisions/ADR-133-the-system-view.md`, `docs/audits/2026-10-31-technical-design-view.md`, `tests/test_e30_view_adr.py`, `docs/decisions/README.md`, `tests/test_validate_adr_status.py`, `.claude/generated/recent-adrs.md`, `scripts/system_view.py`, `tests/test_system_view.py`, `tests/fixtures/system_view/pins.json`, `.gitignore`, `.claude/commands/map.md`, `ecosystem/harness.yaml` · follow-on: the fast-leg runner-event hook (one call site in scripts/queue_runner.py, ADR-133 D4) is built once e30-queue-runner is MERGED on main; the view itself (full leg wired at batch close) is built by e31-system-view · kill-candidates: none -- no open row owns the view · refs `scripts/system_map.py` · source: to-cc/GO-E3.0.md G2 · decided-by: the operator, 2026-10-31, GO-E3.0 id grant
