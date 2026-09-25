# Codex Review — lane-plan-lint-grammar

**Date:** 2026-09-25
**Branch:** `worktree-lane-plan-lint-grammar`
**HEAD:** `e254e469`
**Diff range:** `origin/main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low -->

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

## [HIGH] scripts/plan_lint.py:384 — `serialize-group` invents a direction from CLI argument order

**What:** Group members are converted into directed dependencies based solely on input order.  
**Why:** A valid declared `Starts after` dependency opposite that incidental order becomes a false cycle and blocks the plan; reordering CLI arguments changes the result.  
**Fix direction:** Represent serialization as mutual exclusion, or require/parse an explicit stable ordering before creating directed edges.
**Disposition: FIXED**, same lane, follow-up commit. `build_edges` now freezes the Serial/Starts-after edges as `declared_edges` before adding any `serialize-group` edge, and skips a group pair already reachable the other way through `declared_edges` — a declared dependency always wins over the input-order guess, so it can no longer manufacture a cycle. Regression test: `test_serialize_group_never_overrides_a_declared_edge_the_other_way`.

## [HIGH] scripts/plan_lint.py:330 — Alias detection scans `--model` tokens outside the Dispatch command

**What:** Every `--model <value>` occurrence in the whole contract is treated as a Dispatch model.  
**Why:** Documentation, examples, or “do not run” prose containing `--model opus` can produce a false BLOCKING gate result.  
**Fix direction:** Limit `--model` extraction to the `## Dispatch` fenced command block.
**Disposition: FIXED**, same lane, follow-up commit. Added `_DISPATCH_FENCE_RE`, which captures only the code block under the `## Dispatch` heading; `--model` is now extracted from that captured body, not the whole contract text. Regression test: `test_model_alias_ignores_a_dash_dash_model_mention_outside_the_dispatch_fence`.

## Medium

(none)

## Low

(none)