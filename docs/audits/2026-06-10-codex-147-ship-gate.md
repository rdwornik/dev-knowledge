# Codex Review — 147-ship-gate

**Date:** 2026-06-10
**Branch:** `feat/147-ship-gate`
**HEAD:** `b265df3`
**Diff range:** `main..feat/147-ship-gate`
**Codex version:** codex-cli 0.136.0
**Mode:** diff-review

---

## Focus

- ship-gate verdict logic in scripts/audit.py (cmd_ship_gate, _match_disposition, _load_dispositions): is the block-on-FAIL-or-undispositioned-WARN classification correct and complete?
- F1 correctness: does it read Finding.status (not exit codes)? Any path where an awareness-organ WARN could slip through unblocked?
- _match_disposition precision: substring match keyed on sha 77e5d7d — any false-match risk (e.g. a different finding whose evidence coincidentally contains the token)?
- fail-soft on missing/malformed register: does it degrade to STRICTER (every WARN undispositioned), never looser? Any unhandled exception that wedges the gate?
- _GATE_MODE handling (set False in try/finally) — correct restoration; no global-state leak across invocations?
- Read-only contract: does cmd_ship_gate write anything?
- disposition-register.yaml schema: is the loader robust to a non-list dispositions value, missing keys, None entries?

---

## Findings
## CRITICAL

**CRITICAL scripts/audit.py:1730 — disposition can suppress unrelated WARN content**

**What:** `_match_disposition` is applied to the whole `Finding`, so one matched token dispositions the entire WARN.  
**Why:** `git_backlog_drift` can aggregate multiple drift items into one WARN; if the benign `77e5d7d` drift and a new undispositioned drift appear in the same evidence string, the whole finding is marked dispositioned and ship-gate can go GREEN incorrectly.  
**Fix direction:** Match dispositions at the individual warning/drift-item level, or require the gate to prove every component inside an aggregate WARN is dispositioned before suppressing it.

## HIGH

**HIGH scripts/audit.py:1666 — malformed `dispositions` scalar can wedge the gate**

**What:** `_load_dispositions` iterates `data.get("dispositions")` without first verifying it is a list.  
**Why:** A malformed register like `dispositions: 1` or `dispositions: true` raises `TypeError`, violating the fail-soft contract that malformed register data degrades to `[]` and blocks WARNs strictly.  
**Fix direction:** Validate `dispositions` is a list before iterating; otherwise return `[]`.

## MEDIUM

(none)

## LOW

(none)
