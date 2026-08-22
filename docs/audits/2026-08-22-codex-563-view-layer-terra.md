# Codex Review — 563-view-layer-terra

**Date:** 2026-08-22
**Branch:** `HEAD`
**HEAD:** `b02871c8`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/1/0/0

**Disposition (integrator, 2026-08-22):** BOTH CONFIRMED against source and FIXED in `a7391b56` on `fix/terra-cloud-wave-2026-08-22`, classified MECHANICAL per ADR-111 section 4 (judgment-free). This review discharges the residual cloud-2's own artifact section 8 item 1 records as OWED -- it could not run in the cloud container, which carried neither the `codex` CLI nor the hub wrapper.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## Critical

## [CRITICAL] tests/test_export_backlog_view.py:471 — Cleanup failures are silently ignored

**What:** The test deletes its real repo-level `.backlog-view` export with `ignore_errors=True` and never verifies removal.  
**Why:** A failed cleanup lets the test pass while leaving generated artifacts behind, violating the repo’s no-leftovers invariant.  
**Fix direction:** Let cleanup failures fail the test and assert the directory no longer exists.

## High

## [HIGH] scripts/export_backlog_view.py:401 — Generated config uses an unsupported default-status key

**What:** The exporter writes `default_status`, while Backlog.md’s configuration key is `defaultStatus`.  
**Why:** The setting is ignored, leaving the default `To Do`, which is outside the generated `open/deferred/closed/retired/superseded` status set and can create invalid/invisible tasks through the UI. [Backlog.md configuration docs](https://github.com/MrLesk/Backlog.md/blob/main/ADVANCED-CONFIG.md)  
**Fix direction:** Emit `defaultStatus: 'open'` and update the config test to cover the recognized key.

## Medium

(none)

## Low

(none)