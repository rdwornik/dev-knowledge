# Codex Review — lane-registry-models

**Date:** 2026-09-25
**Branch:** `worktree-lane-registry-models`
**HEAD:** `6859c4d2`
**Diff range:** `main..worktree-lane-registry-models`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

**Consumer:** `LANE-5B-2-registry-models.md` (WAVE5B-N1 §2 row 2) Done item 4 — the model-currency
mechanism this review's two findings are about.

**Disposition (both HIGH, fixed on the same branch, same HEAD range):**
- `tests/test_provider_router.py:580` — `_newest_sharing_shape` now returns `None` (never a
  real model id) when the pinned id has no same-shape sibling in the listing at all, so a fully
  retired pin can no longer pass the check by omission. New regression test:
  `test_newest_sharing_shape_does_not_wave_through_a_fully_retired_id`.
- `tests/test_provider_router.py:614` — added `_live_listing` and the opt-in
  `test_live_probe_executes_the_declared_command_and_applies_the_comparison`
  (`RUN_LIVE_CURRENCY_PROBE=1`, the `RUN_E2E` precedent), which actually executes each
  provider's declared `model_currency.command`, parses it, and applies the same comparison to
  the real, current listing. Run against all three live CLIs (codex, grok, agy) on this box
  2026-09-25 and passed.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

provider registry model currency and cache-write pricing

---

## Findings
## Critical

(none)

## High

## [HIGH] tests/test_provider_router.py:580 — a retired pinned model can be accepted as current

**What:** `_newest_sharing_shape()` returns the pinned ID when the CLI listing contains no same-shape sibling, including when the pinned ID is absent from that listing.  
**Why:** A removed model such as `grok-4.6` can pass the currency check without a `currency_exception`, silently leaving a non-served model pinned.  
**Fix direction:** Require the pinned ID to occur in the listing; treat its absence as stale and require an exception.

## [HIGH] tests/test_provider_router.py:614 — currency checks never consume the declared CLI probes

**What:** The tests compare role pins with hard-coded captured lists rather than executing/parsing `providers.*.model_currency.command`; the declared commands are only checked for argv[0] identity.  
**Why:** Vendor listings can change while every test remains green, so the new `model_currency` data does not provide ongoing currency detection.  
**Fix direction:** Add a designated probe/sentinel that executes and parses each declared command, then applies the comparison to every pinned model (with explicit skipped/exception outcomes).

## Medium

(none)

## Low

(none)