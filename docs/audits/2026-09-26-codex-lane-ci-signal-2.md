# Codex Review — lane-ci-signal-2

**Date:** 2026-09-26
**Branch:** `worktree-lane-ci-signal-2`
**HEAD (reviewed diff):** `4bb84c0d`
**Diff range:** `origin/main...worktree-lane-ci-signal-2`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 0/1/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned, reviewer role)
**Review profile:** code

**Consumer:** `LANE-5B3-8-ci-signal-2.md` Done-contract item 5 — the terra re-review N2's
`LANE-5B2-17-ci-signal.md` owed once Codex quota reset (N2's own record,
`docs/audits/2026-09-26-fresh-eyes-lane-ci-signal.md`, ran DEGRADED on grok because Codex was
quota-blocked at the time). Serves `[#802]` (`tasks/802-the-conductor-emails-on-every-push-because-it-does.md`), the row both lanes' contracts implement.

---

## Focus

(none specified — full diff review of this lane's accumulated N2 + O3 changes)

---

## Findings

## Critical

(none)

## High

## [HIGH] scripts/known_reds.py:261 — Registered `audit-health` red masks unrelated failures

**What:** `compare_hook()` treats every non-zero `audit-health` exit as known when the hook ID
is registered, regardless of why it failed.
**Why:** The committed registry permanently registers the CI-environment failure, so a new
repository regression within `audit-health` is reported as a passing known red and the new CI
signal is silently laundered.
**Fix direction:** Compare a stable, scoped failure signature (or separately classify expected
environment findings) rather than accepting any non-zero exit for the hook ID.

## Medium

(none)

## Low

(none)

---

## Disposition (common rule 3(e): fix a Codex review's P1 findings)

Fixed in the same lane, on top of this record's reviewed `HEAD` (`4bb84c0d`):

- `compare_hook()` now accepts optional `hook_output`; when a `registry.hooks` entry carries a
  `checks:` allowlist (the specific `audit.py health` check names it was measured against), the
  ACTUAL failing check names extracted from the raw hook output must be a subset of that
  allowlist — a name outside it is a genuine regression even though the hook id itself is
  registered. `extract_failing_check_names()` parses both of `audit.py health`'s output sections
  (`[!!] <name>: <evidence>` self-audit lines, `[!!] <label>  (<detail>)` operational lines).
- No `--hook-output` flag, or an entry with no `checks:` list, keeps the prior whole-hook
  behavior exactly — backward-compatible with every existing caller and committed registry entry.
- The `audit-health` registry entry's `checks` list was populated from the real cause already on
  record (`hooks_armed`, `repos registered`, `dispatch_drift`) plus a fourth, previously
  invisible one this same scoping surfaced live against this branch's own CI run 36252211768:
  `journal_spine_anchor`, failing on the identical shallow-clone-leaves-`main`-unresolvable cause
  already registered on the pytest side (LANE-5B2-17, 5 members, run 36220172268) — confirmed by
  running `compare-hook --hook-output` against that run's real `audit-health.out` artifact.

Verified: `tests/test_known_reds.py` (40 passed, including four new cases: the extractor reading
both output sections, a scoped pass on exactly the registered set, a scoped regression on a new
unregistered check name — the RED-first witness for this finding — and the backward-compatibility
case with no `hook_output`); `tests/test_conductor.py` (56 passed); a live re-run of
`known_reds.py compare-hook` against run 36252211768's downloaded `audit-health.out` artifact,
verdict `PASS`.
