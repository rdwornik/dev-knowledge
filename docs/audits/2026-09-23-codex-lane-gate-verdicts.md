# Codex Review — lane-gate-verdicts

**Date:** 2026-09-23
**Branch:** `worktree-lane-gate-verdicts`
**HEAD:** `020037c9`
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

### tests/test_connection_loop.py:79 — `xdist_group` is inert under the repo’s pytest invocations

**What:** `pytest.mark.xdist_group(name="connection_loop")` only affects pytest-xdist’s `--dist=loadgroup` scheduler; this repo uses `-n auto` / `-n 2` without that option.  
**Why:** Tests in this module can still be assigned to separate workers, so commit `e2ebec18`’s claim that the marker “pins every test in this module to one worker” is false and its intended resource/flakiness mitigation is not delivered.  
**Fix direction:** Use `--dist=loadgroup` in the relevant pytest invocation/config, or remove/reword the marker and claim.

## MEDIUM

(none)

## LOW

(none)

The findings parser matches `audit.py`’s actual emitted finding shape and correctly returns `[]` for unrelated output. The new tail-window regression tests are non-vacuous. `core.longpaths` is set through `git config` in the freshly initialized toy repo, so it does not modify the real repository’s configuration.