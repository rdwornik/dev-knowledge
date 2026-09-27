# Codex Review — lane-known-reds-signatures-repair-1

**Date:** 2026-09-27
**Branch:** `worktree-lane-known-reds-signatures`
**HEAD:** `ded3a22f`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

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

### scripts/known_reds.py:414 — Signature normalization masks arbitrary assertion list values

**What:** `_LIST_BODY_RE` replaces every non-nested bracketed value with `[<LIST>]`, not just the intended volatile census list.  
**Why:** A changed failure such as `assert ['old'] == ['expected']` becoming `assert ['new'] == ['expected']` normalizes identically and is accepted as pre-existing, defeating the new signature-regression check.  
**Fix direction:** Restrict list masking to an identifiable volatile failure format, or retain list contents when they are part of a normal assertion.

## Medium

(none)

## Low

(none)