---
id: "[#1634]"
title: "Hub dispatch shim installed; duplicate launchers removed on GO"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1634] [P2][M] **Hub dispatch shim installed; duplicate launchers removed on GO** - The hub dispatch shim is installed and the duplicate win-tooling launchers are removed on the operator's GO per list. Three local launchers run today: `dispatch.py launch`, win-tooling `Invoke-Dispatch` / `Start-DispatchLane`, and the PATH `dispatch` wrapper (Aug 11, no `dispatch.py` string); `templates/dispatch-shim.ps1` is not installed (operator copy). Also `Dispatch-CloudBrief`, `Dispatch-After`. owner: operator (install, deletion GO); CC prepares the list. target batch: D1 · Done when: `dispatch` typed on the laptop resolves to the hub shim (hash shown); each deletion has an operator GO line per entry; real-use witness: the next launch receipt shows `dispatch.py` as the caller · touches: see the body · kill-candidates: none -- code deletion is the operator's · refs `templates/dispatch-shim.ps1`, `to-browser/DIGEST-DISPATCH-ARCHITECTURE-2026-10-18-ANNEX.md` A · source: BATCH-D0-PROCESS-2026-10-18 section 0.4 (operator GO 2026-10-18: plan OK, D0)
