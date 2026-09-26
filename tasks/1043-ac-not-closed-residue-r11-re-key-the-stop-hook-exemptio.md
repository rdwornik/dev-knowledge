---
id: "[#1043]"
title: "AC-NOT-CLOSED residue R11: re-key the Stop-hook exemption on the seat registry plus a counter"
status: open
priority: P3
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1043] [P3][M] **AC-NOT-CLOSED residue R11: re-key the Stop-hook exemption on the seat registry plus a counter** - DIGEST-OPEN-CARRIERS-2026-09-25 §4 residue (DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18 §4 R11): `session_end_backpressure.py` still keys its exemption on the branch name, not the seat registry, and carries no counter. · Done when: `scripts/session_end_backpressure.py`'s Stop-hook exemption keys on the seat registry with a counter, RED-first witnessed on a fixture where the branch name alone would give the wrong answer · refs `scripts/session_end_backpressure.py`, `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md` §4 R11 · kill-candidates: none -- not built
