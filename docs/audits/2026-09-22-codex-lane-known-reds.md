# Codex Review — lane-known-reds

**Date:** 2026-09-22
**Branch:** `worktree-lane-known-reds`
**HEAD:** `af701a47`
**Diff range:** `main..worktree-lane-known-reds`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0
**Consumer:** W4-1, row `[#937]` (`to-cc/DECLARE-WAVE4A-2026-09-22.md` goal G1 -- median integrator time per lane <= 15 min after this lane merges); the tool's own consumer is the integrator's per-lane pairing step (`record-base` once per batch, `compare` per lane); no-consumer: a lane review record, not a governance surface.

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- lane-known-reds (W4-1, R-W4-2): scripts/test_pairing.py gains a batch registry (record-base once, compare each lane against it) and scripts/preflight_contract.py stops silently dropping an all-digit short sha. Tests in tests/test_test_pairing.py and tests/test_preflight_contract.py.
- Attribution correctness: can a lane's red be classified as pre-existing (or a pre-existing one as the lane's) by the registry logic? Check _was_in_registry, the base_flakes path, the collection-error id path, and compare() when the selection is empty or declined.
- The skip-count guard (skip_guard, RunResult, collection-level skips in the plugin): can a lane hide a red behind a skip, xfail or importorskip without the guard refusing? Is cutting both sides to the files both runs covered sound?
- Registry home and write-once: written only under the receipts home, undated name, batch name validated as a filename, --replace the only overwrite. Any path traversal or half-written registry?
- Existing two-commit CLI (BASE HEAD / --lane) must be unchanged; read_events must keep returning PASSED/FAILED/ERROR only.
- preflight_contract.py: an all-digit token that is no commit now FAILS visibly; is that acceptable for counts in backticks, and is any other place still dropping a sha class?

---

## Findings
## Critical

(none)

## High

### scripts/test_pairing.py:629 — Skip guard accepts skip substitutions with the same count

**What:** `skip_guard()` only compares skip counts, so a lane can turn one previously runnable/red test into `skip`/xfail/importorskip while making a different baseline-skipped test runnable; equal counts yield `match`.  
**Why:** The verdict can be `CLEAN` while a red was hidden, defeating attribution.  
**Fix direction:** Treat changes to the set of skipped IDs—not just its cardinality—as unattributable.

### scripts/test_pairing.py:629 — Skips in tests outside the registry are ignored

**What:** The guard discards all skipped IDs whose files are not in `registry.files`; `compare()` still permits a clean verdict for `selection.outside_registry`.  
**Why:** A lane can select an existing but unrecorded test file and hide its base red behind a skip without triggering `UNATTRIBUTABLE`.  
**Fix direction:** Refuse attribution when selected files fall outside registry coverage, or explicitly run/record an equivalent baseline before comparing.

### scripts/test_pairing.py:563 — “Write once” registry creation has a TOCTOU race

**What:** Existence is checked before the run, then `write_registry()` unconditionally uses `os.replace`, so concurrent `record-base` invocations can overwrite each other without `--replace`.  
**Why:** This can launder or replace the batch baseline and violate the registry’s write-once guarantee; the shared `.tmp` name also allows writers to interfere.  
**Fix direction:** Use an atomic exclusive-create/lock protocol and unique temporary names; permit replacement only through the explicit `--replace` path.

## Medium

(none)

## Low

(none)
---

## Disposition (lane-known-reds, after the review)

All three HIGH findings were accepted and fixed in the commit that carries this record; each has a
test written first and seen red (`tests/test_test_pairing.py`, section "the codex terra review's three
HIGH findings").

- **`skip_guard` compares only counts (test_pairing.py:629) -- FIXED.** A skip the registry lacked is a
  mismatch even when the count is level (`test_swapping_which_test_is_skipped_keeps_the_count_...`).
  A different count is still a mismatch, so the contract's literal rule is a subset of the new one.
- **Skips in files outside the registry ignored (test_pairing.py:629) -- FIXED, by refusal.** A selected
  file the registry never ran that already existed on the base has an unknown baseline; the comparison is
  `UNATTRIBUTABLE` with `unregistered` naming it (`test_a_selected_file_that_existed_on_the_base_...`).
  A file the lane added is not affected (`test_a_file_the_lane_added_is_not_unregistered_...`).
- **Write-once TOCTOU (test_pairing.py:563) -- FIXED.** `write_registry` creates exclusively (hard link
  fails if the name exists), uses a per-writer temp name and always removes it
  (`test_write_registry_never_replaces_an_existing_registry_unless_told_to`). The pre-run existence check
  stays as the early, cheap refusal.
