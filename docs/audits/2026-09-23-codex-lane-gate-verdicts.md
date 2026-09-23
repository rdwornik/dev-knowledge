# Codex Review — lane-gate-verdicts

**Date:** 2026-09-23
**Branch:** `worktree-lane-gate-verdicts`
**HEAD:** `c9529fa4`
**Diff range:** `main..worktree-lane-gate-verdicts`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/gates.py: _findings_in parses audit.py's locked '[MARKER] check_name: evidence' line out of FULL captured gate output (never the truncated output_tail). Check the regex against real audit.py output shapes, and that a gate with no such lines yields findings: [] rather than an error.
- tests/test_connection_loop.py: the toy-copy labeller (_fixture_artifacts_in) now reads the structured findings list instead of substring-searching output_tail. Check this can actually fail (not vacuous), and that a marker outside the tail window is genuinely found via the new path, not accidentally still via the old tail.
- tests/test_connection_loop.py: pytest.mark.xdist_group(name='connection_loop') was added at module level to pin the launch-step trio to one xdist worker. This repo's pytest config (pyproject.toml addopts = '-n auto', no --dist=loadgroup) does not honor xdist_group markers -- confirmed via --durations=0 showing two separate ~1056s/~676s 'walk' fixture setup costs in the same -n 2 run. Please confirm whether this marker is dead code under the repo's actual invocations, and whether that matters for the claim in commit e2ebec18 that it 'pins every test in this module to one worker'.
- core-longpaths fix (c9529fa4) in the toy repo's own git config -- check it's scoped correctly and doesn't leak into the real repo's config.

---

## Findings
## CRITICAL

(none)

## HIGH

## [HIGH] scripts/plan_lint.py:1 — plan-lint capability and its test suite are deleted

**What:** The diff removes the entire plan-lint CLI and all 465 lines of its tests, with no replacement in the reviewed code.  
**Why:** This silently removes the freeze-time checks for lane collisions, dependency cycles, missing producers, and related planning hazards.  
**Fix direction:** Restore the module and tests, or land their removal only with an explicit replacement/migration.

## [HIGH] tests/test_connection_loop.py:79 — `xdist_group` does not pin this module under the configured pytest invocation

**What:** `xdist_group` is only applied by pytest-xdist’s `--dist=loadgroup`; this repository runs `-n auto` without that distribution mode.  
**Why:** The claimed single-worker isolation does not occur, so the reliability/resource mitigation described in commit `e2ebec18` is ineffective.  
**Fix direction:** Use an invocation/configuration that enables `loadgroup`, or enforce module-level worker affinity by a mechanism active under the repository’s actual pytest command.

## MEDIUM

(none)

## LOW

(none)

The findings parser itself matches `audit.py`’s real `[OK]/[~~]/[!!]/[??]/[--] check_name: evidence` lines and returns `[]` for unrelated output. The structured-findings regression is non-vacuous: its marker is explicitly absent from `output_tail`, and the end-to-end test pushes it outside the tail window. The `core.longpaths` change is correctly repository-local to the temporary toy repository and does not modify the real repository’s Git configuration.