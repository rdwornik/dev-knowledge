---
id: "[#823]"
title: "The dispatch verb still boots a lane with no committed manifest -- only /lane-boot refuses"
status: open
priority: P1
size: S
theme: "[E2] Enforced governance"
story: "[S3] Turn advisory guards into enforced gates"
generates: BACKLOG.md
---

- [#823] [P1][S] **The dispatch verb still boots a lane with no committed manifest -- only /lane-boot refuses** - Lane ab-804 (merged `af69c92e`) wired `preflight_contract.check_open_batch` into `/lane-boot` through the new hub entry point `scripts/lane_boot.py preflight`, and stopped there by design: the `dispatch` verb lives in `win-tooling` (`Invoke-Dispatch.ps1`), outside that lane's footprint. So the path every batch lane actually launches through -- `dispatch LANE-<...>.md` -> `claude --bg ...` -- still starts a lane when no manifest is committed on `main`. The refusal exists and the launcher never asks it. · Done when: RED-first, `dispatch <contract> -Run` against a repo whose `main` carries no open batch manifest naming that lane REFUSES before any worktree or session exists, exits non-zero and names the missing manifest; its first act is `uv run --locked python scripts/lane_boot.py preflight` from the target repo root; a witnessed refusal is recorded in the lane artifact · refs `scripts/lane_boot.py`, `scripts/preflight_contract.py` (`check_open_batch`), `win-tooling` `Invoke-Dispatch.ps1`, `docs/audits/2026-09-16-technical-lane-ab-804-id-allocator.md` section 6 decision 1 · kill-candidates: none -- this is `[#804]` Done-when (1) at the dispatch verb, split out because it lands in another repo's footprint · source: operator order 2026-09-16, integrator-AB, from lane ab-804's report
