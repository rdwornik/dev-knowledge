# Codex Review — lane-heartbeat-admission

**Date:** 2026-09-26
**Branch:** `worktree-lane-heartbeat-admission`
**HEAD:** `987f2b47`
**Diff range:** `main..worktree-lane-heartbeat-admission`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/3/0/0 <!-- Critical/High/Medium/Low. Disposition, next commit: substrate-heartbeat.yml:132
(prebuild masked by continue-on-error) REVIEWED AND KEPT -- DECIDED-BY-LANE, see the workflow's own
comment and the handback session file (Done-item 4 would be structurally unreachable otherwise,
against a real currently-true staleness); substrate_heartbeat.py:385 (freshness read HEAD, not main)
FIXED -- _resolve_main_ref prefers origin/main, regression test added; codespace_admission.py:131
(PATH accepted non-executable files) FIXED -- Probe.which now requires os.access(X_OK), regression
test added (POSIX-only, skipif on win32). This tally counts what the review found, not what
remains open. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

Reviewing LANE-5B3-9-heartbeat-admission (.dev-knowledge repo). Cite this contract at
H:\My Drive\CLAUDE PROMPT DIR\LANE-5B3-9-heartbeat-admission.md as the consumer.
Key concerns: does scripts/codespace_admission.py faithfully cite the deployed
DispatchHelpers.psm1 line numbers for each gating condition without editing that file;
is the git-hooks-armed check (an ADDED condition beyond the deployed test) sound; does
the prebuild-freshness leg in scripts/substrate_heartbeat.py correctly distinguish
ok/refused/undetermined and never invent a stored secret (uses only the workflow's
default GITHUB_TOKEN); is the container job's bash -l invocation of
codespace_admission.py correct and does it avoid depending on ~/.bashrc PATH gaps.

---

## Findings
Consumer reviewed: `H:\My Drive\CLAUDE PROMPT DIR\LANE-5B3-9-heartbeat-admission.md`.

## Critical

(none)

## High

## [HIGH] .github/workflows/substrate-heartbeat.yml:132 — prebuild refusal is masked

**What:** `continue-on-error: true` makes `refused` (exit 1) and `undetermined` (exit 2) prebuild results leave the declaration job green.  
**Why:** A green heartbeat can therefore coexist with a stale or unverified prebuild, contrary to the consumer contract’s intended admission signal.  
**Fix direction:** Make the prebuild verdict an enforced job result, or explicitly separate a non-gating diagnostic workflow from the heartbeat’s green/red result.

## [HIGH] scripts/substrate_heartbeat.py:385 — freshness is checked against the checked-out branch, not main

**What:** `_newest_devcontainer_commit()` runs `git log … -- .devcontainer` without naming `main`/`origin/main`, despite the contract requiring the newest such commit on main.  
**Why:** A manually dispatched branch behind or ahead of main can produce a false refusal or false OK unrelated to the prebuild served for main.  
**Fix direction:** Resolve the declared default ref explicitly (for example `origin/main`) for the log and ancestry comparison, with a divergent-branch test.

## [HIGH] scripts/codespace_admission.py:131 — PATH checks accept non-executable files

**What:** `Probe.which()` treats any regular file named like a tool as present, without checking that it is executable.  
**Why:** The deployed `command -v` admission checks reject non-executable files; this predicate can instead admit a container missing a runnable `claude`, `uv`, `python3`, or `pre-commit`.  
**Fix direction:** Require executable permission in the Linux-targeted check and add fixtures for non-executable PATH entries.

## Medium

(none)

## Low

(none)