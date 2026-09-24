# Codex Review — lane-launcher-fixes

**Date:** 2026-09-25
**Branch:** `worktree-lane-launcher-fixes`
**HEAD:** `fb01eaf7`
**Diff range:** `main..worktree-lane-launcher-fixes`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** TBD/TBD/TBD/TBD <!-- Critical/High/Medium/Low. FILL FROM THE FINDINGS SECTION before committing. The hub's review_artifact_coverage leg parses four digits here; TBD deliberately does not parse, so an unfilled tally keeps WARNing instead of shipping a number nobody counted. -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

---

## Focus

- scripts/dispatch.py: does the no-live-integrator refusal reliably surface the exact
  seat_registry.py bind --role integrator --batch <BATCH> command through run_prelaunch's
  new REFUSED-line prioritization, without truncation, and without ever giving a false pass?
- scripts/dispatch.py: is the new copilot head correctly spawned DETACHED (log_path set,
  Popen path) exactly like codex, never run to completion in the caller's process?
- scripts/dispatch.py: does warn_model_alias ever change the launched model, or only warn?
- Any regression risk in the _identify/self_identified refactor or the detached-heads set,
  or in the worktree field reported for a copilot lane (cwd, since copilot has no --worktree flag).

---

## Findings
## CRITICAL

## [CRITICAL] scripts/dispatch.py:909 — Copilot launches stop holding their slug after 180 seconds

**What:** `_held_by` uses `process_alive(pid)` only for `provider == "codex"`; a live Copilot receipt falls through to the Claude-agent lookup and is released once its receipt ages beyond `LISTING_LAG_SECONDS`.
**Why:** A second lane with the same slug can then launch while the detached Copilot process is still writing in the same `cwd`, defeating collision protection and risking concurrent-data loss.
**Fix direction:** Apply the PID/liveness holding path consistently to every detached/self-identified head, including Copilot.

## HIGH

## [HIGH] scripts/dispatch.py:826 — REFUSED-line output can still truncate the integrator bind command

**What:** The prioritized refusal output is still passed through `_tail(..., 2000)`, while `--batch` is unconstrained and is interpolated repeatedly before and inside the required bind command; multiple refused lines also share that budget.
**Why:** A long batch value or earlier refusal lines can cut the exact `seat_registry.py bind --role integrator --batch <BATCH>` command, violating the remediation-output guarantee.
**Fix direction:** Preserve the complete selected refusal line (or specifically the complete `no-live-integrator` line) without a shared truncation limit, with coverage for long batch values and multiple refusals.

## [HIGH] scripts/dispatch.py:1422 — Copilot lanes cannot be governed through their detached log

**What:** `_watch` recognizes only `provider == "codex"` for log/PID monitoring; Copilot receipts instead enter the Claude-session binding path.
**Why:** Copilot is absent from `claude agents --json` and has no Claude transcript, so `govern` records it as unobserved rather than monitoring its detached process/log despite its `stream` metering declaration.
**Fix direction:** Route supported detached heads through an appropriate log/PID monitoring path, or explicitly refuse/unavailable-mark Copilot governance until its output has a supported usage format.

## MEDIUM

(none)

## LOW

(none)