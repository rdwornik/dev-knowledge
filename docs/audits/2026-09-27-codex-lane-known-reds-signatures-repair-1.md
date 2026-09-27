# Codex Review — lane-known-reds-signatures-repair-1

**Date:** 2026-09-27
**Branch:** `worktree-lane-known-reds-signatures`
**HEAD:** `ded3a22f`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. Verified against the Findings section below: one High, zero elsewhere. Fixed in a follow-up commit -- see the note after Findings. -->

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

---

## Disposition

**Fixed**, same lane, next commit: `_LIST_BODY_RE` is now scoped to a list that trails an
explanatory `": "` (the census/citation shape both real regressions had -- a human-composed
diagnostic message ending in a formatted list), via a `(?<=: )` lookbehind, so it never
matches a bare pytest comparison repr like `assert ['old'] == ['expected']`. RED-first witness:
`tests/test_known_reds.py::test_normalize_signature_never_masks_a_bare_list_equality_assertion`
(fails against the unscoped regex, passes against the scoped one). Re-verified against the
same real evidence this repair already used (run 36337021076's Windows leg,
`known_reds.py compare --os windows-latest`): the three originally-flagged ids
(`test_the_real_pre_launch_moment_refuses_an_occupied_husk`,
`test_A_LANES_BASE_EQUALS_MAIN_HEAD_AT_DISPATCH`,
`test_committed_baseline_agrees_with_a_live_measurement`) still read as known, unchanged by
the narrower regex.