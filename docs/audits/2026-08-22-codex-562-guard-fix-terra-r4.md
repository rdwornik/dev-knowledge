# Codex Review — 562-guard-fix-terra-r4

**Date:** 2026-08-22
**Branch:** `worktree-lane-fix-562-guard`
**HEAD:** `18d8e281`
**Diff range:** `main..worktree-lane-fix-562-guard`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Tally:** 5/1/0/0

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- Round 4 on scripts/nopack_sandbox.py. Round 3
  (docs/audits/2026-08-22-codex-562-guard-fix-terra-r3.md) found 3 Critical / 1 High; this
  diff closes them: _screen_paths confines absolute/.. operands; _parse_sed handles
  attached and bundled short options; git helper options split by position and every
  stage runs with _child_env(); _registry_lock raises instead of stealing.
- Judge whether the read surface can still reach OUTSIDE the sandbox clone or execute
  anything. Judge whether any check can be made to pass VACUOUSLY (a check that runs over
  nothing, or a refusal that fires at the wrong layer).
- Residual limits are stated deliberately in the module docstring. Flag anything NOT
  honestly covered by them.

---

## Findings
## Critical

## [CRITICAL] scripts/nopack_sandbox.py:2066 — `exec` accepts an unproven sandbox path

**What:** `_load()` accepts any `--sandbox` path (and even proceeds without a manifest), then `run_guarded()` uses it as `cwd`.  
**Why:** `exec --sandbox <outside-dir> -- cat relative-file` reads outside the provisioned clone without any absolute or `..` operand.  
**Fix direction:** Require `exec`/`probe` to validate resolved path, marker, registry membership, nonce, and manifest identity before use.

## [CRITICAL] scripts/nopack_sandbox.py:1526 — Relative operands can escape through symlinks

**What:** `_screen_paths()` only rejects lexical absolute/`..` paths; it never resolves a path-bearing operand against the sandbox.  
**Why:** A tracked `escape -> /host/secret` symlink permits `cat escape` or `ls escape/` to read outside the clone.  
**Fix direction:** Resolve actual file operands (including glob results) beneath a validated sandbox root and refuse symlink escapes.

## [CRITICAL] scripts/nopack_sandbox.py:1534 — `grep`/`rg` pattern-file operands evade confinement

**What:** The pattern parsing handles `-e` but ignores `-f`/`--file`, despite `_PATTERN_FLAGS` listing them.  
**Why:** `grep -f /etc/passwd CLAUDE.md` treats `/etc/passwd` as the default pattern and is allowed, but the tool reads it as a pattern file.  
**Fix direction:** Parse every pattern-source option and its attached/detached values before applying positional exemptions.

## [CRITICAL] scripts/nopack_sandbox.py:252 — Allowed `sort` can write outside the clone or launch a program

**What:** `sort` is allowlisted with no blocked modes; attached short-option values bypass `_escapes_sandbox()`.  
**Why:** `sort -o../outside` writes outside the sandbox, and `--compress-program` can invoke an external executable. This contradicts the claimed containment of write modes.  
**Fix direction:** Remove `sort` unless required, or explicitly parse and deny output, temporary-directory, and compressor options in all forms.

## [CRITICAL] scripts/nopack_sandbox.py:294 — Git signature verification launches external GPG tooling

**What:** `verify-commit` and `verify-tag` are read-subcommand allowlisted, and `log/show --show-signature` options are also unrestricted.  
**Why:** These invoke GPG, which uses host configuration (including possible pinentry/helper programs), so the guarded surface can execute outside programs.  
**Fix direction:** Exclude signature-verification paths or deny signature-related options and scrub the corresponding GPG environment/configuration.

## High

## [HIGH] scripts/nopack_sandbox.py:1937 — Positive controls pass when commands fail or produce no evidence

**What:** `probe()` marks every non-refused control as “allowed” regardless of return code or expected output.  
**Why:** Missing files/SHAs, and pipelines such as `git show <missing> | sed ...`, can make controls pass while checking nothing; this defeats the anti-vacuity purpose of the probe.  
**Fix direction:** Require successful return codes and command-specific output assertions for every positive control.

## Medium

(none)

## Low

(none)