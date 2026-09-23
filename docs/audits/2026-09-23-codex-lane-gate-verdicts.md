# Codex Review — lane-gate-verdicts

**Date:** 2026-09-23
**Branch:** `worktree-lane-gate-verdicts`
**HEAD:** `020037c9`
**Diff range:** `main..worktree-lane-gate-verdicts`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Consumer:** `[#959]` — lane-gate-verdicts' own backlog row
(`tasks/959-wave-4b-lane-3-lane-gate-verdicts-gates-speak-data-and-the-connection-test-reads-it.md`),
the W4B-3 Done-contract item requiring "Codex terra review with its consumer cited". This review's
finding is disposed against that row's Done-contract, not a separate governance surface.

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

---

## Dispositions ([#959], 2026-09-23)

**The one HIGH finding was genuine and independently reproduced before this review ran.**
Investigating Done-contract item 5 (module runtime `<= 10 min` at `-n 2`), three measured
`-n 2` runs of `tests/test_connection_loop.py` came back at 17m33s / 18m29s / 17m42s — unchanged
from the pre-lane baseline (18:08, WAVE4-FINAL digest). `--durations=0` on the third run showed
TWO separate multi-hundred-second `setup` costs for the module-scoped `walk` fixture (1056.58s and
676.85s) in the SAME run, which is only possible if the module ran split across both `-n 2`
workers rather than pinned to one. Checked against the installed `pytest-xdist` source
(`xdist/remote.py`: `config.option.loadgroup = config.getvalue("dist") == "loadgroup"`) and this
repo's `pyproject.toml` (`addopts = "-n auto"`, no `--dist=loadgroup` anywhere in the repo,
including `.claude/skills/verify/verify.py`'s own `--dist worksteal`), the marker added in
`e2ebec18` never activates under any invocation this repo actually uses.

**Fixed:** `tests/test_connection_loop.py`'s module-level comment claiming `xdist_group` "pins
every test in this module to ONE worker" is corrected in place to state the measured truth — the
marker is inert under `-n auto`/bare `-n 2`, kept only as a harmless forward declaration for a
future `--dist=loadgroup` invocation that no part of this repo currently sets. **Not fixed (out of
this lane's owned files):** making the marker actually effective needs a `--dist=loadgroup`
invocation flag, either in `pyproject.toml`'s global `addopts` (repo-wide, cross-cutting, not owned
by this lane) or in whatever future organ standardizes this module's invocation. It is also not
proven to *reduce* wall-clock time — pinning removes the duplicate `walk` build but also removes
the cross-worker parallelism this module currently gets by accident, so serializing everything onto
one worker could net out slower, not faster; that trade-off needs its own measurement, not a
guess written into this lane's diff.

**Done-contract 4 stands regardless:** the launch-step trio's actual, verified fix is
`core.longpaths` in the toy repo's own git config (`c9529fa4`) — proven by 3/3 green `-n 2` runs
(21 passed, 1 xfailed, 0 failed, every time) measured AFTER the comment correction above, with the
`xdist_group` marker confirmed still inert. **Done-contract 5 is NOT met on a strict `<= 10 min`
reading** — see the SESSION file for the full runtime finding and which tests are inherently slow.