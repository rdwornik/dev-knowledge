# lane-nb-tiering — [#598] the durations measurement, and the STOP it triggered

> Sibling artifact to `docs/audits/2026-08-27-technical-lane-nb-tiering.md` (which covers [#597]
> and deliberately makes no claim about the suite's shape — audits are immutable, and this
> measurement had not returned when that file was sealed). Lane `lane-nb-tiering`, branch
> `worktree-lane-nb-tiering`. Evidence input: PERF-RECON B9/B10
> (`docs/audits/2026-08-26-technical-perf-recon.md`).
>
> **Architect amendment, operator-approved, executed here:** cut the measurement short — kill the
> serial arm, cite the repo-recorded serial reference instead of re-measuring, treat the parallel
> arm's `exit=1` as a finding rather than noise, decide [#598] on the table already in hand, and
> execute the narrow path only.

## Verdict

**LONG-POLE. The marker sweep is STOPPED and nothing was marked.** The row narrows per its own
done-when, exactly as the contract instructed: *"if the suite is long-pole (top25 >20% wall), STOP
the marker sweep, report, and fix nothing."*

The only thing executed under [#598] is **B10**, which the contract names separately and
unconditionally.

## 1. The measurement, and what it cost

One arm was run to completion; the second was killed under the amendment.

```
arm        command                                          exit   wall_ms      outcome
parallel   pytest --durations=25 -q  (the default -n auto)     1   1440944   35 failed, 3931 passed,
                                                                            21 skipped, 1 xfailed
serial     pytest -n 0 --durations=25 -q                       -         -   KILLED per the amendment
```

**The serial reference is cited, not re-measured** — `pyproject.toml`'s xdist-adoption note records
it at **1785.61 s** (2026-08-06, same tree/day: serial 1785.61 s vs `-n auto` 358.77 s / 330.15 s,
with pass/fail counts identical across all three runs). Citing a repo-recorded number instead of
spending 30 minutes reproducing it is the amendment's call and it is the right one; the honest
caveat is that the figure is three weeks old and the suite has since grown from ~2362 to **3988**
collected, so it is a floor, not a current wall.

## 2. The top-25 table (parallel arm)

```
   718.62s  test_hub_identity.py::test_no_hub_only_check_skips_when_the_stored_path_is_stale
   688.77s  test_writer_integrity.py::test_live_registry_has_no_unconditionally_inert_check_left
   681.29s  test_audit.py::test_health_degraded_no_ecosystem
   676.28s  test_membership_agreement.py::test_declaration_leg_works_under_package_mode_invocation
   459.13s  test_review_artifact_coverage.py::test_leg_is_advisory_on_the_live_repo
   157.00s  test_audit.py::test_health_ok_with_registered_repo
   151.82s  test_toc.py::test_corpus_fence_fix_never_drops_a_header_from_OUTSIDE_a_code_block
   116.87s  test_normalize_headers.py::test_corpus_no_code_block_line_is_ever_modified
   112.56s  test_session_end_backpressure.py::test_e2e_five_paths
   102.56s  test_carrier_hooks_source.py::test_carried_backlog_id_blocks_unreferenced_close
    98.58s  test_audit.py::test_health_stays_ok_with_na_status
    95.06s  test_verify_handoff_probes.py::test_registered_check_never_fails_on_live_repo
    91.80s  test_adr85_integration_enforcement.py::test_t3_pre_push_has_no_retry_surface
    87.89s  test_normalize_headers.py::test_corpus_rewriter_still_fires_on_real_documents
    86.79s  test_carrier_hooks_source.py::test_carried_block_ff_push_refuses_direct_to_main
    75.64s  test_normalize_headers.py::test_corpus_every_rewritten_line_is_syntactically_a_heading
    73.64s  test_normalize_headers.py::test_corpus_heading_map_indices_land_on_heading_syntax
    72.50s  test_doc_code_edge.py::test_edge_check_registered_and_resolves_starter_set
    62.52s  test_block_ff_push.py::test_precommit_adapter_feature_only_clean_main_passes
    56.66s  test_fleet_parity_events.py::test_events_rotation_is_windows_safe
    55.25s  test_hook_telemetry.py::test_exit_codes_do_not_move_with_telemetry_on[block-unanchored-push]
    54.49s  test_floor_conformance.py::test_layer2_path_scopes_unresolvable_repo_and_passes
    54.46s  test_block_ff_push.py::test_precommit_adapter_multiref_dirty_main_stays_refused
    52.28s  test_cloud_provisioning.py::test_an_unknown_required_ref_is_a_violation_not_a_crash
    49.99s  test_generated_artifact_freshness.py::test_live_a_generator_source_change_alone_makes_the_artifact_stale
```

## 3. Applying the rule — and being careful about the denominator

`--durations` sums **per-test call time**, which under `-n auto` accumulates across workers. So
`top25 / wall` is not apples-to-apples and would flatter the long-pole reading. Three denominators,
the strictest one decided it:

```
top-25 sum                                        4932.45 s   (25 of 3988 tests)
top-5  sum                                        3224.09 s
parallel wall                                     1438.98 s
total worker-seconds  (wall x 16 logical CPUs)   23023.68 s

top25 / worker-seconds   21.42%   <-- the fair denominator. Threshold 20%. LONG-POLE.
top25 / parallel wall     342.8%
top25 / recorded serial   276.2%   (against pyproject.toml's 1785.61 s)
top5  / worker-seconds   14.00%
```

**The verdict does not depend on which denominator you pick** — the loosest reading clears 20% by
17x, and even the strictest, which charges the suite for every idle worker-second on a 16-core host,
clears it. Twenty-five tests out of 3,988 hold more than a fifth of all worker time. That is the
definition of long-pole, and the row said to stop there.

## 4. The finding that matters more than the ratio

**Four of the top five poles are not "slow tests" in B9's sense at all — they run the LIVE audit.**
`test_no_hub_only_check_skips_when_the_stored_path_is_stale`,
`test_live_registry_has_no_unconditionally_inert_check_left`, `test_health_degraded_no_ecosystem`
and `test_leg_is_advisory_on_the_live_repo` each drive `ALL_CHECKS` (or `cmd_health`) against real
repos. They are expensive for exactly the reason `audit.py health` is expensive.

So the suite's pole and the commit gate's pole are **the same object**, and B9's proposed remedy is
aimed somewhere else. A `slow` marker over "tests that spawn a subprocess" would have marked
**60 files** (measured live: 64 files match a `subprocess.`/`sys.executable` pattern, 4 carry a
marker) and still not moved the top five, because those five are slow from the audit they run, not
from a spawn count. PLAYBOOK Ch5 already records the shape of this — *"one test carries 38.4% of
it"*, and *"`pytest -m "not slow"` removes almost none of the 89%"* — and this measurement confirms
it on a corpus 1.7x larger.

**The lever is therefore [#597]/W2A, not markers**, which is a pleasant result to be able to state:
the work that makes the commit gate cheaper is the same work that makes the suite's poles cheaper,
and it needs no authoring obligation on 60 files to do it. Marking those files would have been
motion — a hand-maintained selector, rotting from the day it landed, in front of a cost it does not
sit on.

**What was NOT done, and is not owed by this row:** no `slow` marker was applied, the `-m "not slow"`
per-merge cadence line was NOT landed in PLAYBOOK Ch5, and the spawn-pattern coverage lint was NOT
built. All three were conditional on a long-tail result. PLAYBOOK is untouched by this lane.

## 5. `exit=1` — attribution of all 35 failures

The amendment is right that this is a finding rather than noise. **None of the 35 is attributable to
act 1's tier change**, and the attribution below is by observed cause, not by assumption.

| n | Failures | Cause | Attribution |
|---|---|---|---|
| 17 | `test_fleet_analytics.py::*` | `ModuleNotFoundError: No module named 'pandas'` | **Lane-venv environment.** The lane worktree's venv lacks the `analytics` dependency group. Not code. |
| 9 | `test_nopack_sandbox.py::*` | `rc=127` / `assert 127 == 0` — command not found | **Environment.** The sandbox probe's allowlisted binaries are absent in this shell. Not code. |
| 2 | `test_verify_handoff_probes.py::*` | `['tool absent: sed']`, `['skipped'] == ['pass']` | **Environment**, same absent-tool class. |
| 2 | `test_audit.py::test_health_ok_with_registered_repo`, `::test_health_stays_ok_with_na_status` | both assert `cmd_health` exits 0 against the LIVE repo | **Pre-existing, PROVED:** this lane's own pre-edit baseline run of that same path already exited 1 on the foreign `journal_spine_anchor` FAIL at `08b0d192` (sibling artifact §5/§8). |
| 1 | `test_stale_worktrees.py::test_linked_worktrees_reader_excludes_the_primary` | primary-vs-worktree path assertion | **Worktree substrate.** A full suite run from inside a linked worktree reds this by construction. |
| 1 | `test_enforcement_coverage.py::test_anchor_gate_probe_distinguishes_installed_from_absent` | `pre-push hook 'block-unanchored-push' runs block…` | **Pre-existing on main** since 2026-08-22. |
| 1 | `test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export` | *"the export is read by governance: ecosystem/conformance.htm…"* | **Pre-existing** known false positive; `ecosystem/` lacks the naming-vs-reading carve-out. |
| 1 | `test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings` | `RotFinding(category='backlog-accretion', locus='BACKLOG#348', …)` | **Pre-existing, and CHECKED rather than assumed.** The suspicion was that act 1's ARCHITECTURE.md history entry caused it; the finding's locus is `BACKLOG#348`, not `ARCHITECTURE.md`. Not this lane. |
| 1 | `test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement` | 44 artifacts carry no disposition | **Pre-existing, and this lane ADDS ONE — stated because it is the honest half.** 43 of the 44 predate this lane (2026-08-23 → 2026-08-26); the 44th is this lane's own `2026-08-27-technical-lane-nb-tiering.md`. The test was already RED; the lane did not cause it, but it did lengthen the list. |
| **35** | | | **0 attributable to the [#597] tier change** |

**The funnel row is left open, deliberately, and the reason is a governance question this lane may
not answer.** The check wants a row in a *disposition ledger*, and the live ledger is
`docs/audits/2026-08-17-technical-audit-disposition-ledger.md` — itself an **immutable audit
artifact** (CLAUDE.md §5 rule 3). How a new artifact records a disposition into an immutable ledger
is undecided, which is visibly why 43 artifacts across five days are undispositioned rather than
one. Inventing a mechanism here would be a lane deciding a governance question in passing. Recorded,
with the count, for the funnel owner.

## 6. B10 — fixed, and it is more than a speed-up

`scripts/validate_doc_claims.py::_derive_pytest_collected` spawned a nested `pytest --collect-only`
passing `-p no:cacheprovider` but **not** `-o addopts=`, so it inherited the repo's own
`addopts = "-n auto"` and booted a full 16-worker xdist pool to answer one collection question.
`scripts/worktree_import_proof.py` already passed the flag with the comment *"drop the repo's own
addopts (e.g. `-n auto`)"*; this call did not. Same defect class `pyproject.toml` documents for
mutmut.

Measured after the fix: **3,988 collected in 6.0 s**, in-process, no pool.

It is also a **strengthening**, not only a speed-up: the collected count is identical either way
(the repo's own 2026-08-06 evidence), but `--collect-only -q` parsed out of a worker pool's output
is a less deterministic thing than the same command run in-process — and this deriver's contract is
to return a parsed integer or fail soft.

The fix moved `ecosystem/doc-counts.md` from **3977 → 3988 collected**, which is act 1's added tests
landing in the count fragment; regenerated with `gen_doc_counts.py --write`.

## 7. Honest limits

- **The serial arm was not run.** Its wall is cited from a three-week-old repo record against a
  suite that has grown ~69% in collected tests. The long-pole verdict does not rest on it — it
  holds on the parallel arm's own worker-seconds — but any *ratio* quoted against 1785.61 s is a
  floor.
- **The parallel arm ran on a contended host.** Concurrent `audit.py run` SessionStart sweeps from
  sibling sessions, plus act 1's own commit hooks, overlapped it. That inflates the absolute
  durations — a 718 s single test is contention, not a steady-state cost — and it inflates the
  top-25 sum in the numerator. It does **not** rescue the verdict: contention would have to be
  wrong by more than 17x for the loosest denominator to fall under threshold, and the top-25 are
  disproportionately the live-audit tests that contention hits hardest, which if anything means the
  *quiet-host* pole is even more concentrated in those same few tests.
- **`top25 / worker-seconds` charges the suite for idle workers.** It is the strictest available
  denominator and is used deliberately, but a suite that cannot saturate 16 workers is being
  measured against capacity it never had. The looser readings are given alongside so the reader can
  pick.
- **"Not attributable to the tier change" is an attribution, not a proof.** It rests on each
  failure's observed cause and on the pre-edit baseline for the two `cmd_health` tests. No
  before/after full-suite pair was run — the amendment forbids further full-suite runs, correctly.
- **60 unmarked spawn-pattern files remain unmarked**, and that is now a recorded decision rather
  than an omission: the measurement says marking them would not buy the per-merge tier anything.

## 8. Disposition

[#598] — **narrowed by its own done-when.** The gating measurement returned LONG-POLE, so the
marker sweep, the PLAYBOOK Ch5 cadence line and the coverage lint are all correctly NOT executed.
B10 is fixed. The row's residual value, if any, is re-pointed at the poles themselves — which are
the live-audit tests [#597] and W2A already make cheaper.

ACTIONED.
