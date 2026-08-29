---
id: "[#620]"
title: "Retire the root-README prohibition across the fleet, not only at the hub"
status: open
priority: P2
size: M
theme: "[E5] Canonical-file integrity"
story: "[S14] Keep the day-to-day docs right-sized and current"
generates: BACKLOG.md
---

- [#620] [P2][M] **Retire the root-README prohibition across the fleet, not only at the hub** — ADR-114 `Decommission` item **(a)**: `CLAUDE.md` §5 rule 5's *"do not recreate it"* clause. **Decommissioned at the hub 2026-08-29** by `[#614]` lane-b. The clause is **repo-owned** there — it sits between the `critical-rules-records` end-marker and the `critical-rules-consistency` start-marker — so no lockstep `templates/claude-regions/` act was owed, and none was taken. **Residual:** ADR-38 A5's deprecation is *fleet* doctrine, and the eight ADR-104 children inherit it through their own `CLAUDE.md` and the methodology floor; nothing has told them A5 is now superseded in that single respect, so six of them still carry a prohibition the hub has retired. · Done when: each of the eight consumers' inherited statement of the root-README prohibition is either corrected or shown not to exist, measured per repo rather than assumed · refs docs/decisions/ADR-114-readme-recreation-legality.md, docs/audits/2026-08-29-technical-614-consumer-enumeration.md, #614, #621 · source: ADR-114 Decommission (a)
