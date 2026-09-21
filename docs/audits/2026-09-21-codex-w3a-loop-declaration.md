# Codex Review — w3a-loop-declaration

**Date:** 2026-09-21
**Branch:** `worktree-lane-loop-declaration`
**HEAD:** `3a151660` (reviewed commit; the dispositions below land in the next commit)
**Diff range:** `main..worktree-lane-loop-declaration`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- ecosystem/harness.yaml: the six moments (pre-launch, lane-start, merge, teardown, lane-end, batch-close). Does pre-launch hold exactly the three organs the launcher needs, and does lane-start keep only in-lane organs? Is the merge review row (--merge {merge}) correct against scripts/review_packet.py (exclusive --range/--merge)? Is the declared go_reader CLI (--batch {batch}) a sound contract for a script that does not exist yet?
- scripts/dodo.py: the new moment precondition (SKIPPED-PRECONDITION receipt, no organ runs), per-organ continue_on_failure plus the moment verdict (a continued failure must be recorded, must not stop later organs, and must not be swallowed), and the {merge} / {session_file} substitutions. Stale-receipt hazards: can an old failed receipt or an old ok precondition receipt make a later run wrong?
- The fates block: 36 recorded fates. Any that is false against the code, or any organ dropped from the roster. Nothing may be retired, disarmed or narrowed.
- tests/test_loop_declaration.py: any test that cannot fail (vacuous), any test that would write the operator's live transport, GO file or a remote, and any race with the primary checkout's .claude/worktrees.

---

## Findings
## CRITICAL

(none)

## HIGH

### ecosystem/harness.yaml:75 — Batch digest reads only one receipt directory as one lane

**What:** `batch-close` invokes `lane_digest.py --lane {batch} --receipts-dir {receipts}`, but batch mode in `lane_digest.py` is `--root`; this renders a single lane labelled with the batch name.
**Why:** The digest can omit the actual lanes’ receipts and report a misleading batch outcome.
**Fix direction:** Pass a batch-root containing per-lane receipts, or add a batch-aware input contract and a multi-lane assertion.

### scripts/dodo.py:269 — Missing batch input silently bypasses future GO validation

**What:** Once `scripts/go_reader.py` exists, its `optional: true` row treats an unset `{batch}` as `SKIPPED-NO-INPUT` and succeeds.
**Why:** A merge can proceed without checking for the required GO file.
**Fix direction:** Limit optionality to the unbuilt command case, and make `batch` a refusal once `go_reader` is available.

### tests/test_loop_declaration.py:162 — Test mutates the primary checkout’s worktree directory

**What:** The occupied-slug test creates and removes `<primary>/.claude/worktrees/<slug>`.
**Why:** It races with real launcher/worktree activity and transiently changes the operator’s live worktree surface.
**Fix direction:** Exercise occupancy against an isolated fixture repository or injected root, without touching the primary checkout.

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (W3-A, recorded before handback)

| # | Finding | Disposition | Evidence |
|---|---|---|---|
| 1 | HIGH `harness.yaml:75` -- the batch digest reads one receipts dir as one lane | **ACCEPTED as a known limit, ESCALATED** (a fork with no standing ruling). The row is the contract's own (`lane_digest` moves to `batch-close`, R-W3-3). A batch-root digest needs per-lane receipts, and teardown removes them with the worktree, so the real input surface (the transport's `LANE-END-<lane>.md` reports, or a retained receipts root) is a design choice and not a declaration edit. The row names the batch (`--lane {batch}`) and reads the integrator's receipts dir; W3-F's run shows what it can honestly report. | `to-browser/QUESTION-lane-loop-declaration.md`; `tests/test_loop_declaration.py::test_a_failing_report_does_not_stop_the_digest` runs the declared row for real |
| 2 | HIGH `dodo.py:269` -- an unset `{batch}` skips a built `go_reader` | **ACTIONED.** New row key `strict_inputs: true` narrows `optional` to "not built yet"; `go_reader` carries it, so once W3-C builds the script an unset batch STOPs the moment. | `tests/test_loop_declaration.py::test_go_reader_cannot_be_bypassed_by_omitting_the_batch` (red when either the dodo condition or the row flag is reverted) |
| 3 | HIGH `test_loop_declaration.py:162` -- the occupied-slug test mutates the primary checkout's `.claude/worktrees` | **ACTIONED.** The test builds a throwaway primary checkout and points the git common dir at it through `GIT_DIR`; the declared row runs unmodified and the operator's real worktree surface is never read or written. | `_fixture_primary` in `tests/test_loop_declaration.py`; `test_pre_launch_refuses_an_occupied_fixture_slug` (red when the occupancy row's slug is changed) |

The wrapper's own severity heuristic printed `0/0/0/0` (it counts heading words, not findings); the tally
above is from the Findings section: 0 critical, 3 high, 0 medium, 0 low.