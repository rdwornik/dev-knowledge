---
id: "[#1454]"
title: "The generated transport index is built first in B2 W2 and groups files by the seat that wrote them (R84, R91)"
status: open
priority: P1
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1454] [P1][M] **The generated transport index is built first in B2 W2 and groups files by the seat that wrote them (R84, R91)** - R84 (operator, 2026-10-05) puts `b2-transport-index` (R79.1) in W2's first wave. R91 (operator, 2026-10-08): every seat has a stable id (architect seats are numbered, CC-run sessions are named by their session name), every transport file a seat or session writes carries that id in its head (`by:`) and in its name where the grammar allows, and the generated `INDEX.md` (R79) groups files by seat and session, so one read shows what each seat wrote and which report belongs to which decision. [#1371] holds the index mechanism (R71, R79) and [#1439] holds the `by:` field and the per-seat grouping; [#1439] names R91 and states no `owner:`, which the rulings gate reads as not carrying · Done when: (1) the generated `to-browser/INDEX.md` lists only current files and groups them by seat and session, shown by a fixture transport with two seats whose files land in separate groups; (2) `transport_lint` refuses a new transport file whose head has no `by:`, shown by a fixture; (3) the janitor moves superseded files to `archive/YYYY-MM/` and the file count before equals the count after; (4) RED-first: tests (1) and (2) fail on `03d21ff8` and pass after the change · owner: lane `b2w2-transport-index` (batch B2-W2) · touches: `scripts/transport.py`, `scripts/transport_lint.py`, `ecosystem/transport-registry.yaml`, the index generator, tests · kill-candidates: [#1439] [#1371] -- [#1439] states the same `by:` and per-seat index without an `owner:`, [#1371] states the index and the janitor; fold them into this row, or this row into them, if the lane lands the index, the `by:` field and the janitor as one change · refs [#1439], [#1371], `scripts/transport_lint.py`, `protocols/STANDING_RULINGS.md` section AS (R84, R91) and section AR (R79) · source: R84 in `to-browser/RATIFICATION-2026-10-05.md` (v5) and R91 in `to-browser/RATIFICATION-2026-10-08.md` (v2), landed at section AS by lane `b2w2-rulings-landing`
