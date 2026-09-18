# Codex Review — b2-regressions-fix

**Date:** 2026-09-19
**Branch:** `fix/b2-regressions`
**HEAD:** `548b2cf7`
**Diff range:** `main..fix/b2-regressions`
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
## CRITICAL

(none)

## HIGH

## [HIGH] ecosystem/silent-rule-baseline.yaml:21 — Raised baseline fails the ratchet gate

**What:** The baseline increases from 447 to 452 while retaining `silent-rule-v5`.  
**Why:** The ship-gate compares against `main`’s committed 447 baseline and explicitly rejects same-detector increases, so this branch cannot pass the silent-rule ratchet.  
**Fix direction:** Drain the added occurrences, or change the ratchet’s reviewed transition contract to support an operator-approved exception before raising the baseline.

## MEDIUM

(none)

## LOW

(none)