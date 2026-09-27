# CI OS matrix — one run, both legs, durations recorded (LANE-5B4-3, proposal row L1)

carried-by: lane-ci-matrix (WAVE5B-N4)
date: 2026-09-27
contract: to-cc/LANE-5B4-3-ci-matrix.md
basis: to-browser/PROPOSAL-ADR-CI-VERIFICATION-2026-09-26-seat-71020de7.md Decision D1, row L1 (Blockers table)
method: pushed worktree-lane-ci-matrix at sha 4ad29e44 (`.github/workflows/conductor.yml` +
`tests/test_conductor.py` changed); read the triggered conductor.yml run back with `gh run view`
(read-only); pulled both `pytest` job logs with `gh run view --job <id> --log` and grepped them.
Nothing else was run or written to produce this file.

## L1's Done-when, verbatim

> one run on a `worktree-*` push completes both legs; both durations in the audit; 0 "main does
> not resolve" reds

## The run

- Run: <https://github.com/rdwornik/dev-knowledge/actions/runs/36304438895>
- Trigger: `push` to `worktree-lane-ci-matrix` (matches the widened `worktree-**` pattern)
- sha: `4ad29e44ad4a41a479b5b5964f8c517df8c4c61e`
- Both `pytest (ubuntu-latest)` and `pytest (windows-latest)` reached `completed` in this one run
  — `fail-fast: false` meant neither leg's red cancelled the other before its duration was known.

## Both durations (same run, same sha — the P7 comparable-timing fix)

- `pytest (ubuntu-latest)`: job wall 07:52:25Z → 08:03:01Z = **636 s** (10 m 36 s); pytest's own
  reported wall: **618.46 s** (0:10:18) — `89 failed, 8021 passed, 30 skipped, 3 xfailed`.
- `pytest (windows-latest)`: job wall 07:52:25Z → 08:05:33Z = **788 s** (13 m 8 s); pytest's own
  reported wall: **758.60 s** (0:12:38) — `75 failed, 8051 passed, 14 skipped, 3 xfailed`.
- Both numbers are from the SAME workflow run, on the SAME sha, unlike the proposal's prior
  measurements (Linux CI at one sha, Windows local at a different one) — P7's objection to the
  8.6x comparison answered directly: on one sha, in one run, Windows costs about **1.24x** Linux's
  wall time on these runners (4 vCPU / 16 GB, both), not 8.6x anything.

## Item 4 — the 40-minute flip condition

The Windows leg measured **758.60 s ≈ 12.6 minutes**, far under the 2,400 s (40 min) flip
condition the proposal's sensitivity note names ("A7 falls below A4 if the Windows leg exceeds
~40 min"). **Under it: the full suite stays the Windows leg's job — no flip.** Nothing is built for
a smoke tier because the measured condition that would trigger it did not fire. If a later run
crosses 40 minutes, the flip is `lane-arm-ci`'s (L6) to record and build, not this lane's.

## Item 3 — 0 "main does not resolve" reds (grep pasted)

Both `pytest` job logs, grepped for `does not resolve` and `Not a valid object name main`:

```
$ grep -i "does not resolve\|Not a valid object name main" windows-pytest.log
...E     release-lint WARN C2-tag: git tag v1.1.0 does not resolve yet -- pre-release state...
(2 hits, both this unrelated release-tag warning inside an already-known-red test; zero
"main does not resolve" hits)

$ grep -i "does not resolve\|Not a valid object name main" ubuntu-pytest.log
...E     release-lint WARN C2-tag: git tag v1.1.0 does not resolve yet -- pre-release state...
(2 hits, same unrelated warning; zero "main does not resolve" hits)
```

Both logs also carry, right after checkout on both legs:

```
branch 'main' set up to track 'origin/main'.
```

— the new `git rev-parse --verify --quiet refs/heads/main || git branch main origin/main` step
firing, confirmed by its own output, on both OSes.

Two of the three clone-artefact tests the proposal named at K2/T1
(`test_worktree_seed.py::test_the_verdict_names_WHY_rather_than_only_failing`,
`test_validate_branch_naming.py::test_local_branches_reads_the_live_repo`,
`test_provision_legs.py::test_history_check_exits_0_on_this_repo`) no longer appear in either
leg's failure list at all — they now pass, because `refs/heads/main` resolves. The third,
`test_worktree_seed.py::test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH`, still fails on both legs
— but its own assertion text shows why, and it is not this defect:

```
AssertionError: worktree.baseRef='head' resolves the base to dev-knowledge:HEAD (the dispatching
checkout) at 4ad29e44, but main HEAD is 1a0dc573 -- the dispatching checkout .../dev-knowledge is
not on main HEAD, so `head` seeds lanes from wherever it is sitting...
```

`main` resolves correctly to `1a0dc573` here — the failure is that the CI checkout (correctly, for
a lane push) sits on the lane's own tip, not on `main`, which this test treats as a misconfigured
dispatcher. That is an environment/host-witness class defect (T2's 18-member bucket), not a "main
does not resolve" clone artefact, and it is already carried in the known-reds registry (both legs'
"Compare against the committed known-reds registry" step logs it as `known`, not a regression).
Fixing it is `lane-host-witness`'s (L3) scope, not this lane's.

**0 "main does not resolve" reds, on both legs, evidenced above.**

## What is NOT claimed here

- **Neither leg is green.** Ubuntu reports 7 failures outside `logs/KNOWN-REDS-REGISTRY.json`
  (drift since the registry's 2026-09-26 freeze — unrelated to this diff); Windows reports 5. The
  registry is Linux-measured only (`measured_via: gh-run:35939312231`); `lane-known-reds-signatures`
  (L2, starts after this lane) owns making it OS-keyed so a Windows-only failure population stops
  reading as "5 unregistered regressions." This lane's Done-when asks the run to **complete** both
  legs with durations recorded, not to pass — see L1's Done-when above, which says nothing about
  a green verdict.
- **No ratchet claimed.** Per the common rules: "a lane does NOT run the full `audit.py ship-gate`
  or claim `tests/test_silent_rule_ratchet.py`" — nothing here claims either.
- **The ruleset is not armed and was not touched.** `deploy/conductor-required-checks.ruleset.json`
  still names the single `pytest` context; a Codex review of this diff (2026-09-27,
  `docs/audits/2026-09-27-codex-lane-ci-matrix.md`, High/1) found that the matrix now reports
  `pytest (ubuntu-latest)` / `pytest (windows-latest)` instead — RATIFICATION-2026-09-26 D3
  already names the matrix-scoped contexts as the intended required set, so this is
  `lane-arm-ci`'s (L6) update to make when it arms, not a regression introduced here; recorded as
  `ROWS-OWED` in the session file rather than fixed in a file this lane does not own.
