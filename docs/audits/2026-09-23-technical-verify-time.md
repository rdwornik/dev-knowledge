# DIGEST — where merge time goes (VERIFY-TIME, 2026-09-23)

> **Status:** landed verbatim by `lane-landing-window` (LANE-5A-5) from the transport, where it
> was `carried-by: OPEN` with no repo citation. Source: `to-browser/DIGEST-VERIFY-TIME-2026-09-23.md`,
> answering `to-cc/BATCH-AUDIT-VERIFY-TIME-2026-09-23.md`. Read-only measurement; nothing was
> repaired by the session that produced it. Corrections: 3 of its claims (C1 compare-cost range,
> C2 gates.py fixed cost, C5b failure-count low end) are superseded by
> `2026-09-23-technical-audit-crosscheck.md` — read that file's corrections table before citing a
> number from this one.
> Carrier rows: D1-D5 (`to-cc/DECLARE-WINDOW-DEFECTS-2026-09-23.md`), filed by `lane-landing-window`.

carried-by: CC session (hub root, read-only audit)
answers: to-cc/BATCH-AUDIT-VERIFY-TIME-2026-09-23.md
date: 2026-09-23
method: 4 Sonnet readers; no suite/ship-gate/pytest run; `impacted_tests.py select` replayed per wave-4b merge (file list only). Nothing written but this file.

## The answer in five sentences

