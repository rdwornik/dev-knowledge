# Codex Review — cloud4v2-registries-terra

**Date:** 2026-08-22
**Branch:** `HEAD`
**HEAD:** `7b16f258`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/2/0/0

**Disposition (integrator, 2026-08-22):** ONE CONFIRMED and FIXED, ONE PARTLY REFUTED. The S10 pin-count finding is real -- `check_s10` returned clean when a pin was DELETED, contradicting the artifact's own "all three" claim -- and is fixed in `a7391b56` with a mutation-checked deletion regression test. The absolute-path finding is REFUTED AS STATED: the registry does not *introduce* `C:\Users\1028120\...`; that string is already committed on `main` at `.claude/settings.json:63`, and the registry's own comment says exactly that. The underlying portability defect is real, PRE-EXISTING and owned by no row, so it is carried to the wave-close funnel table rather than charged to this lane. This review discharges the residual cloud-4v2's artifact section 7 item 1 records as OWED.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### ecosystem/provider-registry.yaml:60 — Committed machine-specific absolute path

**What:** The registry introduces `C:\Users\1028120\...` as canonical configuration.  
**Why:** Other checkout locations/users will fail the registry agreement check and cannot use the setting unchanged.  
**Fix direction:** Keep machine-local paths out of committed registry data; derive from the checkout or use local/environment-specific configuration.

### scripts/check_provider_registry.py:141 — Missing workflow model pins pass validation

**What:** S10 only rejects incorrect discovered pins; removing one or two of the three required `model:` fields still returns clean as long as one correct pin remains.  
**Why:** A verifier stage can silently fall back to a default model, defeating the registry’s intended coupling.  
**Fix direction:** Assert the expected pin count and/or explicitly validate each required workflow stage; add a deletion test.

## Medium

(none)

## Low

(none)