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

- [#511] [P2][M] **The 30-minute handoff cut is ~99.8% session authoring, not machinery** — mechanized cost of a cut + live probe gate is **~4.5s, 0.25%** of the 30-min wall clock; the cost is the 15 FILL-IN regions, a 38,067-byte `PASTE_THIS.md`, and the 14 probes `/handoff-verify` re-derives live (§5's anti-bluff point, load-bearing). **The fork (doctrine, not an edit):** cut FILL-IN count (vs RF-6), probe count (vs §5), or verify pass (vs anti-bluff) — any cut is a version bump + reconciliation. Not a duplicate of [#449]. **Scope is the NON-MECHANIZED load only** — the machinery half is out (register `protocols/STANDING_RULINGS.md` I-F2); commission 5's session-continuity half (distillate R43/R50/R51) is attached here (register I-D4), R51's verification-at-cut leg already LANDED · Done when: `protocols/HANDOFF_PROCESS.md` carries the ruled cut of the NON-MECHANIZED loads with a version bump and dependents re-stamped (`reconciled_versions` green), and one post-change handoff records measured wall-clock and token cost against the recorded baseline in its bundle · refs `scripts/gen_handoff.py`, `scripts/verify_handoff_probes.py`, `protocols/HANDOFF_PROCESS.md` §5 + RF-6, [#449], [#350] · kill-candidates: none — [#449] owns byte ceiling; [#350] is the grab-bag · serialize-group: handoff
