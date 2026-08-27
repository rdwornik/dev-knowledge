---
id: "[#266]"
title: "Codify the test-scoped-grant language lesson"
status: deferred
priority: P3
size: S
theme: "[E3] Lessons feedback loop"
story: "[S10] Codify recurring patterns into the methodology"
generates: BACKLOG.md
---

- [#266] [P3][S] Codify the test-scoped-grant language lesson (E4-1 precedent) — Wave-2 ratified (2026-07-05): a NARROW test-scoped grant must explicitly include "plus the mechanical count/pinning assertions the change forces". Epic-4's check-#7 retirement broke two `len(ALL_CHECKS) == 29` literals in `test_doc_code_edge.py`; the lane self-adjudicated 29→28 IN-GRANT and root RATIFIED it beyond the E4-1 letter (mechanical, disclosed, retirement-forced). Write the precedent into the grant-authoring guidance (EPIC_BOOT FILE-BOUNDARY template / ADR-97 §14a) so future narrow grants pre-authorize the count-assertion fallout. · Done when: the grant-authoring guidance states that a narrow test-scoped grant includes the mechanical count/pinning assertions the change forces, at both `templates/handoff/epic/EPIC_BOOT.md.tmpl`'s FILE-BOUNDARY section and `ADR-97` §14a, citing the E4-1 precedent · refs ADR-97, EPIC_BOOT template, tests/test_doc_code_edge.py, LESSONS 2026-07-05 · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
