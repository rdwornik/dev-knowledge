# Codex Review — lane-adr122-accept

**Date:** 2026-09-25
**Branch:** `worktree-lane-adr122-accept`
**HEAD:** `02e63686`
**Diff range:** `main..worktree-lane-adr122-accept`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/4/0/0 <!-- Critical/High/Medium/Low. Fixed in the follow-up commit: the Critical (tasks/ write refusal on new/set/close) and three of four High (converter clause-loss into legacy_body, clean CLI exception handling, write-path test coverage). ONE High recorded, not fixed: `close` does not execute a CommandVerifier or collect ReviewVerifier evidence before citing a closure -- documented as an honest step-1 limit in _cmd_close's docstring; wiring real evidence collection in front of `close` is step 2's job (the closure sweep, D4). -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- ADR-122 status flip to Accepted + amendment section (diff scoped to only those two changes)
- protocols/STANDING_RULINGS.md new section AM (R1-R7)
- scripts/task_record.py: the ADR-122 D1-D9 pydantic model, converter (convert_row/convert_archive_record), and CLI (new/set/show/list/check/close) -- do NOT flip the source of truth, never writes into tasks/
- tests/test_task_record.py RED-first coverage
- three new task rows 1076-1080 under tasks/, manifest.json wiring
- ecosystem/harness.yaml new fates: line for scripts/task_record.py

---

## Findings
## CRITICAL

## [CRITICAL] scripts/task_record.py:410 — Scratch CLI can write into `tasks/`

**What:** `new`, `set`, and `close` accept any `--record` path, including paths under `tasks/`.  
**Why:** This directly violates ADR-122 step 1’s “never writes into `tasks/`” boundary and can mutate the current source of truth.  
**Fix direction:** Resolve and reject any output path within the repository’s `tasks/` tree before every write.

## HIGH

## [HIGH] scripts/task_record.py:190 — Closing does not require evidence that criteria passed

**What:** A `CommandVerifier` or `ReviewVerifier` makes a criterion closable solely by type; `close` writes only commit/digest metadata and neither executes nor records criterion results.  
**Why:** A record with a failing command (for example `false`) can be closed as though its acceptance criteria were met.  
**Fix direction:** Require per-criterion, verifiable closure evidence and refuse close when it is absent or failing.

## [HIGH] scripts/task_record.py:316 — Converter silently drops supported and unknown row clauses

**What:** `convert_row` extracts only a limited clause set; fields such as `routine`, `supersedes`, provenance, and other unrecognised clauses are neither populated nor retained in `legacy_body`.  
**Why:** The reconciliation output can silently lose source-row data while reporting no remaining legacy carrier.  
**Fix direction:** Parse every supported clause and preserve all unclassified remainder verbatim for measurement/refusal.

## [HIGH] scripts/task_record.py:393 — Malformed CLI inputs escape instead of being refused cleanly

**What:** JSON/file reads occur outside the validation handlers in `check`, `set`, `close`, and `list`; the handlers also use broad `except Exception`.  
**Why:** Invalid JSON, unreadable files, and implementation faults produce tracebacks or get masked rather than a reliable CLI refusal result.  
**Fix direction:** Handle expected `OSError`, `JSONDecodeError`, and validation errors explicitly across each command boundary.

## [HIGH] tests/test_task_record.py:231 — Write-path and exclusion behavior have no coverage

**What:** Tests cover `show` and `check`, but not `new`, `set`, `close`, `list`, malformed CLI inputs, or the required refusal to write beneath `tasks/`.  
**Why:** The untested write surface allowed the source-of-truth boundary violation above to land.  
**Fix direction:** Add focused tests for every CLI subcommand, especially `tasks/` path refusal and no-write-on-invalid-input behavior.

## MEDIUM

(none)

## LOW

(none)