---
id: "[#1873]"
title: "Arm the land-on-handback connector at its one call site, and fix the lane's three judge nits"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1873] [P2][M] **Arm the land-on-handback connector at its one call site, and fix the lane's three judge nits** - e30-land-on-handback deferred the arming (SESSION-e30-land-on-handback.md:131, Q-H-1 H-1): one call site in queue_runner's HANDBACK event that runs `once --lane <slug>`; W-1 cannot pass without it. [#1859] (closed) names it out of scope. The same SESSION (:127) lists three non-blocking judge findings with no row: (a) the `--state-dir` lock split, (b) a negative `handback_to_main_s`, (c) a LAUNCH receipt without a `batch` key (to-browser/DIGEST-MORNING-N8-SEAT-LIFECYCLE-NIGHT-2026-11-05.md section 5). · touches: scripts/queue_runner.py, scripts/land_on_handback.py, tests/test_land_on_handback*.py · kill-candidates: none - [#1859] is closed and names this call site as out of its scope · refs `scripts/land_on_handback.py` · Done when: a HANDBACK event in queue_runner runs `land_on_handback.py once --lane <slug>` (test), and each of (a)-(c) has a pinning test · decided-by: DIGEST-RULING-SESSION-CLOSE-DECOUPLED-2026-11-05 S2 + AMENDMENT-1 A2 · source: N0 orphaned item 2
