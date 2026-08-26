# Codex Review — w2b-surfaces

**Date:** 2026-08-26
**Branch:** `worktree-w2b-surfaces`
**HEAD:** `be084c91`
**Diff range:** `main...HEAD`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 1/4/0/0 <!-- Critical/High/Medium/Low. Counted from the Findings section below, not from the console (its heuristic has printed 0/0/0/0 against a populated artifact before). Disposition of all five: docs/audits/2026-08-26-technical-w2b-surfaces.md §3 — every one fixed in this lane's HEAD, the contract's bar being >= medium. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- [#589] BACKLOG.md is now a one-line-per-row projection (scripts/gen_task_tree.py render_view/project_row). Look for information loss, and for any consumer still parsing the view for a row BODY.
- scripts/backlog_source.py canonical_text(): the tasks/-vs-BACKLOG.md fallback rule. Is the fallback correct for consumer repos, and does any caller silently get the wrong text?
- The --write projection refusal and its two-signal discriminator (_looks_like_view): false positives (a legitimate full-body import refused) and false negatives (a view imported anyway).
- The two size ceilings in find_incoherences: do they actually fail on re-inflation, and can they be silently undone?
- [#590] .gitattributes merge=ours + arm_hooks.arm_merge_driver + the narrowed audit-index-freshness files: pattern + the generated_artifact_freshness audits-index artifact. Is the guarantee actually preserved, or is there a window where a stale index ships?
- check_backlog_filing now diffs BACKLOG.md AND tasks/ - ordering, double-counting, and the reword case.
- gen_task_tree._cmd_emit_source: the rollback transaction now has an extra refusal path. Is the plan-before-write guarantee still intact?

---

## Findings
## Critical

### scripts/gen_task_tree.py:672 — Projection detection can be bypassed by a valid title

**What:** A generated row whose bold title contains `Done when:` makes `_looks_like_view()` return false.  
**Why:** `--write --force` then imports the generated projection and overwrites the authoritative task bodies, despite the claimed non-overridable protection.  
**Fix direction:** Use an unambiguous generation-owned discriminator or independently validate the projection before allowing any import; do not use arbitrary row text as the body marker.

## High

### scripts/generated_artifact_freshness.py:392 — Same-day stale audit index is reported fresh

**What:** `audits-index` freshness compares only `date` values with a zero-day baseline.  
**Why:** A merge that keeps `ours` drops an incoming audit from the index, but if both commits occur on the same day, staleness is `0` and the ship gate permits the stale index.  
**Fix direction:** Make the ship-time check content/regen based, or compare ordered commits/timestamps rather than calendar days.

### scripts/gen_dashboard.py:373 — Release notes lose `Done when` gains after the projection switch

**What:** Closure history still reads historical `BACKLOG.md` revisions, which are now projected rows without bodies.  
**Why:** Closures after #589 render the fallback “row carried no `Done when:` clause” even when the authoritative task body has one, silently degrading dashboard release notes.  
**Fix direction:** Resolve the removed row’s historical task body from `tasks/` (or persist the gain at closure) before rendering release notes.

### scripts/backlog_source.py:90 — Consumer fallback silently decodes corrupted backlog text

**What:** The no-`tasks/` fallback uses `errors="replace"` while claiming to return `BACKLOG.md` “as-is.”  
**Why:** Invalid UTF-8 can erase or alter body markers; callers such as `routine_consumers` then scan altered text and can pass rather than fail their declared `UnicodeDecodeError` path.  
**Fix direction:** Decode strictly and let callers classify unreadable source as a failure/unavailable condition.

### scripts/gen_task_tree.py:635 — Size ceilings do not enforce a body-free projection

**What:** The checks allow up to 400 bytes per task row and 100 KB total, but do not assert row structure beyond those ceilings.  
**Why:** A renderer can append roughly 150 bytes of body material to every current row—substantially re-inflating the view—while staying under both limits and passing coherence checks.  
**Fix direction:** Add an independent projection-shape invariant for every task row (including the required pointer and prohibited body fields), not only byte ceilings.

## Medium

(none)

## Low

(none)