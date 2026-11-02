---
id: "[#1748]"
title: "the view: /decide first, then build"
status: closed
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1748] [P2][M] **the view: /decide first, then build** - a generated AS-IS view of the system, decided through /decide before it is built · Done when: (1) an ADR at status Proposed from /decide over DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md section C with every decide_checks.py check passing; (2) after the operator ratifies it, the view is built (expected: scripts/system_map.py extended into the generated AS-IS view, JSON + static HTML, live on localhost, snapshot for the artifact) and wired at batch close. · touches: `scripts/system_map.py`, `docs/decisions/`, `docs/decisions/ADR-133-the-system-view.md`, `docs/audits/2026-10-31-technical-design-view.md`, `tests/test_e30_view_adr.py`, `docs/decisions/README.md`, `tests/test_validate_adr_status.py`, `.claude/generated/recent-adrs.md`, `scripts/system_view.py`, `tests/test_system_view.py`, `tests/fixtures/system_view/pins.json`, `.gitignore`, `.claude/commands/map.md`, `ecosystem/harness.yaml`, `scripts/graph_queries.py`, `tests/test_loop_declaration.py`, `tests/test_spine_moments.py`, `ecosystem/system-map-record.json`, `scripts/queue_runner.py`, `tests/test_dodo.py` · built: the view (full leg wired at batch close) and the fast-leg runner-event hook (one call site in scripts/queue_runner.py, ADR-133 D4) are built by e31-system-view; the integrator closes this row at landing after regenerating BACKLOG.md and tasks/manifest.json · kill-candidates: none -- no open row owns the view · refs `scripts/system_map.py` · source: to-cc/GO-E3.0.md G2 · decided-by: the operator, 2026-10-31, GO-E3.0 id grant · **CLOSED 2026-11-02** — evidence a205746de25c1232df2ff9bedcaa374dc0d685f2 · CI run 41504182046 (success) · tests tests/test_system_view.py::test_pins, tests/test_system_view.py::test_full_leg_builds_the_map_once_then_the_view, tests/test_system_view.py::test_harness_batch_close_carries_the_full_leg_step
