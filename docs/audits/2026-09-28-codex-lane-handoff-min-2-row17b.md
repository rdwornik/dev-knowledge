# Codex Review — lane-handoff-min-2-row17b

**Date:** 2026-09-28
**Branch:** `worktree-lane-handoff-min-2`
**HEAD:** `6b6771c5`
**Diff range:** `main..worktree-lane-handoff-min-2`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/2/0/0 <!-- Critical/High/Medium/Low. Both HIGH findings are `.github/workflows/conductor.yml:91`, part of the already-accepted worktree-lane-ci-matrix/Part A history in this branch's `main..HEAD` diff -- outside row 17b's Owns (Part A's Owns list, tests/test_assemble_paste.py fixture only, ecosystem/transport-registry.yaml's one row), not introduced by this repair, and not this row's to fix (see Findings section and the note beneath it). -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

This is the AMEND-BATCH-WAVE5B-N4-REDISPATCH-2026-09-28 row 17b repair (consumer contract at
H:\My Drive\CLAUDE PROMPT DIR\to-cc\AMEND-BATCH-WAVE5B-N4-REDISPATCH-2026-09-28.md, authorized
by R23 / RATIFICATION-2026-09-25 v15), fixing the two named defects of the second
lane-handoff-min refusal on top of origin/worktree-lane-handoff-min @ 7fb0fa49.

Defect 1: scripts/gen_handoff.py imported scripts/handoff_state.py at module load; the
tests/test_assemble_paste.py fixture copies only assemble_paste.py/gen_handoff.py/
canonical_docs.py into a temp scripts/ dir, so running assemble_paste.py as a script from
there raised ModuleNotFoundError in 41 tests. Fix: deferred the import to use time via a new
_hstate() helper, same dual-shim shape as the existing _vhp() deferral for
verify_handoff_probes (the WAVE5B-N2 repair 1 precedent), replacing the sole call site at
(near) line 2948 (_hstate().state_rows(repo_root, transport)).

Defect 2: scripts/handoff_state.py builds the transport prefix "DIGEST-CAPABILITY-MAP-" with
no row in ecosystem/transport-registry.yaml, so
tests/test_transport.py::test_derivation_finds_nothing_missing_from_the_real_registry failed.
Fix: added a DIGEST_CAPABILITY_MAP row (folder to-browser, writers [operator, integrator]) --
its prefix is longer than the existing bare DIGEST kind's, so load_registry()'s longest-
prefix-first sort resolves classify() correctly without touching DIGEST's own pattern.

Please check specifically:
- Does the lazy _hstate() import correctly resolve under both entry shapes (package import,
  and scripts/-on-sys.path), same as the existing _vhp() shim it copies?
- Any other caller inside gen_handoff.py, or an external importer of gen_handoff, that
  expected the module-level _hstate name to exist eagerly (none found by grep, but check).
- Does the new DIGEST_CAPABILITY_MAP registry row's pattern/prefix correctly and exclusively
  classify DIGEST-CAPABILITY-MAP-<date>.md files ahead of the broader DIGEST kind, with no
  unintended folder/writer mismatch against real transport files?
- Anything outside the row's Owns (Part A's Owns list, tests/test_assemble_paste.py fixture
  only, ecosystem/transport-registry.yaml -- that one row) that this diff touched.

---

## Findings
## CRITICAL

(none)

## HIGH

### `.github/workflows/conductor.yml:91` — Matrix job no longer matches the required `pytest` context

**What:** The OS matrix emits `pytest (ubuntu-latest)` and `pytest (windows-latest)`, while the ruleset still requires `pytest`.  
**Why:** If the ruleset is armed, its required check will never be reported; the existing test only compares the required context to the YAML job ID, not emitted matrix check names. Matrix permutations run as separate jobs. [GitHub Actions documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)  
**Fix direction:** Align the ruleset and its agreement test with the actual matrix contexts, or add a stable aggregate `pytest` check.

### `.github/workflows/conductor.yml:91` — Matrix conversion breaks CI regression extraction

**What:** Existing `ci_verdict` selects only a job named exactly `pytest`; the matrix creates no such job.  
**Why:** CI verdicts will no longer read the suite-gate log/baseline or identify individual regressions, falling back to opaque failed matrix-job names; the new handoff CI state row consumes this result.  
**Fix direction:** Update the CI verdict reader and tests to aggregate/identify the matrix pytest jobs and their suite-gate output.

## MEDIUM

(none)

## LOW

(none)

The row-17b repair delta from `7fb0fa49` touches only `scripts/gen_handoff.py` and `ecosystem/transport-registry.yaml`; the lazy `_hstate()` shim correctly supports both import shapes, and the longer `DIGEST-CAPABILITY-MAP-` prefix correctly wins over `DIGEST-` for the intended Markdown files. No in-repo external eager `_hstate` consumer was found.

The broader requested `main..worktree-lane-handoff-min-2` diff also includes earlier changes to the workflow, `handoff_state`, `seat_registry`, `verify_handoff_probes`, and their tests.