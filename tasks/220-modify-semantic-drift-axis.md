---
id: "[#220]"
title: "MODIFY / semantic-drift axis"
status: deferred
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: coherence
generates: BACKLOG.md
---

- [#220] [P2][M] MODIFY / semantic-drift axis — VERIFY-FIRST SPIKE ONLY: does the ADR-89 Pyright oracle (`references()`) or any existing organ catch a MODIFY edge (a source whose text/behaviour changes while its version pin + symbol signature stay put), or only add/remove/exist? Any detector design is conditional on the spike's finding — do NOT design ahead of it. · Done when: a committed fixture exercises a semantic/MODIFY change, a `docs/audits/` record names which organs fired and which did not against it, and the design leg stays deferred pending that result · refs #172, #180, ADR-88, ADR-89 · serialize-group: coherence · DEFER — the 45-day icebox sweep of 2026-08-27 (C4 §3, ruling X1's final step, night-harvest governance session). Peg: **no row-level dependency is claimed** — this is an ATTENTION decision, not a blocked-by. Un-defers when an arc claims the row or the operator re-prioritises it. Recorded explicitly so this row is never mistaken for one waiting on another row, which is the failure the same session's re-peg step was fixing.
