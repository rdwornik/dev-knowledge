# Codex Review — foundation-4-merge-gate

**Date:** 2026-10-04
**Branch:** `worktree-foundation-4-merge-gate`
**HEAD at review time:** `80d31774`
**Diff range:** `origin/main...80d31774` (24 files)
**Codex version:** n/a — SUBSTITUTED under batch common rule (e) (see Substitution note)
**Mode:** diff-review, isolated read-only session (contract + diff + changed files only; `--tools read_file,list_dir,grep`)
**Tally:** P1=1 (claimed; not reproduced) P2=2 P3=3
**Consumer:** `LANE-FOUNDATION-foundation-4-merge-gate.md` (item 16, "the review record");
`docs/decisions/ADR-127-ci-os-verification.md`; `[#966]`

**Model used:** `grok-4.7` (SUBSTITUTE for the pinned `gpt-5.6-terra`; served id read from the session's `usage.json` `primaryModelId` = `grok-4.7`)
**Review profile:** code

---

## Substitution note

`SUBSTITUTION: codex terra -> grok-4.7 (codex exec: "You've hit your usage limit ... try again at 2:25 AM", 2026-10-04 ~01:40).`

The Codex run was tried first, as the batch rule says after 2026-10-03 21:07: `deploy/codex-review.ps1 -Topic
foundation-4-merge-gate` built the prompt and sent the diff, and `codex exec` exited 1 with the limit message above.
The substitute is the batch order's own: an isolated, read-only `grok -m grok-4.7 --tools read_file,list_dir,grep`
run from an empty folder under the job tmp holding only `DIFF.patch`, the changed files and `CONTRACT.md` — not the
producer's vendor, not the implementing session. `.github/workflows/conductor.yml` was not among the copied files
(the copy filter was by extension and the file path was lost), so the reviewer rebuilt the workflow from the diff.

## Findings and dispositions

**Critical (reported) — `ci_verdict.py:483` returns `PASS` before the baseline classification, so a sha CI did not judge landable reaches `main`.**
NOT REPRODUCED, recorded as a mis-read. The reviewer's premise is that a skipped or absent required context is excluded from `missing`. It is not: `missing = tuple(c for c in required_contexts if job_map.get(c) != "success")` (`scripts/ci_verdict.py:462`) counts a skipped and an absent context as missing, and the `PASS` branch needs `not missing`. A skipped required context returns `RED` with `missing_contexts` (witness: `test_G7_a_SKIPPED_required_context_is_not_a_success`; a skipped pytest leg is a required context). `land` passes the six contexts. The sub-claim about a short-sha prefix in `find_run` needs a short sha, and `land` hands it the full canonical sha (`ci_verdict.resolve_sha` resolves through git), so `startswith` is equality there; no change.

**High (reported) — `known_reds.compare_to_base`: a changed signature inside an already-red job is hidden when the base log carries no signature.**
CONFIRMED in part and FIXED. When the registry entry has no signature (73 of 189 entries today), the base line is a bare `FAILED id`, and the tip line carries a reason, nothing vouched for "the same failure". It now fails closed as `signature_changed` (`_no_basis`); a bare line on both sides still reads known. Witnesses: `test_table_a_tip_reason_the_base_never_carried_is_not_silently_known`, `test_table_a_bare_line_on_both_sides_stays_known_when_the_registry_has_no_signature` (RED before the fix).

**High (reported) — a pytest leg with no parsable node ids can read `PRE-EXISTING`.**
NOT REPRODUCED. The reviewer's own walk concludes the no-id and marker cases are covered inside `_judge_pytest_legs`, and the remaining route depends on the Critical's premise, which does not hold (a non-`success` pytest leg is a missing required context in `ci_verdict` and `UNATTRIBUTED` in `actions_verdict`; witnesses `test_G4_a_FAILED_leg_with_no_node_id_in_its_log_is_a_REGRESSION`, `test_G7_every_REQUIRED_context_must_be_present_and_success`).

**Medium — the integration push may fast-forward a long-lived integration branch that already holds other commits, so CI judges a range `main` will not receive.**
RECORDED, not fixed. The pushed object and the one that goes to `main` are the same merge sha, so no unjudged sha reaches `main`; the extra commits make `spine`/`seal`/`anchor` judge a wider range, which can only refuse. A per-merge ref or an explicit lease would remove it; both change the integration-branch name the contract fixes (`worktree-integrate-<batch>`). Owed to the integrator's first rehearsal.

**Medium — `record_push(target="main")` checked only the sha string, and the suite-before-push check used the FIRST push and FIRST suite step.**
CONFIRMED and FIXED. `main` is now recorded only when the receipt's latest suite read is `PASS` or `PRE-EXISTING`, and the order check uses the latest integration push and latest suite read. Witnesses: `test_G6_the_push_to_main_is_refused_unless_the_recorded_suite_read_is_landable` (6 states), `test_G6_the_suite_before_push_check_reads_the_LATEST_integration_push` (RED before). Partly not applicable: `land` already records the suite read through `actions_verdict.verdict_for`, the same classifier `ci_verdict` delegates to, before its own landable check.

**Medium (scored) — shell quoting of the integration arm in the workflow.**
NO DEFECT: the reviewer traced `target-line`, the redirect order, `seal-base` and the `case` quoting and found them sound. Its fallback-arm note (an empty `github.event.before` gives a three-field line) is unchanged pre-existing code on non-integration refs and is not G3.

**Low — run-event instrumentation could fail the organ it observes (only `OSError` was caught).**
CONFIRMED and FIXED: `emit_run_event` catches every `Exception`. Witness: `test_a_non_OSError_failure_in_the_event_path_never_raises_either`.

**Low — `_same` treated a prefix as equal.**
CONFIRMED and FIXED: exact comparison, and `land` refuses a base that is not a full 40-hex sha (`BASE-NOT-FULL`). Witnesses: `test_land_refuses_a_base_that_is_not_a_full_sha_and_pushes_nothing`, `test_the_same_sha_comparison_is_exact_not_a_prefix`.

**(none)** for the ruleset file: six contexts, `bypass_actors: []`, `refs/heads/main`, `enforcement: disabled`; and no force flag on any push.

## Honest limits

- One reviewer, one pass; the Critical was a mis-read of one `!= "success"` expression, which is itself the evidence that the witness for it existed before the review.
- No Codex pass has run on this diff. If the operator wants the pinned reviewer, `deploy/codex-review.ps1 -Topic foundation-4-merge-gate -DiffRange origin/main...HEAD` runs it after 02:25.
