# Codex Review — b2-rulings-landing, repair 1

**Date:** 2026-10-04
**Branch:** `worktree-b2-rulings-landing`
**Diff range:** repair 1 = `af1e9e28..82aaafdd` (the sync merge, then three commits); pass A at `defb2fae`, pass B on the delta `defb2fae..82aaafdd`
**Mode:** diff-review, isolated read-only session (the diff, the post-repair source and test files, the contract and the refusal in an empty job-tmp folder, not the lane)
**Consumer:** `LANE-B2-W1-b2-rulings-landing.md` (Done-contract item 5) as repaired under `to-browser/REFUSED-b2-rulings-landing.md` (INTEGRATOR, repair 1 of 2); it continues `docs/audits/2026-10-04-codex-b2-rulings-landing.md`, whose pass 4 P1 this repair answers

**Model used:** `gpt-5.6-terra` (served: `OpenAI Codex v0.155.0`, `-c model=gpt-5.6-terra`, as in the first record)
**Command (both passes):** from an empty job-tmp folder, `codex exec -c model=gpt-5.6-terra --sandbox read-only --skip-git-repo-check --output-last-message codex-out.txt -` with the prompt on stdin, run detached. The answer had to open with the nonce from `nonce.txt` and quote the first line of `diff.patch`; both did.

| pass | nonce returned | first line quoted | scope | reviewer verdict |
|---|---|---|---|---|
| A | `NONCE-a03f15ef20c2` | `diff --git a/scripts/decision_coverage.py b/scripts/decision_coverage.py` | repair commit `defb2fae` | reject |
| B | `NONCE-bda9b2a512e8` | same | fix delta `defb2fae..82aaafdd` | reject |

## What the refusal named, and what was done

| refusal item | disposition |
|---|---|
| `test_coverage_drift_guard_registered_and_clean_on_live_repo` and `test_all_checks_count_is_pinned`: the registered-check count pinned at 58 | **Fixed**: both pins read 59 with a dated reason. DECIDED-BY-LANE: the two files are outside "Files you own", in the same class as `tests/test_handoff_cut_acceptance.py` (a registered check forces the pin; the refusal accepts the rule). |
| `test_derivation_finds_nothing_missing_from_the_real_registry`: `R-` read as a transport prefix | **Fixed**: the literal was `f"R{entry.number}"` in `decision_coverage.py` (`transport.derive_kinds_from_code` reads an `R` before a placeholder as a template prefix). `_ruling_id()` builds the id by concatenation, and no `R{...}` template remains in the file (`test_no_f_string_ruling_id_template_remains_in_decision_coverage`). No registry row; `transport.py` and the registry are untouched. |
| Pass 4 P1: `refused` is False for an unmeasured report | **Fixed, RED-first**: `refused` is removed. `RulingsReport` has `passed` (True only when both legs were measured clean) and `exit_code(no_transport=)` (1 on a finding, 2 on an unmeasured leg (a), else 0); the CLI returns `exit_code`. RED: `test_an_unmeasured_report_has_no_attribute_that_reads_as_not_refused` failed on `hasattr(report, "refused")`, `test_exit_code_is_1_on_a_finding_whether_or_not_leg_a_was_measured` failed on a missing `exit_code`. |

## Pass A — repair commit `defb2fae`

| finding | disposition |
|---|---|
| **P1** `found`, the list that replaced `refused`, is `[]` for an unmeasured report, so `not report.found` is fail-open again | **Fixed** in `82aaafdd`: the accessor is private (`_findings`); the verdicts are `passed` and `exit_code`. RED-first as above. |
| **P1** two `f"R{ruling.number}"` templates remain in `unlanded_rulings` | **Fixed** in `82aaafdd`: every `R{...}` in the file goes through `_ruling_id`. The derivation did not read them as `R-` (the test passed), so this is hardening, now pinned by a source test. |
| the reviewer's own note: the CLI exit-code logic is correct | recorded as given |

## Pass B — fix delta `82aaafdd`

| finding | disposition |
|---|---|
| Previous P1 (`found` fail-open): "not fixed" | **Not accepted as stated, disclosed.** The delta removed `found`; the reviewer's ground is the raw per-leg fields, below. |
| Previous P1 (`R{...}` derivation): "fixed" | confirmed by the reviewer |
| **HIGH** `uncarried` (`:1340`) is `[]` for a clean leg (b), so `not report.uncarried` reads clean while leg (a) is unmeasured | **Declined, with the reason.** It is the per-leg datum and `[]` is the true answer for leg (b): the repair scope is the VERDICT surface the pass-4 P1 named. Its only readers are the report's own methods and `audit_checks/check_rulings_carried.py:63-65`, which reports leg (b) on its own line and handles leg (a) separately. Making it private is a rewrite of the report's shape and of that adapter. |
| **HIGH** `unlanded` (`:1341`) is `None` (falsey) for an unmeasured leg, so `not report.unlanded` reads clean | **Declined, with the reason.** `None` is the documented "not measured" sentinel, tested as `is None` by every reader (`check_rulings_carried.py:71`, `exit_code`, `render`, `passed`) and asserted in the tests. A reader that writes `not report.unlanded` instead of `is None` is the hazard the docstring names; the verdict surface no longer offers it a shorter route. |

The two declined items are a broader hardening than the refusal asked for; they are reported here so the integrator can rule on them. They are **not** treated as fixed, and the reviewer's last verdict line reads `reject` on both passes.

## What the review did not examine

Pass A and B saw only the repair diff and the two source files. The three tests the refusal named were run on the tip, detached, through `scripts/memory_admission_gate.py run`; they passed. Five other tests failed in that run and are attributed in the session file (live-transport dependence or red on the base CI run), none to this diff.
