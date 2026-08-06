# Codex Review — batch-protocol

**Date:** 2026-08-06
**Branch:** `feat/505-batch-protocol`
**HEAD:** `47db4a99`
**Diff range:** `main..feat/505-batch-protocol`
**Codex version:** codex-cli 0.145.0
**Mode:** diff-review
**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code
**Tally:** 0/3/0/0 (C/H/M/L)

> **The script's own heuristic tally printed `0 0 0 0` and is wrong** — three HIGH findings are
> in the body below. The line above is hand-counted from the findings, per the canonical-header
> requirement; the heuristic evidently does not match this artifact's `## [HIGH]` heading form.
> Noted rather than fixed here: the script lives in `~/.claude/bin/`, and a global-infra edit is
> exception-with-ruling (core-invariant #6). Carried to the packet.
>
> **Profile note:** the diff is mixed code+prose, so the path-guard filtered it to the code
> subset and the prose (the PLAYBOOK section, the two commands, the ADR addendum) was **not**
> doc-lane reviewed. That is the documented mixed-diff behaviour, not a skipped step — recorded
> so a later reader does not read this artifact as covering the prose.

---

## Focus

- The audit check check_stale_worktrees and its reader _git_linked_worktrees in scripts/audit.py: porcelain parsing correctness, the assumption that the MAIN worktree is always first, boundary handling on the 7-day horizon, and whether any input can make it FAIL rather than WARN.
- scripts/validate_branch_naming.py: regex correctness, classification precedence (a worktree-lane-* that fails the lane grammar must not fall through to the looser worktree- member), remote-stripping, and exit-code discipline (2 = could not look, 1 = looked and found).
- Whether the two new .claude/commands/ files duplicate doctrine that PLAYBOOK Ch8 already owns.
- Test quality: do the new tests actually constrain behaviour, or would a broken implementation still pass?

---

## Findings
## Critical

(none)

## High

## [HIGH] scripts/audit.py:1057 — Porcelain reader cannot parse newline-containing worktree paths

**What:** The reader uses newline-delimited porcelain output and `splitlines()` instead of `--porcelain -z`.  
**Why:** A valid linked-worktree path containing a newline is split into malformed records, then falsely treated as missing and reported stale.  
**Fix direction:** Request `-z` and parse NUL-delimited attributes without stripping path values; add an integration/fixture test for unusual paths.

## [HIGH] scripts/validate_branch_naming.py:115 — Remote stripping only recognizes `origin`

**What:** `strip_remote()` hard-codes `origin/`, so valid remote-tracking names such as `upstream/main` classify as unknown.  
**Why:** Git remote names are arbitrary; this produces an exit-1 “outside the enum” result for an otherwise conforming branch.  
**Fix direction:** Normalize against configured remote names (or explicitly narrow the documented contract to `origin` only) and test a non-`origin` remote.

## [HIGH] tests/test_stale_worktrees.py:153 — Reader behavior is effectively untested

**What:** The only live-reader test accepts an empty result and only asserts that the primary path is absent.  
**Why:** A broken `_git_linked_worktrees()` that always returns `[]` passes all new reader tests, silently disabling stale-worktree detection.  
**Fix direction:** Create a temporary linked worktree and assert its path, branch, on-disk state, and commit epoch are returned.

## Medium

(none)

## Low

(none)

---

## Resolution summary

All three findings ACCEPTED and fixed pre-merge. No finding was dispositioned away.

| # | Finding | Disposition |
|---|---|---|
| H1 | Porcelain reader cannot parse newline-containing paths | **FIXED.** `--porcelain -z` first, NUL-split, path no longer `.strip()`ed. Taken with a fallback rather than straight: `-z` arrived in a later git, and returning `None` on an older one would have *disabled* the check to fix a false WARN. A failed `-z` now re-runs without it. |
| H2 | Remote stripping hard-codes `origin/` | **FIXED.** `strip_remote`/`classify` take a `remotes` tuple defaulting to `("origin",)`, and the CLI derives the real set from `git remote`. `upstream/main` still classifies unknown by *default* — stripping any first segment would let `feature/x` through as a remote — but a caller that knows its remotes gets the right answer. |
| H3 | Reader behaviour effectively untested | **FIXED, and it was the sharpest of the three.** The old live test passed on a reader that always returned `[]` — the green-that-means-nothing class. Two integration tests now provision a real linked worktree against real git: one asserts every field the check consumes comes back populated, the other deletes the directory without deregistering and asserts the half-finished-teardown WARN. Both tear down after themselves. |

**Not from this review, surfaced by the arc and carried to the packet instead of fixed here:**
the review script's severity heuristic (see the header note), the superseded three-check
parallel test still in `templates/handoff/02_METHODOLOGY.md.tmpl`, and `automation/fleet-audit`
sitting outside the prose branch enum.

