# Codex Review — lane-ci-verdict

**Date:** 2026-09-24
**Branch:** `worktree-lane-ci-verdict`
**HEAD:** `4b7268b1`
**Diff range:** `main..worktree-lane-ci-verdict`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low. All 3 HIGH findings fixed in 4b7268b1's follow-up commits: the run-level conclusion check, the window-scoped suite-gate parse (plus a second-resolution padding fix found while verifying it against the live run), and the busy-loop test fix. -->
**Disposition:** all 3 HIGH findings FIXED (pre-authorized ruling 2(e): fix a Codex review's P1 findings). Re-verified against the live run (`run_id 35907748018`) after each fix; see LANE-5A-6's session file.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- New organ scripts/ci_verdict.py (LANE-5A-6): read-only against GitHub (gh run list/view only), no writes to .github/workflows, impacted_tests.py, repo settings or rulesets
- Consumer: .claude/commands/lane-integrate.md's new standalone (non-gating) step that records this organ's JSON verdict beside the local one
- Check: the in-process polling loop (wait_for_run) terminates correctly on every branch (completed, still in-progress past timeout, gh unavailable mid-poll), and the green/red/not-run verdict never reports green when it should not
- Check: parse_suite_gate_block's regex parsing of gh's tab-separated --log output is robust to the format observed live (2026-09-24)

---

## Findings
## CRITICAL

(none)

## HIGH

## [HIGH] scripts/ci_verdict.py:323 — A failed/cancelled workflow can be reported green

**What:** The verdict ignores `run["conclusion"]`; an empty job list, or only `success`/`skipped`/`None` job conclusions, returns `green` even when the completed run itself concluded non-success.  
**Why:** This violates the organ’s “never green when it should not” contract and can record a failed Actions run as green.  
**Fix direction:** Require a successful completed workflow conclusion before returning green; classify non-success conclusions without a failing job as red or not-run conservatively.

## [HIGH] scripts/ci_verdict.py:210 — Suite-gate parsing is not scoped to the suite-gate step

**What:** The parser discards the tab-separated step field and accepts the header, baseline, and regression lines from anywhere in the pytest job log.  
**Why:** Output from pytest or another step that happens to contain these strings can be misrepresented as the suite gate’s verdict, producing fabricated baseline/regression data.  
**Fix direction:** Retain and validate the live step field, then parse only the suite-gate command’s output block.

## [HIGH] tests/test_ci_verdict.py:121 — No-match test busy-loops for the full 900-second default timeout

**What:** The test injects a no-op sleeper but leaves the real monotonic clock and default timeout, so `wait_for_run` repeatedly calls the empty list function until 15 real minutes elapse.  
**Why:** The targeted test suite stalls rather than executing hermetically.  
**Fix direction:** Use a fake advancing clock or set a zero/small timeout with a clock-compatible sleeper.

## MEDIUM

(none)

## LOW

(none)