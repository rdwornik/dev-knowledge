# Codex Review — lane-na-gates

**Date:** 2026-08-27
**Branch:** `worktree-lane-na-gates`
**HEAD:** `f8ae0f6d`
**Diff range:** `main..worktree-lane-na-gates`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Four new audit checks + their detector modules: validate_substrate.py, dispatch_drift.py, consumer_at_landing.py, proof_layer.py, and the four audit_checks/check_*.py adapters.
- Correctness of the regex/AST predicates: false-positive and false-negative behaviour on real inputs, boundary handling, fence/indentation handling.
- Whether any check can report a non-failing status while having evaluated nothing (green-by-skip), including on error paths.
- Baseline/ratchet integrity: identity keying, duplicate handling, count-vs-list agreement, detector_id commensurability.
- Registration coupling: ALL_CHECKS, audit_checks/registry.py CHECK_ORDER ordering, doc-code-edge.yaml exempt entries.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/consumer_at_landing.py:237 — Partial governance-pool reads can pass as fully resolved

**What:** Unreadable pool files are silently skipped, while `pool_resolved` is later set true whenever any pool file exists.  
**Why:** The ratchet can emit a clean result after scanning only part of the governance pool, violating its fail-loud “citations cannot be resolved” contract.  
**Fix direction:** Track read failures and mark the pool unresolved (or fail) when any required pool file cannot be read; add a mixed readable/unreadable fixture.

### scripts/consumer_at_landing.py:260 — Nested audit artifacts are outside both landing and consumption checks

**What:** The corpus uses `audits_dir.glob("*.md")`, excluding Markdown files below `docs/audits/*/`.  
**Why:** A newly landed nested artifact can omit its consumer declaration and grow the unconsumed set without being measured, while the check still passes.  
**Fix direction:** Traverse the intended audit-artifact tree recursively, with explicit exclusions for generated indexes and non-artifact subtrees.

### scripts/proof_layer.py:349 — Common named `skipif` decorators are not detected

**What:** Function scanning only recognizes decorators that are direct `pytest.mark.skipif(...)` calls; a named marker such as `requires_git = pytest.mark.skipif(...)` followed by `@requires_git` is ignored.  
**Why:** This repository already uses that form extensively, so environment-gated enforcement tests can remain absent from the baseline and the proof-layer check can report no regression.  
**Fix direction:** Resolve decorator names through module-level assignments/marker aliases, and cover named decorators (and class-level markers) in the AST tests.

### scripts/journal_anchor.py:153 — Removes the batched ancestry lookup and restores per-entry Git subprocesses

**What:** `introduced()` now invokes two `git rev-list` calls per uncached spine entry; the removed parent-map implementation performed one graph read for the spine.  
**Why:** `check_journal_spine_anchor` walks hundreds of entries during audit/ship-gate runs, so this reintroduces the previously measured minutes-scale hook slowdown.  
**Fix direction:** Retain a bounded batched parent-map/cache implementation, with parity tests against Git’s `first-parent..sha` result.

## MEDIUM

(none)

## LOW

(none)