# Codex Review — b2w2-main-comparable

**Date:** 2026-10-09
**Branch:** `worktree-b2w2-main-comparable`
**HEAD:** `7bfc4a73`
**Diff range:** `origin/main...HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/0/0/0

**Model used:** `gpt-6-astra` (pinned; both lanes — [#469])
**Served model (tool log):** `gpt-6-astra`, session `01a121cd-c1de-7b71-a928-5f83204eba33` (codex run.err lines 4 and 10)
**Review profile:** code
**Consumer:** LANE-1441-b2w2-main-comparable Done-contract item 6 ([#1441])

---

## Focus

Contract: LANE-1441-b2w2-main-comparable (Done-contract items 1-5; Do-not list: no registry entry other than the 40 expired [#912] entries changed; no weakened assertion, skip or exclusion; graph_queries.py touched only by one EDGE_COMPUTATIONS entry and one ORPHAN_DISPOSITIONS entry for scripts/decision_carriage.py). Attack: (a) is the not-an-edge verdict for decision_carriage.py honest, vs private; (b) are the refs clauses in tasks/1425-1437 real provenance; (c) did the 40-entry re-date change anything else in logs/KNOWN-REDS-REGISTRY.json. Return exactly this nonce NONCE-3362aa59bc80 and the sha256 prefix 6e2b7cdaf67f of 'git diff origin/main...HEAD' in your answer.


---

## Findings
## Critical

(none)

## High

(none)

## Medium

(none)

## Low

(none)

Verified: only the 40 authorized registry entries changed; graph edits match scope; the transport exclusion supports `not-an-edge`; refs resolve; the test adjustment matches R78’s documented succession.

Tests and CI were not run during this read-only review.

NONCE-3362aa59bc80  
Verified diff SHA-256 prefix: `6e2b7cdaf67f`