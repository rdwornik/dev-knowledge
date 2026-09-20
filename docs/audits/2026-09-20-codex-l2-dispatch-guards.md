# Codex Review — l2-dispatch-guards

**Date:** 2026-09-20
**Branch:** `worktree-lane-l2-dispatch-guards`
**HEAD:** `fa57d00d`
**Diff range:** `main..worktree-lane-l2-dispatch-guards`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/worktree_occupancy.py: does each of the four legs (registered worktree, directory, worktree-<slug> branch, busy session cwd) fire correctly and independently? Any false FREE (a tree that is taken) or way it mutates state; Windows path/case handling; the fail-closed exit 2 when a leg cannot be read.
- scripts/validate_branch_naming.py is_worktree_lane_name/classify: does worktree-lane-<slug> (hyphenated) admit loop-eval, l2-dispatch-guards, the generator's date-kind-subject shape, and the batch form, while refusing main, claude/x, automation/fleet-audit, worktree-lane- and malformed batch names? Any way the widening admits a native worktree or changes LANE_BRANCH_RE callers.
- tests: RED-first honesty; vacuous assertions; the two test_batch_manifest.py seed edits.

---

## Findings
## Critical

(none)

## High

### scripts/worktree_occupancy.py:146 — Relative `--repo-root` can miss registered worktree and session legs

**What:** `tree` is normalized without resolving it to an absolute path, while Git and agent CWDs normally report absolute paths.  
**Why:** With `--repo-root .`, a detached/prunable registered worktree or session-only occupancy can be reported FREE.  
**Fix direction:** Canonicalize the root/target path before all four leg comparisons; add relative-root tests for registered-worktree and session-only cases.

### scripts/worktree_occupancy.py:152 — Unreadable directory can be treated as clear

**What:** `Path.exists()` is used as the directory leg without converting filesystem-access failures to `OccupancyError`.  
**Why:** An inaccessible unregistered husk can become a false FREE instead of the required fail-closed exit 2.  
**Fix direction:** Perform the directory probe with explicit error handling that raises `OccupancyError` on an unreadable path; test that failure path.

### scripts/worktree_occupancy.py:128 — Invalid/incomplete session data does not fail closed

**What:** Missing `cwd`/`status` fields are interpreted as “not held,” while non-mapping list entries crash at line 154 rather than producing exit 2.  
**Why:** A changed or malformed `claude agents --json` payload can silently clear the session leg or bypass the documented failure contract.  
**Fix direction:** Validate the sessions payload and each record before evaluation, raising `OccupancyError` for unreadable/incomplete records; apply the same validation to `--sessions-file`.

### scripts/validate_branch_naming.py:229 — Truncated malformed batch names are admitted as general lanes

**What:** `_BATCH_SHAPED_RE` requires a trailing hyphen, so names such as `worktree-lane-a-505` and `worktree-lane-abcd-505` bypass the malformed-batch guard and classify as lanes.  
**Why:** These formerly invalid batch-shaped branches enter `is_lane_branch` and can receive the open-batch journal exemption.  
**Fix direction:** Route all ambiguous `<letters>-<digits>` lane slugs through batch-shape validation, including incomplete forms; add negative cases for both valid-width and over-width truncated tokens.

## Medium

(none)

## Low

(none)

---

## Dispositions (lane-l2-dispatch-guards, same session)

All three HIGH fixed. Each has its RED test committed BEFORE the fix (commit `c0e052ed`; 10 tests
red on that commit, witnessed by run), then the fix.

- **HIGH 1 — unreadable directory reads FREE: FIXED.** `_dir_exists` uses `os.stat`; only
  `FileNotFoundError` is "absent", every other `OSError` raises `OccupancyError` (exit 2).
  Test: `test_an_unreadable_directory_fails_closed_rather_than_reading_free`.
- **HIGH 2 — malformed session data does not fail closed: FIXED.** `_validated_sessions` runs in
  `check()`, so it covers the live read AND `--sessions-file`. A non-list payload, a non-mapping
  row, a row with no string `status`, or a `busy` row with no string `cwd` raises. A non-busy row
  with no `cwd` is accepted (it cannot hold a tree). Tests: `test_a_malformed_session_record_fails_closed`
  (5 cases), `test_a_non_busy_session_without_a_cwd_is_harmless`,
  `test_the_cli_applies_the_same_validation_to_a_sessions_file`. Live `claude agents --json` still
  parses (checked against the real list).
- **HIGH 3 — truncated batch names admitted as general lanes: FIXED.** Any slug shaped
  `<letters>-<digits>` followed by `-` or end is judged by `LANE_BRANCH_RE` alone. Tests:
  `test_a_truncated_batch_shape_is_not_absorbed_by_the_general_form` (`a-505`, `abcd-505`,
  `ab-808`). **Trade-off, recorded:** a genuinely intended lane slug that happens to open
  `<letters>-<digits>-…` (e.g. `phase-2-cleanup`) is now refused as a malformed batch name. That
  follows from keeping the standing `abcd-505-slug` refusal and cannot be told apart from it.