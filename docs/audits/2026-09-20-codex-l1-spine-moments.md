# Codex Review — l1-spine-moments

**Date:** 2026-09-20
**Branch:** `worktree-lane-l1-spine-moments`
**HEAD:** `b5e51388`
**Diff range:** `main..worktree-lane-l1-spine-moments`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/dodo.py: receipt-as-target resume. Is 'up to date' ever true when it should not be (stale upstream, always rows, partial receipts, failed runs)?
- scripts/telemetry_emit.py wrap: backwards compatibility of the hook wrapper, atomic receipt write, stdout capture/echo, exit-code propagation.
- ecosystem/harness.yaml moments: schema, placeholder resolution, SKIPPED-NOT-BUILT / SKIPPED-NO-INPUT handling, DECLARE N3 (no cap may stop a task).
- tests/test_spine_moments.py: do the RED-first tests really fail without the change; any vacuous assertions.

---

## Findings
## CRITICAL

(none)

## HIGH

### scripts/dodo.py:130 — Receipt freshness ignores the files and live data a command reads

**What:** The input hash covers environment values, argv text, and prior hash only; it does not fingerprint `{contract}` contents or command inputs such as `protocols/BUILD-LIST.md`.  
**Why:** Editing a contract in place leaves stages 7/11 “up to date”; likewise, changed upstream git/file data can leave a prior stage and all downstream receipts falsely current.  
**Fix direction:** Include declared input content/state fingerprints in freshness, or mark live-input tasks as always-run.

### scripts/dodo.py:145 — A syntactically valid partial receipt is accepted as completed

**What:** `_fresh()` accepts any JSON object with `status: ok`, `exit_code: 0`, and a matching hash; it does not validate schema, expected organ, duration, or required receipt fields.  
**Why:** A partial/legacy/corrupted-but-parseable receipt can suppress execution even though it is not a usable completion record.  
**Fix direction:** Validate the complete receipt schema and task identity before treating a target as fresh.

### scripts/dodo.py:181 — Optional `command: null` organs crash before they can be skipped

**What:** The freshness callback invokes `_argv(row["command"])` before `_execute()` reaches its absent-command skip branch.  
**Why:** An optional not-yet-built organ represented by `command: null` raises during up-to-date evaluation instead of writing `SKIPPED-NOT-BUILT`, defeating N4 handling.  
**Fix direction:** Classify null/missing commands before freshness evaluation and make them unconditionally stale so the skip action writes its receipt.

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (lane-l1-spine-moments, same session)

- **HIGH 1 (freshness ignores what a command reads) -- ACCEPTED, fixed.** The input hash now carries the content
  hash of every argv token that names a file, plus a HEAD + porcelain-status fingerprint, so a commit or an edit
  stales every receipt. Tests added WITH the fix (their red state was not witnessed separately): `test_an_in_place_edit_of_a_file_a_stage_names_invalidates_its_receipt`,
  `test_the_repo_state_fingerprint_is_part_of_the_input_hash`. Stated limit: a receipt is a resume record for one
  preparation, not a cache across repo changes.
- **HIGH 2 (partial receipt accepted) -- ACCEPTED, fixed.** `_fresh` requires every schema key, `organ == label`,
  `status ok`, `exit_code 0`, integer duration. `test_a_parseable_but_incomplete_receipt_is_not_up_to_date`,
  `test_a_receipt_written_for_another_organ_is_not_up_to_date`.
- **HIGH 3 (`command: null` crashes freshness) -- ACCEPTED, fixed.** A row with no command is never fresh; its action
  writes the SKIPPED receipt. `test_an_optional_organ_with_command_null_is_skipped_not_crashed`.