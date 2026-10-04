---
id: "[#1366]"
title: "A Codespace lane is production only when the five end-to-end conditions hold on three consecutive runs"
status: open
priority: P1
size: L
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1366] [P1][L] **A Codespace lane is production only when the five end-to-end conditions hold on three consecutive runs** - R63 (operator, 2026-10-03): every Codespace lane has the full toolset (`claude` pinned to the local version, `gh`, `codex`, `agy`, `rclone`) through the devcontainer and provisioning. No production lane goes to a Codespace until all five conditions are measured: (a) `codespace_parity.py check` passes with no NOT-RUN leg, (b) a real backlog task runs the whole line in a Codespace, (c) the dispatcher sees the lane live and absent after teardown, (d) a fresh Codespace rebuilt from nothing passes, (e) (a)-(d) hold on 3 consecutive runs. The git flow for remote lanes is designed, and logs and telemetry outlive the container. · Done when: a recorded run table shows (a) to (d) passing on three consecutive runs; `dispatch.py` refuses to route a production lane to a Codespace while the table does not; logs and telemetry of a torn-down Codespace remain readable; every stop records its reason, asserted by a test over the stop record · owner: lane `b2-codespace-1to1` (W1-7) measures the first run; B2 W2 closes the three-run condition · touches: `scripts/codespace_parity.py`, `scripts/dispatch.py`, the devcontainer, tests · kill-candidates: `[#1335]` -- it states the same five parity items without the three-run, refusal and observability legs; the integrator folds whichever is narrower · refs `[#1335]`, `[#554]`, `scripts/codespace_parity.py`, `protocols/STANDING_RULINGS.md` section AR (R63) · source: batch B2-W1 lane b2-rulings-landing (AMEND-B2-W1-2, item 2), R63 in `to-browser/RATIFICATION-2026-10-03.md R63`
