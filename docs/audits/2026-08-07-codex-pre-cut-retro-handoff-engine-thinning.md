# Codex Review — pre-cut-retro-handoff-engine-thinning

**Date:** 2026-08-07
**Branch:** `chore/pre-cut-gate-hygiene`
**HEAD:** `b669bd8f`
**Diff range:** `25ff8ec3..b669bd8f`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

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

## [HIGH] scripts/gen_handoff.py:403 — Open-batch refusal can be bypassed by inherited Git location variables

**Disposition:** filed as [#512] (fix-or-file; contract forbids editing `gen_handoff.py` / batch machinery in this arc). Not fixed here.


**What:** `_open_batches()` delegates to `batch_manifest.open_batches()`, whose Git calls do not scrub `GIT_DIR` and related location variables.  
**Why:** An inherited/bogus `GIT_DIR` makes the reader return no open batches, allowing an immutable handoff to be cut during a real open batch—the exact wrong-repository failure this generator otherwise guards against.  
**Fix direction:** Invoke the shared reader with a scrubbed Git environment (or move its Git reads behind the generator’s scrubbed helper) and add a regression test with an open committed manifest plus inherited `GIT_DIR`.

## Medium

(none)

## Low

(none)