---
id: "[#511]"
title: "The 30-minute handoff cut is ~99.8% session authoring, not machinery"
status: open
priority: P2
size: M
theme: "[E1] Handoff continuity"
story: "[S1] Match the handoff payload to the work mode"
serialize-group: handoff
generates: BACKLOG.md
---

- [#511] [P2][M] **The 30-minute handoff cut is ~99.8% session authoring, not machinery** — **MEASURED 2026-08-07**: mechanized cost of a cut + live probe gate is **~4.5s**, **0.25%** of the 30-min wall clock (breakdown: `docs/audits/2026-08-07-technical-handoff-engine-thinning.md`) — not a performance row. **Where the time goes:** 15 FILL-IN regions, a 38,067-byte `PASTE_THIS.md`, 14 probes `/handoff-verify` re-derives live — §5's anti-bluff point, load-bearing. **The fork this row settles (doctrine, not an edit):** cut FILL-IN count (vs RF-6), probe count (vs §5), or verify pass (vs anti-bluff) — any cut is a version bump + reconciliation. Not a duplicate of [#449] (one-artifact ceiling vs whole-cut cost). · Done when: the operator rules which load is cut and by how much, encoded in `HANDOFF_PROCESS.md` (version bump + reconciliation), and a re-measured cut records the new cost vs baseline · refs `scripts/gen_handoff.py`, `scripts/verify_handoff_probes.py`, `protocols/HANDOFF_PROCESS.md` §5 + RF-6, `.claude/commands/handoff-verify.md`, [#449], [#350] · kill-candidates: none — [#449] owns byte ceiling; [#350] is the grab-bag; no open row owns cut cost · serialize-group: handoff
