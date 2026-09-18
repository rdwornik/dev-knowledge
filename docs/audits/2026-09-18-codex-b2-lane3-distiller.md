# Codex Review — b2-lane3-distiller

**Date:** 2026-09-18
**Branch:** `worktree-agent-a773b70aa95731525`
**HEAD:** `b7d930cf`
**Diff range:** `main..worktree-agent-a773b70aa95731525`
**Codex version:** codex-cli 0.153.4
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

## [HIGH] scripts/gen_lane_contract.py:1980 — Caller-supplied `--kind` can contradict the BUILD-LIST row

**What:** The command accepts any enum-valid `--kind` even when it differs from `row.delta`; the emitted contract combines that new verb with the row’s prior-art/removal data and labels the conflict “not a defect.”  
**Why:** This permits an unrecorded reclassification of a frozen build-list decision, potentially dispatching a lane with an internally inconsistent or destructive scope.  
**Fix direction:** Derive the delta from the matched row, or refuse mismatches until the BUILD-LIST row is formally updated.

## [HIGH] scripts/gen_lane_contract.py:1603 — Unreadable persisted graph aborts distillation

**What:** `open_store()` exceptions (corrupt, incompatible, or inaccessible SQLite store) are not handled; only a missing file degrades to a reported gap.  
**Why:** A present-but-unreadable graph causes the CLI to fail instead of producing the otherwise valid contract with dependency resolution marked unavailable.  
**Fix direction:** Handle the graph store’s read/open errors and emit the same explicit unresolved-dependencies state used for an absent store.

## Medium

(none)

## Low

(none)