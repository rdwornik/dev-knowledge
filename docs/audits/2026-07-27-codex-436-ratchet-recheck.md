# Codex Review — 436-ratchet-recheck

**Date:** 2026-07-27
**Branch:** `feat/436-silent-rule-ratchet`
**HEAD:** `5e655cc1`
**Diff range:** `527958fb..feat/436-silent-rule-ratchet`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

This is a RE-REVIEW. A prior terra pass returned five HIGH findings, all claimed fixed in commit 5e655cc1. Verify each fix actually holds, and report any finding that is NOT genuinely resolved:
1. Metric unit changed from per-line to per-occurrence (reflow-gaming). Is it now reflow-stable?
2. Raise-guard now reads origin/main (falling back to main) instead of HEAD. Does this actually close the post-commit self-comparison bypass? Consider: branch raises baseline, main has lower value; and the case where origin/main is absent.
3. Detector measurement failure now returns Finding status 'fail' instead of 'unavailable'. Does ship-gate now block?
4. Missing BACKLOG.md/tasks/ on the hub now returns 'fail' instead of 'n/a'. Is the off-hub 'n/a' guard still correct?
5. Path/ordering comparisons casefolded for platform stability. Any remaining case or platform sensitivity?
Also: any NEW defect introduced by these five fixes.

---

## Findings
Re-review result: fixes 1, 3, and 4 hold. Fixes 2 and 5 remain incomplete.

## [CRITICAL]

(none)

## [HIGH] scripts/audit.py:2643 — An unavailable raise guard still passes

**What:** If neither `origin/main` nor `main` provides a readable baseline, the check returns `pass` with an “INACTIVE” annotation.  
**Why:** Ship-gate ignores annotations on passing findings, so a detached/shallow checkout can raise the baseline and ship green. The fallback works when local `main` exists, but the no-ref case remains fail-open.  
**Fix direction:** Return `warn` or `fail` when the previous baseline is unavailable, with a narrowly verified exception for genuine first-time bootstrap; add behavioral git-repository tests for remote-main, local-main fallback, and neither-ref cases.

## [HIGH] scripts/silent_rule_detector.py:106 — File enumeration remains platform-sensitive

**What:** `Path.glob()` uses its platform-default case sensitivity; only exclusions and subsequent sorting are casefolded.  
**Why:** A mixed-case root, extension such as `.MD`, or filename can be counted on Windows and omitted on Linux, producing different measurements and ratchet decisions. Casefold-only sorting also has unstable ties for paths differing only by case.  
**Fix direction:** Enumerate with explicit case-insensitive matching, use a deterministic secondary sort key, and test mixed-case roots/extensions plus casefold-colliding paths.

## [HIGH] scripts/audit.py:2761 — Broad exception weakens the task-tree fail-closed contract

**What:** Every unexpected exception from `find_incoherences()` is converted into a non-blocking `warn`.  
**Why:** The commit-time audit blocks only `fail`, so malformed inputs or programming defects can bypass the gate described as FAIL-class; the broad catch also obscures specific failure causes.  
**Fix direction:** Catch known artifact-reading exceptions and return `fail`; allow unexpected programming errors to propagate or otherwise block explicitly.

## [MEDIUM]

(none)

## [LOW]

(none)
