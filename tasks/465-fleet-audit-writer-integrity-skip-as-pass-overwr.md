---
id: "[#465]"
title: "fleet-audit writer integrity — legs 1-3 DONE, leg 4 open"
status: closed
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
serialize-group: audit-py
generates: BACKLOG.md
---

- [#465] [P2][M] **fleet-audit writer integrity — legs 1-3 DONE, leg 4 open** — **(1) DONE** (`80e743aa`): a skip is no longer emitted `pass`. **(2)+(3) DONE**: one bug, not two (L-B §4 — the 07-21 daily fell 16 WARNs to 2, the missing 14 exactly the hub-only checks). Cause: hub identity compared the live `_REPO_ROOT` against the absolute path COMMITTED in `state.yaml`, so from any other checkout (worktree, cloud clone, moved repo) the hub failed to recognise itself and all 15 hub-gated checks of 38 skipped `n/a` — the flap tracked which tree ran, not chance. Fix: `resolve_repo_path()` binds the hub to the live tree at the `run`/`repo` seam; 16 copied comparisons collapse into one `_is_hub()`. Regression `tests/test_hub_identity.py`, self-enumerating over `ALL_CHECKS`. NOT fixed: the same-day file collision — a cross-tree run still last-run-wins, now non-lossy. **(4) DONE** (2026-08-04, R5 producer lane): the defect was the WRITER, not the row — `handoff_tag_canonicity` emitted a verdict for two spec generations after its subject died (285 `n/a` vs 5 `pass` across every `ecosystem/*/history/*.md`, and the 5 passes were leg 1's skip-as-pass). Built the CLASS fix first: `_na()`/`_na_reason()` give every `n/a` a machine-readable reason (SUBJECT-ABSENT vs NOT-APPLICABLE) inside `evidence`, leaving the LOCKED `Finding` shape and the daily's columns untouched (tripwire T1 adjudicated: does not fire); `detect_unconditionally_inert_checks` self-enumerates `ALL_CHECKS` and WARNs on a check that can only ever be SUBJECT-ABSENT; `append_history` names a check that vanished since the previous reading, so a retirement is visible to a reader of the dailies. The detector's first verdict RETIRED tag-canonicity — `ALL_CHECKS` **39 → 38**. **Last-run-wins ACCEPTED ON RECORD** (operator ruling 2026-08-04, at the ARC 2 merge gate): the same-day cross-tree collision stands as designed, non-lossy because the later run carries the full check set. · Done when: last-run-wins is accepted on record and tag-canonicity is fixed or retired · refs scripts/audit.py, tests/test_hub_identity.py, #460 · kill-candidates: none — [#460] rules the lane; this is writer correctness · serialize-group: audit-py
