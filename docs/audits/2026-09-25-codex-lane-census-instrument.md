# Codex Review — lane-census-instrument

**Date:** 2026-09-25
**Branch:** `worktree-lane-census-instrument`
**HEAD:** `5dc84cde`
**Diff range:** `2b5a4ef8..worktree-lane-census-instrument`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/0/0/1 <!-- Critical/High/Medium/Low. -->

**Disposition:** the one LOW finding (rendered reachability label omitted the harness.yaml
moment source) fixed in a follow-up commit on this branch — see the `render_census` and
`process_census` docstring text now naming "a harness.yaml moment" alongside hooks/CI/imports.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Consumer: lane contract `LANE-5B-10-census-instrument.md` (Wave 5b, batch WAVE5B-N1) — "a
trustworthy census of what runs". Diff range pinned to `2b5a4ef8` (this lane's own sync point
with `origin/main`, per F2) rather than local `main`, which was stale relative to `origin/main`
by 15 commits at review time; using local `main` swept in unrelated merged lanes' files.
Changes: `tests/test_organ_usage_metric.py` gains a fifth `wired_repo` fixture process reachable
only through an `ecosystem/harness.yaml` moment declaration (not a hook/CI/import), plus a
dedicated test and three touched-up assertions; `scripts/organ_usage_metric.py` gets two
docstring clarifications (no behavioural change) naming the moment declaration as a third
reachability source. No new dependency, no new module.

---

## Findings
## Critical

(none)

## High

(none)

## Medium

(none)

## Low

## [LOW] scripts/organ_usage_metric.py:573 — Rendered reachability label omits harness declarations

**What:** The census output still says reachability comes from “a hook, CI or import chain,” excluding the newly documented `ecosystem/harness.yaml` stage/moment source.  
**Why:** Readers of the report receive an incomplete explanation of why a process is `REACHABLE-BUT-UNOBSERVED`.  
**Fix direction:** Include harness stage/moment declarations in the rendered reachability description.