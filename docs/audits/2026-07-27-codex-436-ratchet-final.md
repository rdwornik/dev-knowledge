# Codex Review — 436-ratchet-final

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `cec92435`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

THIRD review pass. Round 1 found 5 HIGH (all claimed fixed). Round 2 confirmed 3 held, found 2 incomplete + 1 new HIGH; those 3 are claimed fixed in cec92435. Verify ONLY whether any BLOCKING/HIGH defect remains:
1. _baseline_ref_state() splits bootstrap (ref resolves, no baseline file) from unknown (no ref resolves) -- bootstrap passes, unknown WARNs. Is the fail-open genuinely closed? Can an attacker/mistake reach 'bootstrap' while a baseline exists on the target?
2. iter_scoped_files now walks _SCOPE_RULES with casefolded suffix filtering and a two-part sort key. Any remaining platform sensitivity or non-determinism?
3. check_task_tree_coherence now catches (OSError, ValueError, KeyError, UnicodeDecodeError) -> fail and lets other exceptions propagate. Is the fail-closed contract sound? Does a propagating exception break the audit runner in a way that itself fails open?
State clearly for each whether it is RESOLVED or still HIGH. Report any NEW blocking defect.

---

## Findings
Two HIGH defects remain. No Critical defects or additional new blocking defects found.

## Critical

(none)

## High

## HIGH scripts/audit.py:2605 — Bootstrap does not prove the target baseline is absent

**What:** `_baseline_ref_state()` returns `"bootstrap"` whenever a ref resolves, even if `_previous_committed_baseline()` failed because the baseline exists but is malformed, unreadable, or `git show` timed out.

**Why:** A raised branch baseline can pass without comparison while an established target baseline exists, leaving the raise guard fail-open. The current branch is a genuine bootstrap—both target refs currently lack the file—but the general contract remains unsafe.

**Fix direction:** Read each authoritative ref into a structured state: unresolved, baseline absent, valid baseline, or invalid/unreadable. Allow bootstrap only when absence is positively proven; block invalid or indeterminate states.

## HIGH scripts/silent_rule_detector.py:119 — The enumerated file set remains platform-dependent

**What:** The two-part sort makes ordering deterministic only after enumeration. Host-filesystem walking still produces different sets for case-colliding paths; the new test explicitly permits one file on a case-insensitive filesystem versus three on a case-sensitive filesystem. Differently cased scope-root names have the same problem.

**Why:** The same Git tree can therefore produce different file and occurrence counts across platforms, allowing candidate rules to disappear from the ratchet measurement.

**Fix direction:** Derive or validate the corpus against Git’s tracked-path inventory, rejecting casefold-colliding paths and noncanonical scope-root casing before measurement. Define or reject symlink entries as well.

Focus verdicts:

1. `_baseline_ref_state()`: **STILL HIGH**
2. `iter_scoped_files()`: **STILL HIGH**
3. `check_task_tree_coherence()` exception posture: **RESOLVED** — known artifact errors return FAIL; unexpected exceptions propagate through `audit_repo`, `health`, and `ship-gate`, causing a nonzero process exit rather than a green result.
