# Codex Review — l6-test-pairing-fixes

**Date:** 2026-09-20
**Branch:** `worktree-lane-l6-test-pairing`
**HEAD:** `b3e36b87`
**Diff range:** `main..worktree-lane-l6-test-pairing`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Re-review after fixes to the five HIGH findings of docs/audits/2026-09-20-codex-l6-test-pairing.md. Verify each fix actually closes its finding and introduces no new defect.
- The pytest plugin (_PLUGIN / read_events / run_pytest): xdist duplicates, concurrent appends, a red overwritten by a later green, missing events file, PYTHONPATH handling, plugin file leaking into the tested clone.
- Baseline confirmation in pair(): batched rerun on BASE, reclassification to lane candidate, interaction with collection-error file-level ids and with the flake rule.
- Any way a lane-caused red can still exit 0.

---

## Findings
The five prior HIGH findings are closed. New HIGH findings remain.

## Critical

(none)

## High

### scripts/test_pairing.py:137 — xdist workers concurrently append to one event file

**What:** Multiple pytest/xdist processes append JSON lines to the same file without interprocess synchronization.  
**Why:** Writes can interleave or be lost; `read_events()` silently discards malformed rows, allowing a HEAD failure to disappear and the pairing to report `CLEAN`/exit 0.  
**Fix direction:** Use per-worker event files or a single controller-side writer, then validate the complete merged result.

### scripts/test_pairing.py:160 — Missing or empty event output is accepted as a successful test result

**What:** `read_events()` returns `{}` when the event file is absent, and `run_pytest()` accepts pytest exit codes 0 and 1 with no events.  
**Why:** Plugin/reporting failure can turn a real failing run into empty HEAD results, producing `CLEAN` and exit 0.  
**Fix direction:** Fail closed when the required event artifact is missing or inconsistent with a pytest invocation.

### scripts/test_pairing.py:193 — Inherited `PYTHONPATH` can import code outside the detached clone

**What:** The subprocess preserves the caller’s entire `PYTHONPATH`.  
**Why:** A source checkout or editable path in that variable can shadow code in BASE or HEAD, so a lane-caused failure can be hidden by a different local version and exit 0.  
**Fix direction:** Construct a controlled import path for the plugin and clone; exclude caller paths resolving into the source checkout.

### scripts/test_pairing.py:356 — `--tests` permits directory targets and can run the full suite

**What:** The option accepts arbitrary pytest targets, including `.` or `tests/`, despite being documented as test files.  
**Why:** This bypasses the no-full-suite contract and can unexpectedly run all tests.  
**Fix direction:** Validate explicit targets as individual test files/node IDs, rejecting directories and broad pytest selectors.

## Medium

(none)

## Low

(none)