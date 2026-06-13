# Codex Review — 163-probe-validator

**Date:** 2026-06-13
**Branch:** `worktree-163-validator`
**HEAD:** `95e625f`
**Diff range:** `ad56397..HEAD`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- Parser: pipe inside a backtick code span must NOT split the row (split_row backtick-awareness); column mapping is by header NAME (live tables carry a leading # id col).
- Zero-false-positive guarantee: command targets come from the FIRST backtick span only (the P5 audit.py-shorthand false-FAIL trap); file tokens are extension-anchored; the Why column is checked for presence only.
- No silent-pass path: an unresolvable # anchor must be WARN anchor-missing, never PASS; tool-absent must be skipped, never PASS; resolve-only (no subprocess execution).
- check_handoff_probes adapter: FAIL-class gating wiring, latest-bundle-only selection, fail-soft.

---

## Findings
## CRITICAL
(none)

## HIGH

Severity: HIGH  
File: `scripts/audit.py:1376`  
What: An existing but empty or unparseable `PROBES.md` returns zero results and is reported as PASS.  
Why: This creates a silent-pass path where the latest bundle can have no valid probe rows and still clear the gate.  
Fix direction: Treat zero parsed probes from an existing `PROBES.md` as a FAIL, either in `verify()` or in `check_handoff_probes()`.

Severity: HIGH  
File: `scripts/verify_handoff_probes.py:202`  
What: A non-empty command cell with no backtick span produces `cmd == ""` and can still PASS.  
Why: The validator then skips command target resolution and executable detection, violating the no silent-pass guarantee.  
Fix direction: Classify a command cell with no first backtick span as malformed FAIL.

Severity: HIGH  
File: `scripts/audit.py:1371`  
What: Multiple `anchor-missing` / `skipped` probe results are collapsed into one WARN finding.  
Why: `ship-gate` dispositions operate per Finding, so dispositioning one expected warning can suppress unrelated degraded probes in the same aggregate warning.  
Fix direction: Emit one WARN Finding per degraded probe, with probe id and detail in the evidence.

## MEDIUM
(none)

## LOW
(none)
