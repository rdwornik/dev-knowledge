---
id: "[#322]"
title: "Fleet dashboard"
status: deferred
priority: P2
size: M
theme: "[E7] Tooling & evaluation"
story: "[S18] Cut session friction with better tooling"
serialize-group: settings-json
generates: BACKLOG.md
---

- [#322] [P2][M] Fleet dashboard — a human-facing fleet-observability surface, three legs: (a) DATA SOURCES (existing, reuse-don't-rebuild) — the `boundary_report` `logs/BOUNDARY-DRIFT.md` digest + the `fleet_health.py` SessionStart digest; (b) VISUALIZATION LAYER — the rendering surface, decided by the C4 codemap/diagram research (architect-owed); (c) SURFACING HABIT — how it enters the loop (a SessionStart line / the morning brief) so it is consulted, not built-then-ignored (the fleet-audit rent-rule). Data-sibling of #270 + #171. · Done when: the three legs are decided (data sources named, viz layer C4-ruled, surfacing habit chosen) AND a minimal dashboard renders from live fleet data with a surfacing hook · refs scripts/boundary_report.py, scripts/fleet_health.py, #270, #171 · kill-candidates: none — new fleet-observability surface gated on the C4 viz research · serialize-group: settings-json · DEFER — **DATED REVIEW 2026-09-09** (register `protocols/STANDING_RULINGS.md` I-D item 13). The former peg "C4 visualization research" is RETIRED: a peg whose referent will not occur tests nothing, so the trigger is a date. Row stays open; date = the repo's 30-day review cadence from the ruling date, the operator having named none
