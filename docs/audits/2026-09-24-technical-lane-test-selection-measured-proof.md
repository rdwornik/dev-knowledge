# Measured proof — the selector's before/after on the five wave-4b merge diffs

**Lane:** `lane-test-selection` · **Branch:** `worktree-lane-test-selection` · **Date:** 2026-09-24

Consumer: `[#1009]` (this lane's row, Done-contract item 3).

**Method.** Read-only against the live tree, per `scripts/impacted_tests.py`'s own honest
limit ("Selection is computed from the repo TREE, so it answers for the working state, not
for an arbitrary historical commit"). The five wave-4b merges named in the frozen contract's
Value line (`to-cc/DIGEST-AUDIT-CROSSCHECK-2026-09-23.md` C13, and
`to-browser/SESSION-integrator-wave4b-2026-09-22.md`) are the ones with a measured local
`compare`/pairing wall time: `lane-hooks-rearm`, `lane-plan-lint`, `lane-fleet-health-split`,
`lane-gate-verdicts`, and `lane-verify-in-lane` (repair). For each, `git diff --name-only
<parent> <merge-sha>` gave the changed-path list actually merged; that list was fed to
`impacted_tests.select()` twice — once against the pre-fix module (`git show
HEAD:scripts/impacted_tests.py` at this lane's start), once against the fixed one.

| merge | parent..tip |
|---|---|
| `lane-hooks-rearm` | `3689b5ab..2fd8f256` |
| `lane-plan-lint` | `2fd8f256..e8ec23fc` |
| `lane-fleet-health-split` | `de97dad5..10a4c9f5` |
| `lane-gate-verdicts` | `10a4c9f5..3d3b3a0e` |
| `lane-verify-in-lane` (repair) | `3d3b3a0e..4667f731` |

## 1 · Item 2's effect — the merge-receipts ledger, on the real diffs

`logs/MERGE-RECEIPTS.jsonl` is folded into every one of these five merges (the standing
close-out step). Before this lane it matched no rule in the table and fell to the
"unmapped" fail-safe.

| merge | before | after |
|---|---|---|
| `lane-hooks-rearm` | `full_suite=True` | 4 files |
| `lane-plan-lint` | `full_suite=True` | 4 files |
| `lane-fleet-health-split` | `full_suite=True` | 92 files |
| `lane-gate-verdicts` | `full_suite=True` | 6 files |
| `lane-verify-in-lane` (repair) | `full_suite=True` | 12 files |

**5 of 5 before, `full_suite=True` — worse than the 58-file union, and worse than the
Value line's own 30–64 minute figures suggest.** The reason the historical per-merge gate
runs did not visibly hit this: `gates.py`'s `impacted_tests_gate` selects against
`HEAD^1`/`main` at each commit, mostly before the ledger's append-and-fold step lands in
the same diff it inspects. Feeding the selector the FULL merge diff — which is what a
batch-wide or integrator-level check does — hits it on every single one of these five.
`gates.py` REFUSES rather than silently running the full suite when the selector declines
to narrow (`impacted_tests_gate`, "the impacted-test selector declined to narrow"), so this
was a standing risk of redding the per-merge gate on the ledger's own presence, independent
of anything a lane's own diff touched.

**After:** `logs/MERGE-RECEIPTS.jsonl` maps to a `fixed` rule targeting
`tests/test_merge_receipt.py` and `tests/test_lane_digest.py` — the two files that actually
assert on it — so its presence contributes two known tests instead of a full-suite refusal.

## 2 · Item 1's effect, isolated — the mixed-diff union, with the ledger set aside

To measure item 1 on its own (separated from item 2's full-suite masking), the ledger line
was removed from each diff before replay, on both the pre-fix and fixed module.

| merge | old (no ledger) | new (no ledger) | corpus-sized files removed |
|---|---|---|---|
| `lane-hooks-rearm` | 60 | 2 | 58 |
| `lane-plan-lint` | 60 | 2 | 58 |
| `lane-fleet-health-split` | 118 | 90 | 28 |
| `lane-gate-verdicts` | 62 | 4 | 58 |
| `lane-verify-in-lane` (repair) | 66 | 10 | 56 |

**4 of 5 merges dropped by exactly the 58-file `live_repo` corpus size** (the fifth,
`lane-fleet-health-split`, touches `scripts/audit.py` and `scripts/fleet_health.py` — two
hub modules with a large covering closure of their own, so its 90-file "after" answer is
legitimate covering-tier selection, not a doc-tier leftover, and the corpus overlaps that
closure by only 28 files). This matches the contract's Value line ("On 4 of 5 wave-4B
merges, the lane's own code reached 0 to 3 test files") almost exactly: `lane-hooks-rearm`
and `lane-plan-lint` land on 2 files (one covering + one self, or similar), `lane-gate-
verdicts` on 4, `lane-verify-in-lane` on 10.

**Mechanism.** Before this lane, `select()` resolved a MIXED diff's marker into
`live_repo_test_files(root)` — every test file in the corpus carrying the `live_repo`
marker (58 at the time of this measurement) — and unioned it into the lane's own
`test_files`, because `pytest -m live_repo a.py b.py` INTERSECTS rather than unions and the
old code worked around that by resolving the marker to files instead. The fix drops that
resolution: `Selection.marker` stays set (so a caller can tell a doc path also matched) but
never joins `test_files`; `pytest_args()` is unaffected by the marker whenever `test_files`
is non-empty, which is already true before this lane (unchanged code path), so the lane's
own selection is intact and the corpus union is gone. `Selection.docs_tier_args()` is the
new, separately-callable answer for the doc tier: `["-m", "live_repo"]` whenever `marker`
is set, for whoever owns running it — the integrator, once per batch, per the Done-contract.

## 3 · Combined effect (both fixes, real diffs including the ledger)

| merge | before (this selector) | after (this selector) |
|---|---|---|
| `lane-hooks-rearm` | `full_suite=True` (≈7343 tests) | 4 files |
| `lane-plan-lint` | `full_suite=True` | 4 files |
| `lane-fleet-health-split` | `full_suite=True` | 92 files |
| `lane-gate-verdicts` | `full_suite=True` | 6 files |
| `lane-verify-in-lane` (repair) | `full_suite=True` | 12 files |

## 4 · Honest limits

- **Computed against the live tree, not a historical checkout** of each merge — the
  selector's own stated limit. The covering-tier numbers (import-closure sizes) reflect
  today's module graph, which has grown since these merges landed; the doc-tier corpus size
  (58) is read the same way and is the number the contract's Value line itself cites.
- **Not a wall-clock re-measurement.** This table counts *selected files*, not minutes; it
  does not re-run `test_pairing.py compare` or `gates.py run` on a historical checkout to
  reproduce the 30–170 minute figures directly. `test_pairing.py`'s own consumption of
  `impacted_tests.select()` (`_selection_to_dict`, `scripts/test_pairing.py:335-357`) already
  uses `selection.test_files` as the file list handed to pytest, so a smaller `test_files`
  here is a smaller `compare`/pairing run there — unverified by re-running it in this pass.
- **`lane-fleet-health-split`'s large after-count (90/92) is not a defect.** It is the
  general import-closure trade-off this selector already accepted (`DEFAULT_DEPTH`,
  documented in the module docstring), triggered by touching two widely-imported hub
  modules in the same diff, not by anything this lane's fix changed about that mechanism.
