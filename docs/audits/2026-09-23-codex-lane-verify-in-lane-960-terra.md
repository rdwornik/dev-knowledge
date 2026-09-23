# Codex Review — lane-verify-in-lane-960-terra

> consumer: `[#960]` (this lane's row) — see "Disposition" below for what each finding did to it.

**Date:** 2026-09-23
**Branch:** `worktree-lane-verify-in-lane`
**HEAD:** `e54898e3`
**Diff range:** `main..worktree-lane-verify-in-lane`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low -->

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

### scripts/test_pairing.py:809 — Lane record tests the lane tip, not `origin/main + lane`

**What:** `record_lane()` clones `head_sha` directly, so its pytest run excludes the selected `main_ref` tree.  
**Why:** A record can claim it was run against a particular `origin/main` SHA and be reused while the lane only passed before main’s changes were combined, producing a false-clean integration result.  
**Fix direction:** Test a synthetic merge/rebased tree of `main_ref` plus the lane tip (or refuse when the lane does not already contain `main_ref`) and record the tested tree identity.

### scripts/test_pairing.py:695 — Collection-level skips can bypass the registry skip guard

**What:** The guard considers only added skip IDs that exactly match known node IDs; a module-level/collection skip has a file-level ID and is treated as a harmless new ID.  
**Why:** A lane can skip collection of a registry-covered file containing known red tests, then receive a `CLEAN` verdict instead of `UNATTRIBUTABLE`.  
**Fix direction:** Treat collection/file-level skips for registry-covered files as dangerous when they suppress known nodes, while retaining the exemption for genuinely new test node IDs.

### scripts/impacted_tests.py:589 — Invalid lane/main refs silently select no tests

**What:** `changed_from_lane_diff()` ignores Git’s return code and returns an empty path list on a failed `git diff`.  
**Why:** `select-lane` can report an empty, successful selection when `origin/main` or the lane ref is missing or invalid, silently skipping verification.  
**Fix direction:** Check the subprocess result and raise/report a selection error on Git failure.

## Medium

(none)

## Low

(none)

---

## Disposition — all 3 HIGH CONFIRMED and fixed, same branch

1. **`record_lane` tests the tip, not `origin/main + lane` (test_pairing.py:809).** CONFIRMED
   by reading `record_lane`: `make_clone(repo, head_sha, ...)` never combines `main_sha` into
   the tested tree, so a record keyed to an `origin_main` sha the lane never actually merged
   would be false. Took the "refuse" fix direction over the synthetic-merge one: WAVE4B-COMMON
   rule 1 already requires every lane to `git fetch origin && git merge origin/main`
   periodically, so a synced lane satisfies the new `_is_ancestor(main_sha, head_sha)` check
   trivially, and an unsynced one is refused with a message naming the sync command rather than
   silently recording a claim it never tested. Regression:
   `test_record_lane_refuses_when_the_lane_has_not_merged_main`.
2. **Collection-level skips bypass the skip guard (test_pairing.py:695).** CONFIRMED: a module
   skipped at collection time (`pytest.skip(..., allow_module_level=True)`, a file-level
   `collect_ignore`) reports one skip whose id is the FILE, never a per-test node id, so the old
   `a in known` check (node ids only) never matched it even while it silences every known
   red/passed/skipped node in that file. Fixed by also treating a file-level added id as
   dangerous when that file carries known ids. Regression:
   `test_a_collection_level_skip_that_silences_a_known_file_is_not_missed`.
3. **Invalid refs silently select nothing (impacted_tests.py:589).** CONFIRMED, and the same
   `check=False`-and-ignore pattern already exists in the untouched `changed_from_git` (common
   rule 8 left it alone) — but `changed_from_lane_diff` is the new LANE-selection entry point,
   reachable straight from `select-lane --main-ref/--lane-ref` on the CLI, so a bad or unfetched
   ref there silently reporting an empty, successful selection is a live risk this lane
   introduces, not an inherited one. Fixed: raises `RuntimeError` on a nonzero `git diff` exit.
   Regression: `test_changed_from_lane_diff_raises_on_a_bad_ref_instead_of_selecting_nothing`.

All three fixes plus their regression tests: `scripts/test_pairing.py`, `scripts/impacted_tests.py`,
`tests/test_test_pairing.py`, `tests/test_impacted_tests.py` — commit following this record.
Full suite for both owned modules re-run green at `-n 2` after the fixes (106 passed).