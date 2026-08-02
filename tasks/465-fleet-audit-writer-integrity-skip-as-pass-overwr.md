---
id: "[#465]"
title: "fleet-audit writer integrity — legs 1-3 DONE, leg 4 open"
status: open
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#465] [P2][M] **fleet-audit writer integrity — legs 1-3 DONE, leg 4 open** — **(1) DONE** (`80e743aa`): a skip is no longer emitted `pass`. **(2)+(3) DONE**: one bug, not two (L-B §4 — the 07-21 daily fell 16 WARNs to 2, the missing 14 exactly the hub-only checks). Cause: hub identity compared the live `_REPO_ROOT` against the absolute path COMMITTED in `state.yaml`, so from any other checkout (worktree, cloud clone, moved repo) the hub failed to recognise itself and all 15 hub-gated checks of 38 skipped `n/a` — the flap tracked which tree ran, not chance. Fix: `resolve_repo_path()` binds the hub to the live tree at the `run`/`repo` seam; 16 copied comparisons collapse into one `_is_hub()`. Regression `tests/test_hub_identity.py`, self-enumerating over `ALL_CHECKS`. NOT fixed: the same-day file collision — a cross-tree run still last-run-wins, now non-lossy. **(4)** OPEN — `handoff_tag_canonicity` self-disabled. · Done when: last-run-wins is accepted on record and tag-canonicity is fixed or retired · refs scripts/audit.py, tests/test_hub_identity.py, #460 · kill-candidates: none — [#460] rules the lane; this is writer correctness · serialize-group: audit-py
