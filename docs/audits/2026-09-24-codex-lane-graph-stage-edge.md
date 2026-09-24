# Codex Review — lane-graph-stage-edge

**Date:** 2026-09-24
**Branch:** `worktree-lane-graph-stage-edge`
**HEAD:** `263822c1`
**Diff range:** `main..worktree-lane-graph-stage-edge`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. The 1 HIGH finding fixed in 366661fd (pre-authorized ruling 2(e): fix a Codex review's P1 findings). -->
**Disposition:** the 1 HIGH finding FIXED (pre-authorized ruling 2(e)). Re-verified with a
RED-first regression test (`test_harness_dash_c_snippet_organ_triggers_its_import`) confirmed
red before the fix and green after; see `to-browser/SESSION-lane-graph-stage-edge.md`.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

no-consumer: this lane files no BACKLOG row of its own for this finding tonight -- it is
disposed against the frozen contract directly (below), the same shape
`2026-09-24-codex-lane-ci-verdict.md`'s own no-consumer line uses.

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

---

## Dispositions (2026-09-24)

The 1 HIGH finding was genuine and fixed in the same session, follow-up commit `366661fd`
("resolve python -c snippet imports in harness moment organs"):

1. **HIGH, file_purpose_graph.py:725, `-c` snippet organs contributed no trigger edge.**
   `_dash_c_targets` now resolves a `python -c "..."` organ's `import <module>` (after
   `sys.path.insert(0, 'scripts')`) the same way `graph_queries._snippet_scripts` already
   resolves it reading the same file for the moments query. No live orphan-census change:
   `scripts/fleet_health.py` is already wired via `.claude/settings.json`, so this closes a
   real completeness gap in the graph's view of `ecosystem/harness.yaml`, not a census
   regression.

See `to-browser/SESSION-lane-graph-stage-edge.md` for the per-finding detail.

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-24-codex-lane-graph-stage-edge.md | ACTIONED | 366661fd |