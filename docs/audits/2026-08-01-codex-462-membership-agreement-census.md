# Codex Review — 462-membership-agreement-census

**Date:** 2026-08-01
**Branch:** `feat/462-membership-agreement-census`
**HEAD:** `a049f661`
**Diff range:** `main..HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

New audit check check_membership_agreement in scripts/audit.py: correctness of the surface readers, the pure classifier, the hub-only guard, and error handling. Verify the PASS-not-FAIL verdict for declared-but-not-deployed is coherent with the FAIL direction. Check the registry.md row does not break parse_registry_md. Check the ADR-109 appended amendment does not edit decision body prose in place.

---

## Findings
## Critical

(none)

## High

scripts/audit.py:3289 — State-directory scan can crash the audit instead of returning a FAIL finding.

**What:** `eco.iterdir()` / child path checks run outside the surface-read `try` block.  
**Why:** Permission or filesystem I/O errors abort `audit.py health`, bypassing the gate’s intended fail-closed reporting.  
**Fix direction:** Wrap the `state-dirs` read in the same error-to-`Finding(..., "fail", ...)` handling as the other surfaces.

## Medium

(none)

## Low

(none)