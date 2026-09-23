# Codex Review — lane-hooks-urgent

**Date:** 2026-09-24
**Branch:** `worktree-lane-hooks-urgent`
**HEAD:** `5b4e4bbe`
**Diff range:** `main..worktree-lane-hooks-urgent`
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

## scripts/telemetry_emit.py:359 — Legacy databases without `run_id` are silently excluded from migration

**What:** The source query always selects `run_id`, although older stores may not have that column.  
**Why:** The query error is converted to zero copied rows after the legacy DB is renamed, so historical counters disappear from the active shared store.  
**Fix direction:** Migrate or inspect the source schema before selecting rows, supplying the legacy default for absent columns.

## scripts/telemetry_emit.py:578 — Migration failures are silently swallowed

**What:** `default_db_path()` catches every exception from migration and does nothing.  
**Why:** A failed migration can leave the renamed legacy DB unimported while callers proceed with an apparently healthy empty shared store.  
**Fix direction:** Catch only expected recoverable failures and emit an actionable warning or preserve a retryable migration state.

## HIGH

## scripts/hook_expiry_verdict.py:113 — Failed hook launches can be classified as REMOVE candidates

**What:** Only `block` outcomes are counted; `error` outcomes are treated as clean runs.  
**Why:** A hook whose wrapper repeatedly fails to launch can reach a zero-block REMOVE verdict despite never executing successfully.  
**Fix direction:** Treat errors as unmeasured/error evidence that prevents a REMOVE verdict, with a failed-launch test.

## MEDIUM

(none)

## LOW

(none)