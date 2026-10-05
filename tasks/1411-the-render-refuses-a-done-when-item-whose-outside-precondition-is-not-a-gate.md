---
id: "[#1411]"
title: "The render refuses a Done-when item that depends on state outside the lane unless the contract names that precondition as a gate"
status: open
priority: P2
size: M
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1411] [P2][M] **The render refuses a Done-when item that depends on state outside the lane unless the contract names that precondition as a gate** - W1-12 `b2-codespace-green`'s Done item 6 (three consecutive all-green R63 runs, C3's merge leg included) needed a green CI push verdict, which needs main's own CI green; main's CI was red or cancelled, so the item could not pass whatever the lane did, and the lane looped on it (DECIDED-BY-SEAT A, 2026-10-05 21:34Z). The render's checks (plan lint, vacuity probes, RED premises, dry-runs) all passed it: none asks whether a Done item can be met from inside the lane · Done when: (1) the render step (its checklist and `plan_lint`) refuses a Done-when item that names state the lane does not own (main's CI verdict, another lane's merge, a provider's service, an operator login) unless the contract names it as a gate (`gate: <precondition>`, read by the dispatcher as a HOLD or a `WAITING` fate, not a failure); (2) a gated item whose precondition is false at the lane's close ends `WAITING <gate>`, never a repeated attempt; (3) RED-first tests: a contract carrying W1-12's item 6 text without a gate line is refused (fails on `9c72c990`), and the same item with `gate: main's CI push run green` passes · kill-candidates: none -- `[#652]` is a gate that passes when its precondition is absent, the opposite shape; `plan_lint.py` has no precondition rule (`git grep -n precondition scripts/plan_lint.py` = 0) · refs `scripts/plan_lint.py`, `templates/lane-contract-template.md`, `scripts/dispatch.py`, `[#652]`, `[#1410]` · source: `LANE-B2-W1-b2-codespace-green.md` Done item 6; B2-W1 integrator receipt `to-browser/SESSION-integrator-b2-w1-2026-10-04.md` (DECIDED-BY-SEAT A 21:34Z); render record `to-browser/SESSION-gen-b2-w1-record-2026-10-04.md` §"AMEND-5"
