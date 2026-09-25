# Codex Review — lane-launcher-fixes

**Date:** 2026-09-25
**Branch:** `worktree-lane-launcher-fixes`
**HEAD:** `fb01eaf7`
**Diff range:** `main..worktree-lane-launcher-fixes`
**Codex version:** codex-cli 0.155.0
**Mode:** diff-review
**Tally:** 1/2/0/0 <!-- Critical/High/Medium/Low -->

**Model used:** `gpt-5.6-terra` (pinned; both lanes — [#469])
**Review profile:** code

no-consumer: this lane files no BACKLOG row of its own for these findings -- all three were
fixed directly in the same session's commit `cc098d48`, the same direct-disposition route
`2026-09-24-codex-lane-provider-registry.md`'s own no-consumer line takes for its finding.

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

---

## Dispositions (lane-launcher-fixes, same session, commit `cc098d48`)

- **CRITICAL (Copilot launches stop holding their slug after 180 seconds) — ACCEPTED, fixed.**
  `_held_by`'s PID-liveness branch was keyed on the literal string `"codex"`; generalized to
  `provider in _DETACHED_HEADS` (`{"codex", "copilot"}`), so a live Copilot process now holds its
  slug by `process_alive(pid)` exactly as codex does, past `LISTING_LAG_SECONDS`. Fixed:
  `test_a_copilot_receipt_whose_process_is_alive_holds_the_slug_past_the_listing_lag` and
  `test_a_copilot_receipt_whose_process_has_ended_frees_the_slug`
  (`tests/test_dispatch_launch.py`).

- **HIGH 1 (REFUSED-line output can still truncate the integrator bind command) — ACCEPTED,
  fixed by removing the cap rather than raising it.** A raised-but-fixed budget is the same
  defect at a larger radius: a long enough `--batch` value, or a second refusal sharing the
  budget, can still cut the command. `run_prelaunch` no longer passes a matched `REFUSED [...]`
  line (or several) through `_tail` at all -- it joins and returns them whole. Fixed:
  `test_a_very_long_batch_value_does_not_cut_the_command_out_of_its_own_remedy` and
  `test_two_refusals_in_one_run_both_survive_in_full` (`tests/test_dispatch_launch.py`).

- **HIGH 2 (Copilot lanes cannot be governed through their detached log) — ACCEPTED, fixed by
  making the gap explicit rather than building an unverified reader.** The CLI does carry a
  supported usage surface (`copilot --help`: `--usage-output-file`, `--output-format json`), but
  this session did not run a live `copilot` invocation to confirm the per-line event shape
  against the code that would parse it -- guessing that shape would risk a reader that silently
  mis-parses rather than one that is honestly absent. `_watch` now branches on
  `provider == "copilot"` explicitly, records an honest `UNOBSERVED` naming the real reason (no
  claude-agent identity, no usage-format reader yet) instead of falling through to a
  claude-agent bind that can never succeed and a misleading reason. Wiring a real reader for
  `--usage-output-file`'s JSON (the shape is already witnessed in-repo:
  `docs/audits/2026-09-23-technical-copilot-admission-evidence.md`'s `copilot-usage.json`
  artifacts) is left as a ROWS-OWED finding rather than fixed blind. Fixed:
  `test_govern_on_a_copilot_receipt_is_an_honest_unobserved_never_a_false_zero`
  (`tests/test_dispatch_launch.py`).

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-25-codex-lane-launcher-fixes.md | ACTIONED | cc098d48 |