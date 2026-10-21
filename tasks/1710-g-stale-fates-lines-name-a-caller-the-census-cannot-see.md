---
id: "[#1710]"
title: "G-STALE: 14 fates lines name organs that already have a real caller (R149)"
status: open
priority: P3
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1710] [P3][S] **G-STALE: 14 fates lines name organs that already have a real caller (R149)** - the E1 fates digest found 14 `ecosystem/harness.yaml` fates lines whose organ has a caller the census already sees (e.g. `ci_verdict.py` at `scripts/gen_handoff.py:858`), so the line is obsolete; 13 now carry `manual_until: 2026-11-09` and this id; the 14th, `plan_lint.py`, keeps 2026-10-19 until [#1711] changes the test that pins it · owner: harness-fates lane · target batch: E2 · Done when: (1) RED first: the in-process `organ_moments` census set is shown to contain none of the 14; (2) the 14 fates lines and their `ORPHAN_DISPOSITIONS` entries are deleted; (3) real-use witness: `uv run --locked pytest tests/test_loop_declaration.py -k fates` green after the deletion · touches: `ecosystem/harness.yaml`, `scripts/graph_queries.py` · kill-candidates: none -- no open row covers the stale lines · decided-by: R149 (operator, 2026-10-19) · refs `ecosystem/harness.yaml` · source: G-STALE in `to-browser/DIGEST-E1-FATES-2026-10-19.md`
