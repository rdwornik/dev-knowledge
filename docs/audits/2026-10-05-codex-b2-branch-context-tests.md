# Codex Review — b2-branch-context-tests

**Date:** 2026-10-05
**Branch:** `worktree-b2-branch-context-tests`
**HEAD:** `88968da9`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low, counted by hand from the Findings section: three HIGH findings, each a P1 and each fixed in 9c6a85dd. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** [#1101] LANE-B2-W1-b2-branch-context-tests

## R59 proof of read (lane b2-branch-context-tests, 2026-10-05)

- **Contract:** `LANE-B2-W1-b2-branch-context-tests` (batch B2-W1, lane W1-8), Done-contract item 4;
  related rows `[#1101]`, `[#912]`, `[#590]`.
- **Served model id, from the tool's own log:** `model: gpt-5.6-terra` (the `codex exec` run header:
  `OpenAI Codex v0.155.0`, provider openai, sandbox read-only, reasoning effort high, session
  `01a10bc1-2594-7460-8648-8aa1ed637a35`). The reviewer's own one-line self-report said `gpt-5`; the run
  header is the record.
- **Content hash returned by the reviewer:** `tests/branch_context.py`
  `sha256=06b50ace81bf69c80f575401a92cbbc2294bd3944ee325427bebb330b4c36b73`. Recomputed by the lane with
  `Get-FileHash` at the reviewed HEAD before the run
  (`06b50ace81bf69c80f575401a92cbbc2294bd3944ee325427bebb330b4c36b73`): equal, so the read was real.
- **Reviewed HEAD:** `88968da9`.
- **Route:** `codex exec --sandbox read-only -c model=gpt-5.6-terra -c model_reasoning_effort=high` run
  directly (not through `deploy/codex-review.ps1`) so the run header was captured to a file; the prompt
  asked for the content hash and a model-id line as the first two lines of the answer.

## Disposition (added by the lane after the review, same day)

All three HIGH findings are P1 and are fixed in `9c6a85dd`; each has a test.

1. `tests/branch_context.py` `names_at_merge_base` scoped against `origin/main` alone, so a checkout on `main`
   ahead of a stale tracking ref treated its own recent commits as "the lane's" -- fixed:
   `merge_base_with_main` takes the LATER of the merge bases with local `main` and `origin/main` (None when
   neither contains the other, which every caller reads as "judge strictly"); tests
   `test_a_main_ahead_of_a_stale_origin_is_judged_on_everything_it_carries`,
   `test_a_lane_that_adds_an_audit_leaves_it_out_of_what_it_inherited`,
   `test_the_merge_base_is_unknown_when_there_is_no_main_to_compare_with` (in `tests/test_gen_audit_index.py`).
2. `tests/test_check_derived_copies.py` `_inherited_root` had the same fault -- fixed by using the same
   helper, so on `main` HEAD the live tree is judged.
3. `pin_journal_spine` replaced a whole organ (`audit.check_journal_spine_anchor`) with an unconditional
   pass -- fixed: it now replaces only the result of `journal_anchor.unanchored_on_spine`, the one input that
   depends on the branch; the preflight row and the `ship_gate` organ run for real; test
   `test_the_journal_pin_replaces_the_spine_list_and_leaves_both_organs_real`
   (in `tests/test_handoff_cut_acceptance.py`).

The reviewer's closing line -- every witness node id resolves to a named test, and it found no new skip,
xfail, deselect or branch-name conditional -- is recorded as read.

---

## Focus

Contract: LANE-B2-W1-b2-branch-context-tests (no test's verdict depends on running on a lane or integration
branch instead of `main`). Attack: tests/branch_context.py (clone fixture, `witness`, `names_at_merge_base`,
`pin_journal_spine`), the merge-base scoping in test_gen_audit_index / test_consumer_at_landing /
test_check_derived_copies, the journal pin in test_handoff_cut_acceptance / test_seat_release_moment, and the
fixtures in test_worktree_seed / test_provision_legs. Questions: can a witness pass vacuously; does a scoped
check still fail on `main` for a stale index row, an unconsumed record or a stale derived copy; is the journal
pin honest; any weakened assertion, added skip/xfail/deselect, or branch-name condition.

---

## Findings
CONTENT-HASH tests/branch_context.py sha256=06b50ace81bf69c80f575401a92cbbc2294bd3944ee325427bebb330b4c36b73
MODEL-ID gpt-5

## Critical

(none)

## High

**HIGH — tests/branch_context.py:147 — `origin/main` can make main-scoped checks silently non-strict.**

**What:** `names_at_merge_base()` scopes against the remote-tracking ref, so a local checkout on `main` whose `origin/main` is behind `HEAD` treats recent main commits as lane additions.
**Why:** A stale index row or unconsumed audit introduced after the last fetch can pass in `test_gen_audit_index` and `test_consumer_at_landing`, while the original strict check would fail.
**Fix direction:** Establish strictness from the checked-out `main` identity, or explicitly refuse/fall back to strict checking when `HEAD` is on `main` but differs from `origin/main`.

**HIGH — tests/test_check_derived_copies.py:175 — stale derived copies can be hidden on an unfetched `main`.**

**What:** `_inherited_root()` clones the merge base whenever `origin/main` lags local `main`, including while currently on `main`.
**Why:** A stale derived copy in commits after the stale tracking ref is not inspected at all, so this test can pass where its former current-tree assertion fails.
**Fix direction:** Use the live tree whenever `HEAD` is `main`; reserve merge-base cloning for a confirmed non-main lane shape.

**HIGH — tests/branch_context.py:187 — `pin_journal_spine` replaces an entire handoff organ, not just its live JOURNAL input.**

**What:** The helper monkeypatches `audit.check_journal_spine_anchor` to an unconditional pass; preserving its `__name__` only preserves the organ-set spy's name check.
**Why:** The dry-cut tests no longer exercise that organ's invocation or failure behavior, contrary to the stated "only inputs" pinning contract.
**Fix direction:** Patch the journal/spine data dependency beneath `check_journal_spine_anchor` to a clean deterministic fixture while retaining the real organ function.

## Medium

(none)

## Low

(none)

All witness nodeids resolve to named tests, and pytest would fail on zero collection; I found no new skip, xfail, deselect, or branch-name conditional.
