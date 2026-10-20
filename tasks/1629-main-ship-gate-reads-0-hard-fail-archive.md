---
id: "[#1629]"
title: "main ship-gate reads 0 hard-fail; archive-row signature current"
status: open
priority: P1
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
implements: "intake-118"
generates: BACKLOG.md
---

- [#1629] [P1][S] **main ship-gate reads 0 hard-fail; archive-row signature current** - main reads ship-gate 0 hard-fail: canonical_freshness, journal_day_letters, consumer_at_landing and organ_truth are green and the archive-row signature is current. D0.2 (P0): on main @ 579053a3 `audit.py ship-gate` lists 11 hard-fail entries from four organs and `tests/test_archive_row_body.py::test_every_committed_record_still_proves_out` fails 79 of 86 on a stale signature; `[#1350]` carries the transport-lock flake and its known-red expiry · owner: lane `lane-dz-1350-p0-green-main`, landed by the integrator. target batch: D0 · Done when: `uv run --locked python scripts/audit.py ship-gate` run on main reads 0 hard-fail organ(s) and the archive-row test is green; the `[#1350]` registry entry is quoted from main; real-use witness: the next lane's self-check runs ship-gate with no inherited red · touches: see the body · kill-candidates: `[#1350]` -- shares the known-reds expiry, the lock fix itself stays there · implements: intake-118 · refs `[#1350]`, `[#1347]`, `to-cc/PLAN-HARNESS-2026-10-18.md` · decided-by: R137 (Q5: the plan r4 OK of 2026-10-18). Defect C7: `journal_spine_anchor` FAILs on main's own merge commit (base-side) (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`). Defect C8: `organ_truth` is red after 2026-10-19 on the R149 date cliff (map C2, `DIGEST-HARNESS-MAP-2026-10-20-ANNEX`) · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
