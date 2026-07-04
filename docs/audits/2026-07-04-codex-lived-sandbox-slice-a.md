# Codex Review — lived-sandbox-slice-a

**Date:** 2026-07-04
**Branch:** `feat/lived-sandbox-slice-a`
**HEAD:** `ac3461c`
**Diff range:** `main..feat/lived-sandbox-slice-a`
**Codex version:** codex-cli 0.141.0
**Mode:** diff-review

---

## Focus

- CLAUDE_CONFIG_DIR isolation correctness (THE property): does the child truly NOT inherit the outer ~/.claude L0 hooks? Is scrubbing to _KEEP_ENV + dropping CLAUDE_PROJECT_DIR sufficient, or could an outer hook/setting leak (e.g. an unscrubbed CLAUDE_*/ANTHROPIC_* env, or a config file read outside CLAUDE_CONFIG_DIR)?
- API key handling (change #4): any path where the key could reach disk/transcript/log; no hardcoded secrets path; the sk-ant secret-scrub guard on frozen fixtures.
- Reuse of floor_conformance._run / _rmtree_guarded and the teardown blast-radius guard: correct, no path-escape / no-leftovers.
- Isolation verdict logic (present_in_configA AND absent_in_configB): is the positive-control leg necessary and correctly required (a dead control must fail the proof)?
- Windows specifics: SessionStart hook command quoting (python -c "print('MARK')"), autocrlf on the clone, subprocess env construction.
- Any correctness/robustness bug in spawn.py / isolation.py / cli.py.

---

## Findings
## CRITICAL

## CRITICAL deploy/lived_sandbox/spawn.py:211 — teardown guard is effectively bypassed

**What:** `teardown()` passes `Path(temp_root).parent` as the trusted root, so any caller-provided path automatically passes `_rmtree_guarded`.
**Why:** A bad `temp_root` or `prove_isolation(tempdir=...)` value can delete arbitrary directories, which is a data-loss risk and violates the teardown blast-radius guarantee.
**Fix direction:** Only teardown roots minted by this module, or validate against a fixed temp parent plus expected prefix before calling `_rmtree_guarded`; add a test that `sp.teardown(non_sandbox_path)` refuses before deleting.

## CRITICAL deploy/lived_sandbox/isolation.py:34 — failed child runs can still prove isolation

**What:** `IsolationResult.passed` ignores `exitA` and `exitB`, so configA can emit the marker, configB can omit it, and the proof reports `PROVEN` even if both `claude -p` runs failed.
**Why:** Auth/CLI/startup failures can become a false green isolation proof, letting later sandbox work measure a non-working facade.
**Fix direction:** Require successful exits for both legs, and test nonzero-exit combinations as failed proofs.

## HIGH

## HIGH deploy/lived_sandbox/spawn.py:131 — `extra_env` can reintroduce scrubbed Claude/Anthropic state

**What:** `_child_env()` builds a scrubbed env, then blindly applies `extra_env`, allowing callers to override `CLAUDE_CONFIG_DIR`, `CLAUDE_PROJECT_DIR`, or `ANTHROPIC_API_KEY`.
**Why:** One future caller passing a broader env can silently defeat the isolation property or leak the wrong credential into the child.
**Fix direction:** Reject or filter protected keys after merging `extra_env`; only allow explicit safe additions such as `PRE_COMMIT_HOME`.

## HIGH deploy/lived_sandbox/spawn.py:167 — subprocess failures are not normalized

**What:** `subprocess.run()` is not wrapped for `FileNotFoundError`, `TimeoutExpired`, or other `OSError` cases.
**Why:** Missing `claude`, timeout, or launch failure escapes as an unstructured traceback instead of a `SandboxError`/failed proof, despite the CLI being the operator-facing stop point.
**Fix direction:** Catch process-launch and timeout failures in `spawn()` and raise `SandboxError` with a concise diagnostic while preserving cleanup.

## MEDIUM

(none)

## LOW

(none)
