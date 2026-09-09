---
id: "[#655]"
title: "`run_retention()` has no production caller, and the ruled one is `fleet_health`'s daily run"
status: open
priority: P2
size: S
theme: "[E7] Tooling & evaluation"
story: "[S20] Revive the nightly layer, load-gauge first (rent-rule discipline)"
generates: BACKLOG.md
---

- [#655] [P2][S] **`run_retention()` has no production caller, and the ruled one is `fleet_health`'s daily run** — the log retention entry point is reachable only from its own tests, which is why the flat `PROPOSALS-*` artifacts accumulated in `logs/` until a lane swept them by hand. Lane V-5 escalated where the call belongs and the browser seat ruled it: **not** `propose_closures.py`, which collides with the batch-T error-marker ruling, but `fleet_health.py`, which already owns `logs/` and is the fleet's one live schedule. Wiring it there gives `run_retention` a trigger under the harness definition, so it stops being an orphan by the census's own rule rather than by argument · Done when: `fleet_health`'s daily run calls `run_retention`, a test fails if the call is removed, and one live run is witnessed against the artifacts the sweep left behind · refs DECLARE-BATCH-V-MERGE §2, `scripts/logs_retention.py`, `scripts/fleet_health.py`, `[#642]` · source: browser ruling on lane V-5's escalation, filed by batch V lane V-4
