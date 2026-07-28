---
id: "[#220]"
title: "MODIFY / semantic-drift axis"
status: open
priority: P2
size: M
theme: "[E2] Enforced governance"
story: "[S5] Catch spec/dependent drift mechanically, not by memory"
serialize-group: coherence
generates: BACKLOG.md
---

- [#220] [P2][M] MODIFY / semantic-drift axis — VERIFY-FIRST SPIKE ONLY: does the ADR-89 Pyright oracle (`references()`) or any existing organ catch a MODIFY edge (a source whose text/behaviour changes while its version pin + symbol signature stay put), or only add/remove/exist? Any detector design is conditional on the spike's finding — do NOT design ahead of it. · Done when: a verify-first pass records whether any existing organ detects a semantic/MODIFY change on a fixture (the design leg is deferred, gated on this spike's result) · refs #172, #180, ADR-88, ADR-89 · serialize-group: coherence
