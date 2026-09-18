# Batch AC — close packet · 2026-09-18

**BATCH AC IS OPEN, PENDING THE FULL SUITE ON `78d7e98f` -- read this before the text below** (marker inserted 2026-09-18 as a pure insertion; nothing below it was edited). This packet, as first landed, asserted that batch AC closes. That is NOT TRUE: the integrator ran only targeted and paired gates (M5, M6, R2), and the ADR-110 refuse-to-finish item "full suite run once on the merged result" was never run. Ruling `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md` §1: the batch stays OPEN until the full suite runs on `78d7e98f` with `-n 6`; a green run closes it with the run as its witness, and any failure is pair-measured against the baseline -- a failure that does not reproduce there is a REGRESSION and keeps the batch open until named and ruled. The result is recorded in a further marker below this one. Where the text below says the batch "closes", read "is OPEN".

**C3 RESULT: BATCH AC IS CLOSED -- the full suite ran on `78d7e98f`, and every failure reproduces at baseline** (marker inserted 2026-09-18 as a pure insertion; nothing below it was edited; this discharges the OPEN marker above). **Run:** `uv run --locked pytest tests/ -n 6` in a detached throwaway worktree at `78d7e98f`, seeded with the primary's six `ecosystem/*/state.yaml` and `.claude/settings.local.json` -- **75 failed, 6,388 passed, 26 skipped, 2 xfailed** in 2,650 s. Not green, so each failure was pair-measured against the batch base `87638c8d`. **Pair 1 (xdist):** the 36 test files holding the 75 failures, `-n 6`, same worktree, adjacent in time -- tip 74 failed / 1,716 passed, baseline 74 failed / 1,716 passed, **failing-test ids IDENTICAL**. **Pair 2 (deterministic), for the one full-suite failure the file-level run did not reproduce on either side** -- `test_manifest_link_route.py::test_the_class_enum_is_the_hermetization_module_s_own_object`, the documented xdist-only identity RED (`batch_manifest.AUDIT_CLASS_ENUM is vh.AUDIT_CLASS_ENUM` fails while the two frozensets are equal; `tests/test_seal_repo_profile.py` swaps the module object): `-n 0` alone PASSES and `-n 0` after `tests/test_seal_repo_profile.py` FAILS, at BOTH `78d7e98f` and `87638c8d`. Batch AC's diff touches none of `validate_hermetization.py`, `batch_manifest.py` or either test file. **Regressions: 0.** Per-file failures at tip: test_prompts_guard_hook_wiring.py 20 · test_release_lint.py 5 · test_normalize_headers.py 4 · test_graph_spine_commit_tier.py 4 · test_gen_handoff.py 4 · test_audit.py 3 · test_validate_adr_status.py 2 · test_logs_retention.py 2 · test_decision_coverage.py 2 · test_canonical_docs.py 2 · test_archive_row_body.py 2 · test_worktree_seed.py 1 · test_validate_doc_rot.py 1 · test_v6_frozen_contract.py 1 · test_toc.py 1 · test_stale_worktrees.py 1 · test_routing_agreement.py 1 · test_reverse_dep_oracle.py 1 · test_proof_layer.py 1 · test_preflight_freeze_predicates.py 1 · test_manifest_link_route.py 1 · test_lived_sandbox_observer.py 1 · test_handoff_modes.py 1 · test_graph_spine.py 1 · test_generator_newlines.py 1 · test_gen_task_tree.py 1 · test_funnel_coverage.py 1 · test_floor_mechanisms.py 1 · test_export_backlog_view.py 1 · test_enforcement_coverage.py 1 · test_doc_code_edge.py 1 · test_desired_state_schema.py 1 · test_desired_state_loader.py 1 · test_consumer_at_landing.py 1 · test_conductor.py 1 · test_check_derived_copies.py 1. The 75 are pre-existing debt the batch did not create and did not reduce; closing the batch does not make them green.

