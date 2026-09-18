# Codex Review — b2-lane2-organ-invocations

**Date:** 2026-09-18
**Branch:** `worktree-agent-a987786819e3dd5f1`
**HEAD:** `00604bf9`
**Diff range:** `main..worktree-agent-a987786819e3dd5f1`
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

## HIGH scripts/organ_usage_metric.py:386 — Census misses `python -m` process invocations

**What:** Matching only recognizes a stored slash-path in the command text, so `python -m scripts.codemap.cli` never increments `scripts/codemap/cli.py`.  
**Why:** Module-style execution is an established invocation form in this repo, producing false “UNCALLED” results.  
**Fix direction:** Normalize supported dotted module invocations to their registered process paths before counting.

## HIGH scripts/organ_usage_metric.py:386 — Census treats any `uv` command containing a path as executing that process

**What:** Any interpreter-headed line with a process path increments its count, including non-execution commands such as `uv run ruff check scripts/foo.py`.  
**Why:** The report can silently claim a process was invoked when it was only linted, tested, or otherwise passed as an argument.  
**Fix direction:** Parse command segments and identify the actual executable/script operand for each supported runner before matching.

## HIGH scripts/organ_usage_metric.py:369 — JSON output reports zero counts for explicitly unobservable processes

**What:** `counts` is initialized for every process and returned unchanged, so `census --json` emits `0` for command/skill entries despite labeling them “not observable.”  
**Why:** JSON consumers can interpret those zeroes as non-use, contradicting the census’s stated observability contract.  
**Fix direction:** Exclude unobservable entries from counts or represent their count as an explicit non-numeric/observability state.

## Medium

(none)

## Low

(none)