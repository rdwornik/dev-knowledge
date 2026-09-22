# Codex Review — lane-landing-decisions

**Date:** 2026-09-22
**Branch:** `worktree-lane-landing-decisions`
**HEAD:** `e4ea8a2f`
**Diff range:** `main..worktree-lane-landing-decisions`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Landed 7 in-scope transport rulings (DECLARE/AMEND/ANSWER, 2026-09-20..22) into their repo homes: ADR-120 status Accepted, ADR-87 amendment (equilibrium E1-E5), STANDING_RULINGS AJ section, docs/decisions/README index rows
- Filed 13 new task rows (#937-#949) for wave-4b/wave-5 deferred items, one row per item (fair why test merges two source citations into one row)
- Re-pointed carried-by: lines on 7 transport files (H: drive, outside this diff) to their repo homes; left 2 AMEND-HANDOFF-BOOT-* files OPEN as out-of-scope (HANDOFF_BOOT.md not in this lane's owned files, and its byte budget had no headroom)
- Verify: every landed: predicate this lane added resolves TRUE; ratchet/ADR-status/task-tree/landing-predicate tests pass; audit.py health is OK; no ruling was reworded, only cited and located
- Consumer for this review: LANE-W4-5-landing-decisions.md Done-contract item 8

---

## Findings
## Critical

### [CRITICAL] tasks/manifest.json:681 — Reuses existing task IDs 937–941

**What:** The manifest remaps IDs 937–941 from their existing Wave-4a task records to unrelated new task files.  
**Why:** `tasks/manifest.json` is the backlog source of truth, so this drops five existing deferred work items during generation.  
**Fix direction:** Preserve the existing 937–941 mappings and assign unused IDs to the new rows.

## High

### [HIGH] scripts/test_pairing.py:410 — Removes batch-registry command support

**What:** `main()` no longer dispatches `record-base` or `compare`; the associated registry, skip-guard, and unattributable-result implementation were removed.  
**Why:** Batch consumers can no longer perform the required one-base-run comparison, and lanes can again be attributed despite skip-based masking.  
**Fix direction:** Retain the registry command path and its fail-closed skip/unregistered-test guards.

### [HIGH] scripts/preflight_contract.py:371 — All-digit short SHAs are silently ignored

**What:** The new `sha.isdigit()` branch skips an otherwise valid 7–40 character SHA locator.  
**Why:** A contract containing an all-digit short commit ID can report clean without validating that locator.  
**Fix direction:** Validate all SHA-shaped tokens and report unresolved all-digit tokens explicitly.

## Medium

(not assessed — diff review scope is Critical/High.)

## Low

(not assessed — diff review scope is Critical/High.)