**§5 COST IS SUPERSEDED: USD 30.59, RE-DERIVED -- read this before §5 below** (marker inserted 2026-09-18 as a pure insertion; §5 is left as landed, so the record keeps the error). §5 says cost is UNAVAILABLE because "no cost telemetry exists". That premise was ruled without a check and is FALSE ([#893]; `to-cc/DECLARE-BATCH-AC-NOT-CLOSED-2026-09-18.md` §2). **Method:** the integrator ran `uv run --locked python scripts/lane_cost.py lane --slug <slug> --batch AC` from the primary checkout, 2026-09-18, for all seven AC sessions (rates as_of 2026-06-24). **Per lane (USD):** ac-night-freeze 15.06 (124 calls) · lane-ac-589 5.07 (94) · lane-ac-741 4.41 (69) · lane-ac-863 2.56 (58) · lane-ac-661 1.92 (42) · lane-ac-694 1.37 (21) · lane-ac-285 0.20 (4). **Per model:** claude-opus-5 **15.06** (the freeze seat only), claude-sonnet-5 **15.53** (all six lanes). **Total USD 30.59** -- matching [#893]'s figure, now independently re-derived. Honest limits: the rate card is stamped 2026-06-24; ac-741 and ac-694 were resumed background sessions, and a transcript filed under a launching session is a lower bound; seat sessions (architect, primary, dispatcher, integrator) are NOT in this figure -- that is [#907].

> The `closed_by` artifact named in `docs/audits/2026-09-17-technical-batch-ac-manifest.md`.
> Written by the integrator seat (Opus 5, session `c334b928`) under the operator's three close
> decisions of 2026-09-18 and `to-cc/DECLARE-BATCH-AC-CLOSE-2026-09-18.md` +
> `DECLARE-BATCH-AC-CLOSE-AMENDED-2026-09-18.md`. Every figure names its instrument; a figure with
> no instrument is marked UNAVAILABLE or UNMEASURED rather than estimated.

## 1. Merged SHAs (main first-parent, batch base `87638c8d`)

| # | Branch @ tip | Merge | What |
|---|---|---|---|
| M1 | `worktree-lane-ac-741-dispatch-surface` @ `7b599303` | `a86354f7` | dispatch-surface measurement for [#741], 5 audits |
| M2 | `worktree-lane-ac-661-evals` @ `4f7d3aa0` | `f2f81ecd` | SDA-1 evals [#661]: cannot run, reason named |
| M3 | `worktree-lane-ac-694-insurance-census` @ `9bbb4d89` | `5d7d847f` | insurance census; merged under R4 despite the dispatch-shape deviation ([#898]) |
| M4 | `worktree-lane-ac-589-backlog-closures` @ `367d1391` | `9d1e4638` | files [#889], [#890]; closes nothing |
| M5 | `worktree-lane-ac-863-notification` @ `fb50bbeb` | `939e49ed` | `expiry` beside each disabled hook |
| P1 | `worktree-handback-contract-row` @ `e0de14a9` | `bb710468` | [#891] handback contract -- merged by a SECOND session on the primary (see §8) |
| M6 | `worktree-ac-night-freeze` @ `7f15218b` | `ab5f6245` | the batch freeze: manifest, contracts, organs intake |
| -- | `docs/batch-ac-integration` @ `47db8b9a` | `4601b70f` | R3 undone, [#901], audits index |
| -- | `worktree-ac-amended-rows` @ `e570dbb7` | `0936c18d` | [#902]-[#904] |
| -- | `worktree-ac-close-followups` @ `7fce90c0` | `dd1cb4f0` | R2 Stop-hook exemption, two censuses, [#892]-[#900] |
| -- | `docs/batch-ac-close` | the merge that lands this file | [#906], this packet, the JOURNAL correction |

**Not merged:** `lane-ac-285-config-headers` -- 0 commits, WEDGED, torn down (R5, [#894]). Lane
`ac-582` (L6) was contracted CONDITIONAL and correctly NOT booted: L1 reported the dispatch verb
outside this repo. The R3 rescue branch `feat/790-runtime-resource-recovered` was pushed and then
deleted on the operator's reversal; `01c446f7` stays off every ref, as ruled.

**Gates on the measured merges.** M5: `pytest tests/ -k "settings or hook" -n 4`, paired, 27F/212P
both sides, identical failing-test ids. M6: `pytest tests/ -m live_repo -n 4`, paired in a
throwaway worktree seeded like the freeze worktree -- baseline `87638c8d` 34F/127P, candidate
`7f15218b` 34F/127P, failing-test lists identical with multiplicity (34 lines, 30 distinct ids);
the first candidate run was killed by Claude Code for critically low memory and rerun on order.
R2: `tests/test_session_end_backpressure.py` 49 passed on main `0936c18d`, 55 passed on the merge.

## 2. Rows filed vs closed

**Filed 17, closed 0.** Instrument: `status:` of `tasks/*.md` at `87638c8d` vs the close branch.
Filed: [#889] [#890] [#891] [#892] [#893] [#894] [#895] [#896] [#897] [#898] [#899] [#900] [#901]
[#902] [#903] [#904] [#906]. Reservation [#905] is held on origin by `ac-amended-rows` and UNUSED:
it duplicated [#901] and was dropped before merge. M4 closes nothing -- the 25 closures the night
order named had been executed by lane ab-828 before batch AC ran.

## 3. BACKLOG size

Instrument: `wc -c BACKLOG.md`, `grep -c '^- \[#' BACKLOG.md`, `status: open` over `tasks/*.md`.

| | bytes | `- [#` lines | open task files |
|---|---|---|---|
| batch base `87638c8d` | 76,256 | 368 | -- |
| close (`docs/batch-ac-close`) | **79,870** | **385** | **333** |

Against the [#589] bar of 72,000 B: **7,870 B over**; it was already 4,256 B over at base.
Row age (`docs/audits/2026-09-18-census-row-age-full-coverage.md`, n=316 open at base): median
age 17 d, 111 rows filed in the last 7 d. **Oldest bucket: 91-180 d, 7 rows.** One
ABANDONMENT-CANDIDATE ([#342]) and 29 WATCH rows -- PROPOSE ONLY. The census REFUTES "the backlog
is an age problem": the measured pressure is inflow.

## 4. Merge minutes

Instrument: committer timestamps of consecutive integrator merges in the serial walk M1->M5, one
sitting, 2026-09-18 UTC 10:35:57 -> 10:56:43.

- M1->M2 2.27 · M2->M3 1.42 · M3->M4 1.37 · M4->M5 15.72 (includes M5's two paired ~6-min runs)
- **Median 1.85 min, n=4.** M6 is excluded: 81.2 min M5->M6 was a memory-killed run plus an
  operator re-order -- gate latency, not merge work.

## 5. Cost per lane and per model -- UNAVAILABLE

**UNAVAILABLE.** Reason, per the operator's close decision: no cost telemetry exists, so no
figure here has an instrument this packet can stand on. The gap is recorded, not estimated.

**Anti-claim carried, not adopted:** the primary session reported that `lane_cost.py` (run with
`--repo-root` at the primary, `lane --slug SLUG --batch AC`) prices every AC lane today at
USD 30.59 in total -- night-freeze 15.06 on opus-5 · 589 5.07 · 741 4.41 · 863 2.56 · 661 1.92 ·
694 1.37 · 285 0.20, rates as_of 2026-06-24. That is the claim [#893] is filed on. The integrator
did not re-derive it. If [#893] holds, "no cost telemetry exists" is false and this line is
recoverable; settling that is [#893]'s job, not this packet's.

## 6. The acceptance test ([#889]) -- GREEN-WITH-A-NEARLY-EMPTY-ARMED-SET

**Recorded as GREEN-WITH-A-NEARLY-EMPTY-ARMED-SET, per the operator. It is NOT a pass.**

- **Armed set: 4 of 36 guards fire locally**, verified from `.pre-commit-config.yaml` at close:
  `audit-index-freshness`, `organ-index-freshness` (pre-commit), `block-ff-push`,
  `block-unanchored-push` (pre-push). The other 32 are `stages: [manual]`, reachable only
  through a disabled conductor ruleset. None of the four checks the correctness of a commit.
- **Dispatch -> commit** (consolidated handback; dispatch = each lane's first transcript
  message, a proxy): median **39.0 min, n=6**; 38.2 min, n=4 excluding the two overnight
  outliers; 4 of 6 inside one hour.
- **Dispatch -> MERGED -- the Done-when's own wording, measured here** (same dispatch proxy; merge
  = the merge commit's committer time): freeze 898.8 · 589 749.5 · 863 765.6 · 661 746.0 ·
  741 746.2 · 694 736.5 min. **Median 747.9 min (12.5 h), n=6; 0 of 6 inside one hour.** The
  lanes were fast; integration waited overnight for authorisation. Against [#889]'s verbatim
  Done-when ("dispatch to merged, in under one hour") no lane met the bar.

## 7. Organ usage beside throughput (AX9-5)

Instrument: `docs/audits/2026-09-18-census-ax9-5-organ-use-rerun.md`, 14 d to 2026-09-18.
**Median 0.67 raw searches per organ invocation, per session**; 2,230 raw vs 2,759 strict organ
invocations; **36 of 215 sessions (17 %) invoked no organ.** The guard's declared escape held on
a single segment and is still defeated by a pipe. Uncalled in the window: 7 git-hook entry points
whose gate is `stages: [manual]` and 10 directly invocable scripts, named in that audit. The
browser seat carries no telemetry and is absent from the count.

## 8. The collision this close produced

A second session merged P1 (`bb710468`) on the primary between M5 and M6. Both sessions allocated
JOURNAL letter (f), and the integrator's (g) listed [#891] as still waiting after it had landed.
CAUSE: two sessions committed on the same primary checkout concurrently. Filed as [#906] -- the
primary has ONE writer at a time, and during a batch close the integrator holds it; a mechanism,
not an etiquette request. Corrected by an appended JOURNAL entry, never an edit.

## 9. Teardown

`git worktree list` == primary only; `git stash list` empty; no AC lane, freeze, handback, rows
or follow-ups branch remains locally or on origin. The R2 Stop-hook exemption ships **without a
counter** (JOURNAL 2026-09-18 (i)); under the standing rule it is removed at its next review
unless one is added.
