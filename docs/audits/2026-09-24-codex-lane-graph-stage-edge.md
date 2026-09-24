# Codex Review — lane-graph-stage-edge

**Date:** 2026-09-24
**Branch:** `worktree-lane-graph-stage-edge`
**HEAD:** `263822c1`
**Diff range:** `main..worktree-lane-graph-stage-edge`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- New EDGE_TRIGGERS edges from ecosystem/harness.yaml stages/moments to the scripts they run (scripts/file_purpose_graph.py: WIRING_SURFACES addition + _harness_command_targets).
- The false-positive guard: _harness_command_targets must read only stages[].command and moments[].organs[].command, never the fates: section (which records scripts NOT yet run).
- ORPHAN_DISPOSITIONS cleanup in scripts/graph_queries.py: four rows discharged (merge_receipt.py, actions_verdict.py, review_packet.py, single_flight.py) because they are now genuinely triggered.
- tests/test_graph_spine.py: new harness_repo fixture + 3 new tests, retirement of one stale disagreement test.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/file_purpose_graph.py:725 — Inline harness commands do not create trigger edges

**What:** `_harness_command_targets()` only resolves literal path/module command arguments; it misses `python -c` commands that import and run a script, such as `fleet_health` in the `lane-end` moment.  
**Why:** The graph silently omits a real `ecosystem/harness.yaml -> scripts/fleet_health.py` trigger edge, making its process/wiring view incomplete.  
**Fix direction:** Parse Python `-c` payloads for imports using the same module-resolution rules as the script import pass, and add a regression test for an inline-command target.

## MEDIUM

(none)

## LOW

(none)