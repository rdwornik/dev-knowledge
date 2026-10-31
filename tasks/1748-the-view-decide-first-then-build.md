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

- [#1748] [P2][M] **the view: /decide first, then build** - a generated AS-IS view of the system, decided through /decide before it is built · Done when: (1) an ADR at status Proposed from /decide over DIGEST-E3-0-PROPOSALS-EVALUATION-2026-10-31.md section C with every decide_checks.py check passing; (2) after the operator ratifies it, the view is built (expected: scripts/system_map.py extended into the generated AS-IS view, JSON + static HTML, live on localhost, snapshot for the artifact) and wired at batch close. · touches: `scripts/system_map.py`, `docs/decisions/` · kill-candidates: none -- no open row owns the view · source: to-cc/GO-E3.0.md G2 · decided-by: the operator, 2026-10-31, GO-E3.0 id grant
