<!-- fixture provenance: copied verbatim (2026-09-25) from
     H:\My Drive\CLAUDE PROMPT DIR\to-browser\REFUSED-lane-hooks-port.md
     for tests/test_learning_distiller.py (LANE-5B2-13-learning-distiller). Content below is
     unmodified except for this header. -->

from: the INTEGRATOR
repair 1 of 2
date: 2026-09-25
batch: WAVE5B-N1
lane: lane-hooks-port (LANE-5B-5-hooks-port.md), branch worktree-lane-hooks-port @ 76eda9c1

# REFUSED — lane-hooks-port, repair 1 of 2

## What failed

CI on the integration merge (run 36078947609, and again on 36079008845, Linux runner) — **four
reds in a test file this lane rewrote**, not in main's paired set:

```
tests/test_surface_triage.py::test_zero_open_triage_issues_is_silent
tests/test_surface_triage.py::test_open_triage_issues_are_surfaced_with_count_and_numbers
tests/test_surface_triage.py::test_a_single_open_triage_issue_uses_the_singular_word
tests/test_surface_triage.py::test_malformed_issue_json_is_swallowed_fail_soft
E   AssertionError: assert '[gh] auth invalid -- run: gh auth refresh -h github.com' == ...
```

Cause (read, not guessed): `_fake_gh()` writes only a Windows `gh.cmd` shim. On POSIX
`shutil.which("gh")` (scripts/surface_triage.py:34) does not resolve a `.cmd`, so it finds the
runner's real, unauthenticated `gh`, and `gh auth status` fails. The tests pass on Windows and
fail on exactly the substrate this port exists for (Linux / the container). The same fixture
shape may affect `tests/test_billing_leak_sentinel.py` if it stubs a CLI the same way — check it.

Everything else was green: lane-changed tests on the merged tree (Windows) 73 passed; ship-gate
hard-fail 0 -> 0 (+2 fleet_parity WARN-undeclared for the two new hook commands, +1 organ_truth
count — findings, not refusal causes); post-merge check clean.

## Cure (the lane's to make; nothing weakened)

- Make the fake `gh` resolvable on POSIX too: also write an executable `gh` (a `#!` script
  running `sys.executable fake_gh.py "$@"`, `chmod +x`) beside `gh.cmd`, and keep PATH pointing
  only at the fixture dir for the tests that must not see a real `gh`.
- Prove it on Linux, not only on this box: push the branch and paste the Actions run id whose
  `pytest` job shows `tests/test_surface_triage.py` green (dispatch `conductor.yml` on your branch:
  `gh workflow run conductor.yml --ref worktree-lane-hooks-port`).
- Your Done-when item 3 stays recorded as PARTIAL in your own words (median not below before);
  the integrator does not ask you to re-measure it.

## Sync rule

Sync from origin only: `git fetch origin` then `git merge origin/main` (main is now 4fab7aea).
Never `git merge main`. Purity before handback: `git log origin/main..HEAD` = your commits and
merges of origin/main only. Hand back with the machine line
`HANDBACK worktree-lane-hooks-port @ <sha> code` in `to-browser/SESSION-lane-hooks-port.md`.
