# Codex Review — 446-v6-boot-build

**Date:** 2026-07-30
**Branch:** `feat/446-boot`
**HEAD:** `7723a431`
**Diff range:** `main..feat/446-boot`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review

---

## Focus

[#446] SS B(b) one-round-trip boot build, 14 commits, built to a RED-first frozen contract
(tests/test_v6_frozen_contract.py, frozen at 1e93c746 BEFORE any build code).

Review with these specific risks in mind:
- ANTI-BLUFF INTEGRITY: no generated bundle row may carry an answer value. Probe rows are
  locator+command+assertion only. verify_handoff_probes FAILs any row matching /expected[ :]/i.
- PROBE WEAKENING: the _FILE_RE tokenizer change (leading dot at a token boundary via negative
  lookbehind) and the header_tokens change (^#{1,6}\s) must ADD bindings and REMOVE a false
  anchor class WITHOUT widening what resolves. Check the lookbehind for over/under-matching.
- FAIL-OPEN DEGRADE: gen_handoff._tracked_under fails OPEN on git error (documented). Is that
  the right call, and is the RM-8 refusal defeatable in a way that matters?
- SPLIT-SITE ENFORCEMENT: assemble_paste WARNs, audit.check_boot_byte_budget FAILs. The budget
  is single-sourced in assemble_paste and READ by audit. Any way the two disagree?
- CLI CONTRACT: verify_handoff_probes.main returns codes and never raises SystemExit;
  --cross-repo without --repo-root returns 2; the default call esults = verify(bundle) is
  preserved byte-identical.
- Correctness of the ALL_CHECKS 34->35 pin moves and the reverse-dep-oracle line-pin updates.

---

## Findings
## Critical

(none)

## High

### [HIGH] [scripts/gen_handoff.py:197](<C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\gen_handoff.py:197>) — Git errors disable RM-8

**What:** `_git()` returns the same empty string for “no tracked files” and Git failure, so `_tracked_under()` authorizes the original bundle directory on errors; an invalid inherited `GIT_DIR` reproduced this against an existing tracked bundle.

**Why:** A Git configuration/error can silently permit overwriting an immutable committed handoff—the exact behavior RM-8 is intended to prevent.

**Fix direction:** Scrub Git-location environment variables using the existing audit precedent and preserve success/error as distinct states; refuse an existing target when tracking status cannot be established.

### [HIGH] [scripts/gen_handoff.py:225](<C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\gen_handoff.py:225>) — `--allow-suffix` can overwrite an existing untracked bundle

**What:** Suffix selection accepts the first directory containing no tracked files, even when that directory already exists with untracked work.

**Why:** Generation then rewrites files in that directory, contradicting the CLI promise to create a “NEW” sibling and potentially destroying an in-progress handoff.

**Fix direction:** Select only a nonexistent suffix directory; skip or explicitly refuse every existing candidate, tracked or untracked.

### [HIGH] [scripts/verify_handoff_probes.py:69](<C:\Users\1028120\Documents\Dev\.dev-knowledge\scripts\verify_handoff_probes.py:69>) — Dotfile tokenizer creates false live bindings

**What:** The lookbehind guards only the optional dot, not the start of the complete token. Consequently `/.methodology.yaml` becomes `.methodology.yaml`, while `https://host/.methodology.yaml` becomes `host/.methodology.yaml`; basename fallback resolves both to the repo-root `.methodology.yaml`.

**Why:** Absolute or URL-like locators can incorrectly pass structural probe validation, widening what resolves and weakening probe teeth.

**Fix direction:** Add the dotfile support as a separately boundary-anchored relative-path alternative while preserving the old matcher unchanged; add negative tests for absolute and URL-prefixed dotfiles.

## Medium

(none)

## Low

(none)

Validation: `git diff --check` passed, 1,986 tests collected, and 10 applicable read-only contract tests passed. Tests requiring writable temporary directories could not run in the read-only sandbox.
