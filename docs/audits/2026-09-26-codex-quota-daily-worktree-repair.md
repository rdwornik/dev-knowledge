# Codex Review — quota-daily-worktree-repair

**Date:** 2026-09-26
**Branch:** `worktree-lane-wire-quota-distiller`
**HEAD:** `88a7b15d`
**Diff range:** `main..worktree-lane-wire-quota-distiller`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Consumer: to-cc/LANE-5B3-2-wire-quota-distiller.md (frozen contract), repair 1 of 2 named in to-browser/REFUSED-lane-wire-quota-distiller.md
- Scope: scripts/hooks/quota_daily.py (_git_rev_parse, _is_linked_worktree, main() gating) and tests/test_quota_daily.py (new linked-worktree fixtures)
- Check: the linked-worktree detection is correct and fail-direction (False/proceed) on git-detection failure is safe; the new tests actually pin the fixed bug (RED before, GREEN after, verified manually this session)

---

## Findings
## CRITICAL

(none)

## HIGH

**scripts/hooks/quota_daily.py:132 — Git-detection failure proceeds from a linked worktree.**

**What:** If either `git rev-parse` call fails or times out, `_is_linked_worktree()` returns `False`, so `main()` launches the quota worker.  
**Why:** A real linked worktree with unavailable/failed Git detection can still run `quota_watch.py record` and write its divergent tracked ledger, recreating the repaired bug. Skipping is fail-open for SessionStart; performing the write is not safe under uncertainty.  
**Fix direction:** Distinguish “confirmed primary” from “detection failed,” and skip unless the checkout is positively identified as primary; add a test forcing a `rev-parse` failure from a real linked-worktree fixture.

## MEDIUM

(none)

## LOW

(none)