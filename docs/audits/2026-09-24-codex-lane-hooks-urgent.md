# Codex Review — lane-hooks-urgent

**Date:** 2026-09-24
**Branch:** `worktree-lane-hooks-urgent`
**HEAD:** `5b4e4bbe`
**Diff range:** `main..worktree-lane-hooks-urgent`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 2/1/0/0 <!-- Critical/High/Medium/Low, as raised in Findings below. Disposition (all three fixed, commit e87fb7eb) is recorded in the Dispositions section, not folded into this count. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

(none specified)

---

## Findings
## CRITICAL

## scripts/telemetry_emit.py:359 — Legacy databases without `run_id` are silently excluded from migration

**What:** The source query always selects `run_id`, although older stores may not have that column.  
**Why:** The query error is converted to zero copied rows after the legacy DB is renamed, so historical counters disappear from the active shared store.  
**Fix direction:** Migrate or inspect the source schema before selecting rows, supplying the legacy default for absent columns.

## scripts/telemetry_emit.py:578 — Migration failures are silently swallowed

**What:** `default_db_path()` catches every exception from migration and does nothing.  
**Why:** A failed migration can leave the renamed legacy DB unimported while callers proceed with an apparently healthy empty shared store.  
**Fix direction:** Catch only expected recoverable failures and emit an actionable warning or preserve a retryable migration state.

## HIGH

## scripts/hook_expiry_verdict.py:113 — Failed hook launches can be classified as REMOVE candidates

**What:** Only `block` outcomes are counted; `error` outcomes are treated as clean runs.  
**Why:** A hook whose wrapper repeatedly fails to launch can reach a zero-block REMOVE verdict despite never executing successfully.  
**Fix direction:** Treat errors as unmeasured/error evidence that prevents a REMOVE verdict, with a failed-launch test.

## MEDIUM

(none)

## LOW

(none)

---

## Dispositions (LANE-5A-7, 2026-09-24)

**All three findings were genuine and are fixed (commit `e87fb7eb`).**

- **CRITICAL, `telemetry_emit.py:359`.** Confirmed: `_copy_rows` migrated only the destination
  connection's schema (`d`), then read the source connection (`s`) with a SELECT naming `run_id`
  explicitly. A legacy per-checkout store written before the `run_id` column existed ([#565])
  has no such column, so the SELECT raised `sqlite3.OperationalError`, caught by the existing
  `except sqlite3.Error: return 0` -- every row in the file silently discarded rather than
  migrated. **Fixed:** `_copy_rows` now runs `s.execute(SCHEMA); _migrate(s)` on the source
  connection before the SELECT, exactly mirroring what it already does for the destination.
  Regression test: `test_legacy_store_predating_run_id_column_still_migrates` builds a real
  pre-run_id-column SQLite file by hand and asserts the row survives migration.
- **CRITICAL, `telemetry_emit.py:578` (pre-fix line; `default_db_path()`).** Confirmed: the
  `except Exception: pass` around `migrate_legacy_checkout_store()` left a failed migration with
  no observable trace at all. **Fixed:** the swallow is unchanged in behavior (a migration defect
  still must never raise or block the hook resolving its store path -- that contract is
  intentional, see the function's docstring), but it now prints one line to stderr naming the
  exception, so a failed migration is diagnosable rather than fully invisible.
- **HIGH, `hook_expiry_verdict.py:113`.** Confirmed: `verdict_for` counted every row with
  `runs = len(rows)` but only `outcome == "block"` rows toward `blocks`, so a hook whose wrapper
  only ever produced `outcome="error"` rows (a launch failure, per `telemetry_emit.py`'s own
  `OUTCOMES = {"pass", "block", "error"}`) would read `blocks == 0` after a full window and reach
  REMOVE -- deleting a hook that never got the chance to check anything, exactly the false-REMOVE
  failure mode this lane's Done-contract item 2 exists to prevent for the zero-runs case. **Fixed:**
  `verdict_for` now tracks `errors` separately; a full window with `blocks == 0` and `errors > 0`
  is UNMEASURED, not REMOVE, while a genuine block still wins over interleaved errors (KEEP).
  Regression tests: `test_full_window_of_launch_errors_and_zero_blocks_is_unmeasured_never_remove`,
  `test_a_genuine_block_still_wins_over_interleaved_errors`.

Re-verified after the fix: `uv run --locked pytest tests/test_telemetry_emit.py
tests/test_hook_expiry_verdict.py -q` -- 58 passed; `uv run --locked ruff check
scripts/telemetry_emit.py scripts/hook_expiry_verdict.py tests/test_telemetry_emit.py
tests/test_hook_expiry_verdict.py` -- clean.