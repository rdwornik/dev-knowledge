# Codex Review — lane-decide-command

**Date:** 2026-09-28
**Branch:** `worktree-lane-decide-command`
**HEAD:** `a2ca5043`
**Diff range:** `origin/main..HEAD`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/4/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** `LANE-5B4-12-decide-command.md` (this lane's own frozen contract)
**Disposition:** all 4 High findings **fixed** in the same commit as this record, each with a
RED-first regression test in `tests/test_decide_checks.py` (`test_matrix_ignores_a_later_
unrelated_table`, `test_response_coverage_flags_two_distinct_findings_sharing_one_id`,
`test_run_probe_refuses_*` ×3, `test_run_probe_rejects_line_zero_as_a_locator`). A second,
correctly-scoped run after the fixes found nothing new to re-check (fixes verified by the new
tests, not by a third Codex pass, per common rules' Codex-usage economy).

---

## Focus

(none specified)

---

## Findings
## Critical

(none)

## High

### scripts/decide_checks.py:167 — Matrix parser consumes later, unrelated tables

**What:** It treats every Markdown table after the matrix header as a matrix row.  
**Why:** A later response/evidence table can cause an index error (exit 2) or false matrix defects.  
**Fix direction:** Stop parsing at the end of the contiguous matrix table and validate row width.

### scripts/decide_checks.py:265 — Duplicate evaluator finding IDs are silently collapsed

**What:** Finding IDs are collected in a `set`, so two distinct evaluator findings sharing an ID become one.  
**Why:** One response row can incorrectly satisfy both findings, yielding a clean coverage result.  
**Fix direction:** Track finding IDs with source/count and report duplicate IDs before coverage checking.

### scripts/decide_checks.py:382 — Probe paths can escape the repository

**What:** `grep` probes join an unchecked user-supplied path to `repo_root`; absolute and `..` paths can target external files.  
**Why:** A subagent-authored evidence file can use the gate to probe sensitive local files outside the decision repository.  
**Fix direction:** Resolve probe paths and reject any path outside the resolved repository root.

### scripts/decide_checks.py:399 — `path:0` is accepted as a valid locator

**What:** The line probe only checks `n_lines >= line_no`, so line zero passes for any existing file.  
**Why:** An invalid source locator can falsely verify a subagent claim.  
**Fix direction:** Require line numbers to be at least 1 before accepting the probe.

## Medium

(none)

## Low

(none)