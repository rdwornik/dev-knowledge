# Codex Review — adr85-integration-enforcement

**Date:** 2026-08-03
**Branch:** `feat/adr85-integration-enforcement`
**HEAD:** `8543841f`
**Diff range:** `main..feat/adr85-integration-enforcement`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- FR6 fail-closed: block_ff_push.py and block_unanchored_push.py must never return 0 on an internal error. Check every early-return and exception path for a silent allow.
- journal_anchor.py is the SHARED predicate for the pre-push gate and the audit backstop. A divergence between them, or a fail-soft that renders an unreadable history as "anchored", is the defect class this arc exists to remove.
- range_is_anchored treats an empty range as anchored. Verify that is correct for a push to main and cannot be reached with real unanchored work.
- _local_tip mirrors block_ff_push.resolve_push_range across two wirings (native stdin, PRE_COMMIT_* env). Check for a wiring where the tip and the range disagree.
- unanchored_on_spine excludes the floor commit itself and requires the floor be an ancestor. Check off-by-one and the not-an-ancestor path.
- audit.check_journal_spine_anchor reads the floor from the ADR by regex. Consider what a missing/duplicated/malformed floor line does.
- Tests: T1-T8 in tests/test_adr85_integration_enforcement.py. Flag any assertion that would pass even if the mechanism did nothing (vacuous/tautological), and any test that pins implementation shape rather than the acceptance criterion.

---

## Findings
## Critical

## [CRITICAL] scripts/block_ff_push.py:127 — stdin read errors silently allow the push

**What:** `_read_stdin()` converts `OSError`/`ValueError` into `""`; with no pre-commit env, `main()` treats that as “not main” and returns 0. `block_unanchored_push` shares this path.  
**Why:** This violates FR6: an internal failure can silently bypass both pre-push gates.  
**Fix direction:** Propagate input-read failures to `main()` and return exit 2; add a regression test for the native-stdin error path.

## [CRITICAL] scripts/block_ff_push.py:185 — scan failures are converted into a clean result

**What:** `violations_in_range()` delegates to `validate_no_ff.find_violations()`, whose git-error contract is `[]`; `main()` then returns 0.  
**Why:** A failed git scan is indistinguishable from “no violations,” defeating the new fail-closed contract.  
**Fix direction:** Use a gate-specific scan that preserves command failure, or change the shared API to expose an error result and refuse on it; test a nonzero `git log` result.

## High

## [HIGH] scripts/block_unanchored_push.py:83 — pre-commit fallback can skip a real main push

**What:** Unlike `block_ff_push`, this gate does not reconstruct the protected-main range when pre-commit has consumed stdin and forwarded another ref (or omits refs on an initial push). It returns 0 at line 85.  
**Why:** A multi-ref or fresh-remote push that includes unanchored `main` work can bypass the ADR-85 hard leg.  
**Fix direction:** Give the anchor gate the same protected-ref reconstruction and matching tip resolution, with tests for both native stdin and pre-commit wiring.

## [HIGH] scripts/journal_anchor.py:86 — ambiguous ADR floor is accepted

**What:** `floor_sha()` uses `search()` and returns the first matching floor; duplicate valid floor lines or a malformed line alongside a valid one are silently accepted.  
**Why:** A later, higher floor can be ignored or selected, changing which unanchored history is exempted instead of failing closed.  
**Fix direction:** Require exactly one well-formed floor declaration and raise `AnchorError` for duplicates or malformed/ambiguous declarations.

## [HIGH] tests/test_adr85_integration_enforcement.py:280 — `--no-verify` transport assertion is vacuous

**What:** T6 runs `git push --no-verify` without installing the pre-push hook, so the push would succeed even if `block_unanchored_push.py` did nothing.  
**Why:** It does not verify that `--no-verify` is bypassing a real refusal, leaving the actual hook wiring untested.  
**Fix direction:** Install the configured pre-push hook in the throwaway repo; assert normal push refuses, then assert `--no-verify` transports and the audit backstop fails.

## Medium

(none)

## Low

## [LOW] tests/test_adr85_integration_enforcement.py:178 — test pins a private implementation shape

**What:** T3 asserts `seb._HARD_CHECKS == ()` in addition to checking observable Stop-hook output.  
**Why:** A valid advisory-only implementation can change the private registry shape while preserving FR5 behavior.  
**Fix direction:** Keep the subprocess/output assertion and remove the private-tuple assertion.