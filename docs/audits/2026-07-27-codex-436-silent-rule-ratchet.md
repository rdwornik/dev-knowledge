# Codex Review — 436-silent-rule-ratchet

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `c64c7f9f`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

- scripts/silent_rule_detector.py is a NEW pinned metric definition. Scrutinise the detector contract: is the count deterministic and platform-stable? Does iter_scoped_files have a path-exclusion bug (archive segment matching, relpath comparison on Windows)? Can the metric be trivially gamed or accidentally inflated?
- The ratchet-down-only invariant is enforced in two places: validate_transition (pure) and _previous_committed_baseline (git show HEAD). Is the git leg correct on a merge commit, a first commit, and a detached HEAD? Does fail-soft-to-None create a bypass?
- check_silent_rule_ratchet and check_task_tree_coherence are new ALL_CHECKS members and therefore ship-gate legs. Verify the hub-only guards, the Finding status choices (fail vs warn vs unavailable), and that exactly one Finding is emitted per check (the #147 disposition contract).
- gen_task_tree.py: find_incoherences was extracted from _cmd_check. Confirm CLI behaviour and exit codes are genuinely unchanged and no problem-path was dropped in the extraction.
- Tests: do the four contract cases (pass-at-baseline, fail-above-baseline, ratchet-down accepted, baseline-raise rejected) actually pin what they claim? Any test that would pass vacuously?

---

## Findings
```text
## CRITICAL

(none)

## HIGH scripts/audit.py:2581 — Ratchet compares the baseline against the current commit

What: `_previous_committed_baseline` reads `HEAD`, so after committing—or on a merge commit or detached HEAD—the new baseline is compared with itself; failure returns `None` and silently skips validation.
Why: A raised baseline passes the ship gate after commit, and deleting then re-adding the file resets history without requiring `--no-verify`. The baseline-raise test exercises only `validate_transition`, so it misses this bypass.
Fix direction: Compare the candidate baseline with the appropriate parent baseline(s), handle pre-commit and post-commit states explicitly, and emit a blocking Finding when history cannot be established.

## HIGH scripts/audit.py:2677 — Detector failure is non-blocking at ship time

What: Measurement errors produce `status="unavailable"`.
Why: `cmd_ship_gate` blocks only `fail` and undispositioned `warn`; therefore unreadable or undecodable scoped files allow the ratchet to ship green without measuring anything.
Fix direction: Return `fail`, or at minimum `warn`, for detector failures so the ship gate blocks.

## HIGH scripts/audit.py:2724 — Missing task tree is reported as not applicable

What: On the hub, a missing `BACKLOG.md` or `tasks/` returns `n/a` before `find_incoherences` can report the missing output directory.
Why: The newly armed coherence leg becomes non-blocking when its required derived artifact is removed. The missing-directory test covers only the helper and therefore does not catch the adapter bypass.
Fix direction: Reserve `n/a` for the off-hub guard; return a failing Finding when either required hub artifact is absent.

## HIGH scripts/silent_rule_detector.py:123 — Physical line count is trivially gameable

What: The metric counts matching lines rather than normalized rules or keyword occurrences.
Why: Joining two rule lines lowers the count without removing a rule, while splitting or reflowing one line raises it. It also counts examples and already-enforced rules, so harmless formatting can block shipping while equivalent silent rules can create headroom.
Fix direction: Base the metric on normalized candidate records or stable fingerprints, excluding non-rule contexts; bump `DETECTOR_ID` and remeasure the baseline.

## HIGH scripts/silent_rule_detector.py:94 — Path exclusions are not platform-stable

What: Archive segments and excluded relative paths use case-sensitive string comparisons after platform-dependent glob discovery.
Why: Windows can discover differently cased paths such as `templates/Archive/...` or an excluded YAML path while the exact comparisons fail, producing counts that differ from case-sensitive platforms.
Fix direction: Enumerate canonical Git/POSIX paths with explicit case semantics, or normalize both segment and relative-path comparisons; add mixed-case Windows contract tests.

## MEDIUM

(none)

## LOW

(none)
```
