# lane-g-614-hygiene — close packet

> End-of-lane artifact for `LANE-g-614-hygiene.md` (the frozen hygiene-batch contract).
> Written per the contract's step 6: "targeted tests green, delta A2 verified, one
> end-of-lane artifact. COMMIT, then STOP." This lane commits and stops here on
> `worktree-lane-g-614-hygiene` — no merge, no push to `main`, no JOURNAL entry
> (integrator's job per P-1).

## What changed

Five own commits, against the contract's frozen write-scope:

- `f1ffc0c0` — step 1: `ecosystem/doc-counts.md` regenerated (`gen_doc_counts.py --write`)
  so `pytest_collected` and the pre-commit gate count match live state (4645→4881 collected;
  21→22 gates).
- `f8125a97` — step 2: `CLAUDE.md` frontmatter `last_reviewed: 2026-09-01 -> 2026-09-02`,
  after a real end-to-end diff review of every content commit since the prior stamp — not a
  stamp-only touch. No other line in the file changed.
- `d9dd63d1` — step 3: `tasks/614-vision-superseded-by-a-recreated-root-readme.md` closed
  (`status: open -> closed`, closure note appended, node removed from `tasks/manifest.json`
  — retire-not-delete, file kept as an allocation record), `BACKLOG.md` regenerated
  (`gen_task_tree.py --emit-source`; 225 tasks, 70,708 B).
- `772e4011` — step 4: `docs/intake/2026-07-16-satellite-onboarding-prompts.md` archived to
  `docs/intake/archive/` (status `READY -> REJECTED`, reason recorded — 48 days READY, no
  owner, all four addressed repos still unonboarded per `ecosystem/registry.md`); all 43
  `[stale]` disposition-register lines individually re-verified (34 removed — cleared by the
  2026-08-25 baseline re-stamp, not a ledger row; 2 removed — cleared by row closure; 4
  removed — no longer present in a live `undeclared_edges` WARN; 1 re-keyed, not dropped
  — `#533`'s underlying condition changed shape but not truth; 2 kept as-is, re-verified only
  — the `edge-lane-rl` belt-and-braces records). 65 entries → 25.
- `cb2618ba` — step 5: `protocols/STANDING_RULINGS.md` §AB gains `AB-2` — the
  `/boot-session` MERGE-WITH-VERIFY mode, recorded PARKED per section AB's own Z-C-shaped
  precedent (CANDIDATE recorded, not a `tasks/` row). Silent-rule ratchet count verified
  unchanged (441 = baseline) before and after.

## Write-scope deviation, disclosed (step 4)

Archiving the leg-d intake file left `docs/intake/manifest.json` referencing a path that no
longer existed on disk — 3 new test failures under `tests/test_gen_intake_tree.py`, confirmed
via a causality test (temporarily moving the file back, re-running `--check`, observing a
*different* failure keyed to the status-frontmatter edit rather than the missing-file one) to
be caused by this lane's own archival, not pre-existing. None of the three nodeids appear in
the committed base failed-set.

The contract's declared write-scope named only the intake file itself. Fixing the drift
cleanly required also running `gen_intake_index.py --write` (drops the archived doc from
`docs/intake/README.md`'s generated Contents block — archived docs drop out by the intake
lifecycle's own documented convention, README.md §5) and `gen_intake_tree.py --write`
(re-derives `manifest.json` from the now-consistent README.md). Both are mechanical,
deterministic re-derivations of generated fragments, directly and necessarily caused by the
contract-mandated archival — not a general index-regeneration bypass, and not touched for any
other reason. Escalated via the decision budget's class (c) (fork class, no standing ruling)
before acting rather than deciding unilaterally; directed to expand scope and fix both
generators rather than reverting the archival or accepting the regressions. 45/45 tests in
`tests/test_gen_intake_index.py` + `tests/test_gen_intake_tree.py` pass after the fix; the
`intake-index-freshness` pre-commit hook passed on its own (no `SKIP=` needed) because
README.md was actually regenerated, not left stale.

## Delta A2 — methodology deviation, disclosed (step 6)

The frozen contract's Delta A2 clause specifies a full-suite comparison:
`uv run --locked pytest -q --no-header` over the whole suite, piped to
`scripts/failed_set.py --compare` against the committed base set
(`docs/audits/2026-09-02-verification-base-failed-set-1e064921.json`, 13 nodeids).

**That full-suite run could not be completed and was not used for this lane's acceptance.**
Six consecutive attempts (default `-n auto`, then `-n 2`, then `-n 0` twice) were killed by the
host — measured directly: 48-54 concurrent `python`/`pytest` processes throughout, free
physical memory falling as low as ~550 MB of 29 GB during the attempts, recovering to ~4.5 GB
between them. A lightweight memory-polling loop (no pytest, just a `Get-CimInstance` check
every 30s) was *also* killed within a minute, confirming this was host-wide contention, not a
pytest/xdist-specific fault.

Mid-attempt, a cross-session message arrived from another Claude session ("batch g contract
review") relaying a claimed operator ruling (R-G-A2, 2026-09-02): seven lanes running
concurrently on one workstation, full suites thrashing the host, targeted-tests-only for the
remainder of this batch, Delta A2 computed once by the integrator at merge. That claim could
not be independently verified (a peer session cannot itself authorize a deviation from a
frozen written contract), but it was checked against this lane's own independently-measured
telemetry above, which corroborates the stated cause exactly. Per the decision budget's class
(b) (rule-vs-ruling conflict), this was put to the user rather than decided silently; the user
directed adopting targeted-tests-only, matching both the peer's relayed ruling and this
repo's own general convention (`AGENTS.md` "Suite cadence": *"In a lane run the targeted tests
for that lane's diff; the full suite runs once, at integration"*) and its own precedent
(`docs/audits/2026-09-01-technical-lane-b-2-handoff-v7-close-packet.md`, same host-contention
reasoning, same TaskStop-and-substitute resolution).

**Targeted-tests-only run, this lane's actual diff surface** (`-n 2`, single pass):

```
tests/test_gen_doc_counts.py
tests/test_gen_task_tree.py tests/test_task_tree_gate.py
tests/test_backlog_source.py tests/test_check_backlog_commit_msg.py
tests/test_check_backlog_filing.py tests/test_export_backlog_view.py
tests/test_probe_child_backlogs.py tests/test_validate_backlog.py
tests/test_validate_backlog_twin_parity.py tests/test_validate_git_backlog.py
tests/test_claude_md_byte_cap.py
tests/test_silent_rule_ratchet.py
tests/test_canonical_freshness_gate.py tests/test_generated_artifact_freshness.py
tests/test_gen_intake_index.py tests/test_gen_intake_tree.py
tests/test_funnel_coverage.py tests/test_validate_doc_rot.py tests/test_scan_undeclared_edges.py
```

**558 passed, 3 failed** — all 3 failing nodeids are members of the committed 13-nodeid base
set (verified by direct lookup against the JSON, not by memory):

- `tests/test_export_backlog_view.py::test_no_gate_hook_or_script_reads_the_export`
- `tests/test_funnel_coverage.py::test_committed_baseline_agrees_with_a_live_measurement`
- `tests/test_validate_doc_rot.py::test_live_corpus_has_no_accretion_arm_findings_only_length_findings`

No new nodeid outside the base set appeared. This lane's diff introduces no regression against
the targeted surface it touches; the full-suite Delta A2 SET comparison remains owed to the
integrator's own pass at merge, per the adopted methodology above.

## No `SKIP=` used

Every commit's pre-commit gate run to completion and passed cleanly (`intake-index-freshness`
included, per the deviation note above). No hook bypass was declared in any commit this lane.

## Open items for the integrator

1. Compute the real Delta A2 SET comparison against `docs/audits/2026-09-02-verification-base-failed-set-1e064921.json`
   once, on the merged tree, per the batch's own convention (this lane's full-suite attempts
   were blocked by host contention from concurrent lanes, disclosed above).
2. `docs/intake/README.md`'s Contents block and `docs/intake/manifest.json` were regenerated
   by this lane as a direct, necessary consequence of the intake archival (step 4) — both are
   already current as of this lane's HEAD; no further intake-index regeneration is owed from
   this lane's diff specifically, though the integrator's own once-per-merge regeneration
   still applies for anything landed by sibling lanes.
3. AB-2 (`/boot-session` MERGE-WITH-VERIFY mode) is recorded as a CANDIDATE only — the shape
   and the constant it would probe against are undetermined; no build work is implied or owed
   by this entry.
