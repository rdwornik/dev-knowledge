---
id: "[#1481]"
title: "test_filled_waiver_refuses_a_malformed_seats_row reads live CI state, so it reds on the windows runner"
status: open
priority: P2
size: S
theme: "[E10] Batch convergence"
story: "[S28] File every owed item with in-repo provenance"
generates: BACKLOG.md
---

- [#1481] [P2][S] **test_filled_waiver_refuses_a_malformed_seats_row reads live CI state, so it reds on the windows runner** - `tests/test_gen_handoff.py:600-609` calls `gh._self_inflicted_bd_manifest` after the fill without pinning the live readers; its sibling `test_filled_waiver_refuses_a_ci_row_that_does_not_name_the_cuts_own_sha` pins them first (`_live_state(monkeypatch, ci=..., seats=_SEATS_AT_CUT)`, `:594`). The un-pinned test reads the live CI state at run time: it was green on the windows leg of push run `37839948936` (3 attempts) and red on the windows leg of the B2-W2 lane-1 merge run `37984981579` and in the integrator's paired local runs. Filed as ROWS-OWED (ii) of seat ruling S-15 (`to-cc/AMEND-BATCH-B2-W2-ROUND2-2026-10-09.md` §1 condition 5) · Done when: (1) the test pins its live readers as its `:594` sibling does, and asserts the same refusal it asserts today; (2) it passes on both CI legs with no registry entry; (3) RED-first: with the live CI reader returning a non-green state, the un-pinned test fails on `aaf43867` · kill-candidates: none -- no open row owns this test (`[#1427]` is the BD-ci gate-job count, a different defect) · refs `tests/test_gen_handoff.py`, `scripts/gen_handoff.py` · source: `to-cc/AMEND-BATCH-B2-W2-ROUND2-2026-10-09.md` §1 (S-15 condition 5 (ii)); `to-browser/SESSION-integrator-b2-w2-2026-10-09.md` (the paired base run); B2-W3 render challenge of lane 2
