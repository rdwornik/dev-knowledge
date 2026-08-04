# Codex Review — 465-leg4-inert-check-detector

**Date:** 2026-08-04
**Branch:** `fix/465-leg4-tag-canonicity`
**HEAD:** `f020e0b9`
**Diff range:** `main..fix/465-leg4-tag-canonicity`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- _na/_na_reason: 32 call sites were mechanically converted from Finding(x,"n/a",msg) to _na(x,"NOT-APPLICABLE",msg). Is every one of those classifications actually correct, or is any site truly SUBJECT-ABSENT? Did the sweep corrupt any multi-line/edge construction? Check the helper itself is not recursive.
- detect_unconditionally_inert_checks: correct inertness rule? Can it FALSE-POSITIVE on a consumer (FR-7 / the D1 regression), or FALSE-NEGATIVE on a genuinely dead check? Is late-binding ALL_CHECKS via `checks=None` genuinely roster-free? Any silent-pass path when a check misbehaves?
- append_history retirement notice: this MUTATES THE DURABLE WRITER. Can the notice ever fail the daily write, emit a false retirement (e.g. a repo whose previous reading was partial/errored, a same-day second run, an out-of-order date), or miss a real one? Is _previously_reported_checks' "strictly before" date comparison sound for the file naming scheme?
- Retirement completeness: is check_handoff_tag_canonicity gone from EVERY surface (ALL_CHECKS, doc-code-edge exempt, tests, deploy manifests)? Is ALL_CHECKS 38 consistent everywhere (4 test pins + doc-counts)?
- Tests: any vacuous, tautological, or self-constructing assertions? Note the detector cannot fire on the live registry post-retirement - is the synthetic-member coverage genuinely sufficient, or is something now untested in production shape?

---

## Findings
## Critical

(none)

## High

### scripts/audit.py:3612 — Inert-check detector is never invoked

**What:** `detect_unconditionally_inert_checks()` is only called by tests; `run`, `health`, and `ship-gate` still execute `ALL_CHECKS` directly.  
**Why:** A future inert check will continue to write normal dailies without any `writer_integrity` warning—the detector has no production effect.  
**Fix direction:** Invoke it from the fleet/daily audit using the actual registered repo paths and persist/surface its warnings.

### scripts/audit.py:456 — Same-day reruns repeat a retirement notice

**What:** `_previously_reported_checks()` ignores the existing file for `run_date`, so each same-day `append_history()` compares against yesterday and re-emits the same retirement notice.  
**Why:** A second `run`/`repo` invocation records “retired since the previous reading” even when the prior same-day reading already documented it, corrupting the durable history’s meaning.  
**Fix direction:** Compare against the most recent prior entry, including same-day entries, and parse only that entry’s table rather than all appended tables.

### tests/test_writer_integrity.py:196 — Live-registry test ignores detector failure warnings

**What:** The test filters for `"INERT"` and passes even if the live roster produces `writer_integrity` warnings for an unclassified `n/a`, exception, or empty result.  
**Why:** The synthetic cases test those branches in isolation, but the production-shaped `ALL_CHECKS` invocation does not verify that all mechanically converted call sites are actually classifiable and evaluable.  
**Fix direction:** Assert that the live detector output is empty (or explicitly assert no `writer_integrity` warning), alongside the inert-check assertion.

## Medium

(none)

## Low

(none)

The `_na` helper is non-recursive, and the converted production call sites appear to be per-repo/conditional skips; I found no clear case that should be classified `SUBJECT-ABSENT`.