1. A wave-4b merge costs 77–207 min pickup→push (median ~93). The fixed cost is `gates.py` (14–17 min) plus `test_pairing.py compare` (30–59 min at `-n 2`). Everything above ~75 min is discarded or fallback pytest wall-clock.
2. About 290–340 min of wave-4b's five merges was duplicate or discarded pytest, and wave 4 had about 85 min (narrow count) to 195 min (broad count). The biggest single source is the two-commit-pairing fallback that the registry `compare` forces when a test is UNATTRIBUTABLE or unregistered (170 min on fleet-health-split; 76 min killed and thrown away on gate-verdicts).
3. Selection is prose-driven. On 4 of 5 wave-4b merges the lane's own code reaches 0–3 test files, while `JOURNAL.md` alone pulls in the whole 58-file `live_repo` set: 256 of 276 selected-file slots (93%) come from prose or self-selection. The `live_repo` tests are also the historically slow ones.
4. CI already runs the whole 7,343-test suite in ~8 min (`-n 4`, ubuntu). The local merge spends 30–59 min comparing a 59–118-file subset. But CI is 20/20 red because the `suite-gate` baseline freeze is 6 days stale, so nobody can use its verdict: CI says failure and local says CLEAN on every sampled merge.
5. Memory, not CPU, sets the pace: 27.7 GB box, 3–6 GB free, `-n` hand-set to 2 (sometimes 4), ≤2 heavy seats by operator cap, and repeated reaper and OOM kills. The tools that would cut the work — lane-side record reuse [#960], memory-derived `-n`, an armed CI check — are unmerged, absent, or disabled.

## Per-merge time table (minutes; source: SESSION-integrator-wave4/4b logs, git commit times; "dup" = work repeated or thrown away)

```
WAVE4 (5 merges; wall first→last push 05:12Z→15:58Z = 10h46m; plus overnight 1h46m idle, 54m Sonnet-500 outage)
merge | lane | pickup→push | steps (min) | dup min | what repeated
8746b741 | known-reds | 351 (incl 54 outage) | pairing 110 (discarded on refusal) · pairing 121 (after a reap; first attempt 5-7 wasted) · gates -n2 15 | 118 (+~6) | first pairing thrown away; impacted-tests re-ran the set pairing's head leg had just run (8)
cd6e0d34 | connection-hygiene | 154 | shared base record 44.5 · compare 29.5 → UNATTRIBUTABLE · two-commit pairing 63 · gates -n4 13.8 | 30 | compare refused before attribution → full pairing
b7768721 | batch-digest | 87 | waited on base re-record 42.4 · compare 29.7 CLEAN · gates -n4 12.8 | 0 | —
e125fff8 | landing-decisions | 127 | compare 32.5 · ship-gate 5 hard-fails (selection gap) · repair · re-compare 28.5 · gates 9 | ~32 | compare pass 1 superseded
3689b5ab | merge-gates-truth | 271 | compare LANE-RED 39 · ship-gate on doomed tree 7 · repair-1 self-verify ~9 (discarded) · repair-2 compare 38.8 · gates -n4 16.6 | ~55 | two verification passes discarded
WAVE4 dup total: ~85 narrow / ~195 broad (broad counts every discarded run)

WAVE4B (5 merged; wall 2fd8f256 19:46Z (22nd) → 3d3b3a0e 17:23Z (23rd) = 21h38m; batch NOT closed; 7h20m ruling wait on handback-organ)
merge | lane | pickup→push | steps (min) | dup min | what repeated
2fd8f256 | hooks-rearm | 77 | shared base record reaped at 42 → restarted 84 · gates -n2 16 · compare 30 | 42 | reaped base record (batch-shared)
3f535db5→de97dad5 | handback-organ | 55 refused + 93 repair | gates 14 · ship-gate diff 9 · compare 51 (after cause known) · repair: self-check + gates 17 + compare 59 | ~60 | compare ran after refusal was decided; ship-gate run by repair AND integrator on same tree
e8ec23fc | plan-lint | 90 | ship-gate pair 10 · gates -n2 16 · compare -n2 55 (serial, memory cap) | 0 | —
10a4c9f5 | fleet-health-split | 207 | compare → UNATTRIBUTABLE (unregistered test_fleet_health.py) · two-commit pairing 170 | 115–170 | pairing re-ran the already-recorded base; ≥115 is excess over a normal ~55 compare
3d3b3a0e | gate-verdicts | 189 | two-commit pairing killed at 76 (ruling) · split verify 64 | 76 | killed pairing fully discarded
WAVE4B dup total: ~293–348 min (≈ 60–70 min per merge on average)
```

The logs record the "split verification" ruling saving ~1h46m per lane (~2h50m pairing vs 1h04m split).

**Latent hazard (measured, not yet biting):** each merge commit folds a row into `logs/MERGE-RECEIPTS.jsonl`, and no `impacted_tests.RULES` entry claims that path. Replaying `select --ref <merge>^1` on each wave-4b merge returns `# FULL SUITE`, which `gates.py::impacted_tests_gate` (L124-136) turns into a RED refusal. The logged gate runs narrowed normally, so the row was evidently written after the gates ran. Any flow that stages the row first will red the gate.

## Selection, wave-4b (replay on today's tree, receipt file excluded)

```
merge | selected files | self (changed tests) | via lane's own scripts/*.py | via prose only (live_repo union)
2fd8f256 hooks-rearm | 59 | 1 | 0 | 58
de97dad5 handback-organ | 70 | 3 | 17 | 53
e8ec23fc plan-lint | 59 | 1 | 1 | 58
10a4c9f5 fleet-health-split | 118 | 3 | 88 (scripts/audit.py imported broadly) | 29
3d3b3a0e gate-verdicts | 61 | 3 | 3 | 58   (matches the log's own "61 selected")
```

The mechanism is `select()` L522 `if marker and selected:`, which unions the entire `live_repo_test_files()` set (58 files) when any doc changes and anything else is selected. So one line of `doc-counts.md` costs the same as 15 files of prose.

## Top slow tests — STALE, shape only

No timing exists on today's 7,343-test corpus (`.pytest_cache` has only `lastfailed`/`nodeids`; no junit, no receipts carry per-test seconds). The newest per-test data is R1 (`docs/audits/2026-08-14-technical-night2-latency.md`, 2,897 tests, `-n 0`) and R3 (`2026-08-27-technical-lane-nb-tiering-durations.md`, 3,988 tests, contended `-n auto`). No targeted run was made because timing data existed. The prescribed fresh-measure command is in `2026-08-29-technical-nb2-slow-marker-evidence.md` §6a and was never executed.

```
test (R1 seconds unless noted) | spawns
test_safe_remove::test_real_oracle_blocks_real_cross_module_removal 268.7 (38% of run) | real oracle subprocess (pyright-langserver)
test_reverse_dep_oracle::test_finding_headline_resolves_with_provenance 65.6 | pyright-langserver subprocess
test_reverse_dep_oracle::test_main_finding_json_exit_zero 65.5 | pyright-langserver
test_legibility_graph_conformance::{oracles_registered, cell_code_code} 20.8 / 20.4 | pyright-langserver
test_safe_remove::test_real_oracle_allows_orphan_removal 20.7 | oracle subprocess
test_normalize_headers corpus_* (4) 17.7/9.0/8.7/8.6; test_toc corpus 17.5 | whole-hub scan
test_writer_integrity 12.0; test_hub_identity 11.7; test_audit health_* (3) ~10 | live repo / ALL_CHECKS
test_membership_agreement::declaration_leg 7.6 (R3 676 contended) | package-mode subprocess
R3: review_artifact_coverage live_repo 459 · session_end_backpressure e2e 112.6 · adr85 t3_pre_push 91.8 | live sweep / hook subprocesses

top modules (R1): safe_remove 289.7s · reverse_dep_oracle 151.8 · normalize_headers 44.0 · legibility_graph_conformance 41.2 · audit 32.5 (202 tests, live repo) · toc 18.0 · doc_code_edge 13.7 · writer_integrity 12.0 · hub_identity 11.7 · (static-only candidate: deploy_floor, 185 pre-commit refs, never timed)
```

- **Shape (R1, confirmed by R3):** the top 10 files (14%) carried 89% of cost.
- **What drives the cost:** pyright-langserver oracles and live-repo audit sweeps, not synthetic git repos. Only 4 test files build tmp repos, and no test uses the network.

## CI facts and parity

```
workflow | jobs | pytest invocation | gating?
conductor.yml | pytest, ruff, seal, commit-gate, terra (not run: no secret), phase-gate | uv run --locked pytest -q -n 4, full suite, judged by conductor.py suite-gate vs logs/SUITE-BASELINE-FREEZE.md (87 frozen reds, c5108329, 2026-09-17) | NO: ruleset deploy/conductor-required-checks.ruleset.json enforcement: disabled; merges are local --no-ff, so PR triggers never fire
report-only-wall.yml | record (+ gated mutation-pilot) | pytest -q (default addopts), all steps continue-on-error | never; "success" = record written (pytest leg exit 1 on newest runs)
no shards, no matrix; single ubuntu job
```

**conductor, last 20 runs:**
- **Wall time:** min 4m12s, median ~8m20s, max 9m07s. The `pytest` job is the long pole at ~8 min (241–532 s).
- **Verdicts:** 20/20 failure. `pytest` failed 20/20: 88–96 failures, of which 14–24 are REGRESSION outside the freeze. 4 of those are the deliberate `[#664]` witnesses; the rest is drift in a recurring set (`test_bounded_hook`, `test_graph_spine*`, `test_integrator_surface`). `commit-gate` failed 18/20 because it runs every manual-stage hook over the whole tree. `ruff`, `seal` and `phase-gate` passed 20/20.

```
parity (same SHAs)
sha | CI conductor | local gate record | agree?
3d3b3a0e | FAIL (16 regressions) | CLEAN, lane tests 21/21 | no
10a4c9f5 | FAIL (17) | CLEAN | no
de97dad5 | FAIL (17) | CLEAN post-repair | no
e8ec23fc | FAIL (17) | CLEAN | no
2fd8f256 | FAIL (17) | CLEAN | no
3689b5ab | FAIL (18) | CLEAN | no
```

- **The two gates answer different questions.** Local asks "no new red vs the lane's parent"; CI asks "anything red outside a stale freeze". Both are true, and the regression count creeps 12→17 while every lane reports 0 new.
- **`lane-verify-in-lane` parity record:** `docs/audits/2026-09-22-technical-lane-verify-in-lane-merge-queue-measurement.md` (+ the `-codex-…-terra` and `-disposition` audits) exists ONLY on the local, unpushed branch `worktree-integrate-lane-verify-in-lane` (tip b32b85df, 19:31+02:00). It is on neither main nor origin/main, and [#960] is still open.
- **What that record found:** the same result on 10 pushes, "CI 10/10 failure vs local 10/10 mergeable — different questions, both true". It recommends against arming required checks until the freeze is refreshed and commit-gate is diff-scoped. This digest corroborates that independently.

## Memory

```
time (Z) | seats | free GB (of 27.7) | -n | forced by
09-22 02:50 | 4 lanes | 4.2 | -n 2 | reaper killed pairing + poll
09-22 04:56-05:28 | 0-1 | 3.0-6.2 | -n 2 | manual PYTEST_ADDOPTS
09-22 07:19-15:58 (wave4 day) | ≤2 lanes | — | -n 4 | manual (more headroom)
09-22 17:03-17:47 | wave4b start | 5.1→4.2 | -n 2 | reaper killed 42-min base record
09-22 21:54 | 4 (merge_receipt concurrent_seats) | — | -n 2 | manual, "because lanes run concurrently"
09-22 22:00-09-23 06:47 | — | 4.0-4.3 | — | 8 further poll reaps
09-23 ~07:20 | — | — | — | OOM stopped lane-verify-in-lane + lane-gate-verdicts; operator cap ≤2 heavy sessions, 3 GB launch floor
09-23 10:12 | 2 heavy | 2.78 | — | launch freeze (<3 GB)
```

No script chooses `-n` (`resource_lifecycle.py:12`: "Nothing in the tree reads free memory before a dispatch"). `-n auto` OOM-killed 5 full-suite attempts on 09-07/08 (pyproject.toml:266-288), and that is why `-n 2` is the hand standard.

## Built but not in the merge path

```
tool | where | used at merge? | why not
lane-side record reuse / select-lane (#960) | branch worktree-integrate-lane-verify-in-lane (b32b85df) | no | unmerged: OOM-stopped 09-23, repair in flight; integrator still re-runs compare every merge
impacted-test selection | scripts/impacted_tests.py → gates.py impacted_tests_gate | per-lane gate only | refuses on FULL SUITE ("CI owns that run"); integration still runs test_pairing compare over a prose-inflated set
CI full suite (8 min, -n 4) | .github/workflows/conductor.yml | no | ruleset enforcement: disabled; local --no-ff merge never makes a PR; suite-gate baseline 6 days stale → permanent red, so no one reads it
memory-derived -n | absent | — | recorded gap QR-RES-001; -n hand-set per run
xdist safety settings | pyproject addopts -n auto (interactive); -n 2 + --timeout=900 for unattended suite | partially | gates.py _run_pytest passes no --timeout / worker bound; relies on PYTEST_ADDOPTS
pytest-timeout | dep, used only in the scripted unattended-suite line | no (gates/compare) | interactive path deliberately unchanged
--lf / --ff / testmon | absent | — | never configured, no recorded intent
mutation testing (mutmut) | pyproject, only_mutate *fleet_analytics.py; CI mutation-pilot job | no | a one-file pilot with its own false-green history; not in GATES or ship-gate
```

## Changes, ranked by minutes saved per merge

Savings overlap: #1+#2 overlap with #3, so don't add them.

1. **Retire the local `compare`/pairing leg in favour of CI's full suite: ~45–55 min per merge, plus the whole fallback tail.**
   - Basis: `compare` is 30–59 min at `-n 2` (logged, 9 merges), while CI runs all 7,343 tests in ~8 min (20 runs), and the machine's memory forces `-n 2`.
   - Prerequisite: refresh `SUITE-BASELINE-FREEZE.md` (87 frozen at c5108329 → the current drifting set) so CI's verdict is readable, then have the integrator gate on the CI run for the merge SHA, or push a pre-merge ref and wait ~9 min.
   - The unpushed `lane-verify-in-lane` record reaches the same prerequisite.
2. **Make split verification the default and never fall back to two-commit pairing: ~100–170 min on each merge that hits the fallback (3 of 10 across both waves), ~35 min averaged per merge.**
   - Basis: fleet-health-split 170, gate-verdicts 76 discarded, connection-hygiene 30+63.
   - The ruling already proved the method: 64 min split vs ~170 for pairing.
   - Also register new test files at lane handback, so `compare` is never UNATTRIBUTABLE.
3. **Stop the prose-triggered `live_repo` union at merge time and run the 58 `live_repo` files once per batch (Tier B), not per merge: est. 25–40 min per merge.**
   - Basis: 256/276 wave-4b slots (93%) are prose or self; lane code reaches 0–3 files on 4/5 merges; R1/R3 put the slow poles in `live_repo`-style tests.
   - Estimate, not measured: time is not proportional to file count.
4. **Land [#960] (reuse the lane's test record by tree SHA): est. 20–40 min per merge.**
   - Basis: the integrator re-ran the lane's already-green tests in every `compare` (e.g. gate-verdicts' 21 lane tests), and the branch exists with 106 passing at `-n 2` and its 3 Codex HIGH findings fixed.
   - Partly overlaps #1 and #3.
5. **Kill repeat gate runs on one tree, and derive `-n` from free memory: ~10–20 min per merge.**
   - Basis: ship-gate run by both the repair and the integrator (~9 min); impacted-tests re-run after pairing (8 min); the reaped 42-min base record; `-n 4` gates took ~13 min vs `-n 2` ~16 min.
   - Map `logs/MERGE-RECEIPTS.jsonl` in `impacted_tests.RULES` before it turns every gate into a FULL-SUITE refusal.

Where evidence stops:
- Durations come from session-log prose and git times; the receipt JSONL and the out-of-repo sampler ledger were not read.
- Selection counts are replayed on today's tree.
- Test seconds are ≤2026-08-27 data on a corpus ~half today's size.
- Wave 4b is not closed (`lane-verify-in-lane` is pending; `lane-merge-path` is deferred).

DONE 2026-09-23T18:30Z (20:30+02:00)
