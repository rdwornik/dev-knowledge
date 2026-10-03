# Codex Review — foundation-2-cheap-fixes

**Date:** 2026-10-03
**Branch:** `worktree-foundation-2-cheap-fixes`
**HEAD at review time:** `321811a9`
**Diff range:** `origin/main...321811a9` (`2e7fa5f2` base)
**Codex version:** n/a — SUBSTITUTED under BATCH-COMMON §0 ruling (e) (see below)
**Mode:** diff-review, isolated read-only session (the diff, the changed files and the contract only — not the lane)
**Tally:** P1=0 P2=0 P3=0 (one disputed remark, dispositioned below)
**Consumer:** `LANE-FOUNDATION-foundation-2-cheap-fixes.md` (Done-contract item 7, "the review record citing this contract inside it")

**Model used:** `grok-4.6` (SUBSTITUTE for the pinned `gpt-5.6-terra` — see Substitution note)
**Review profile:** code

---

## Substitution note

`SUBSTITUTION: codex terra -> grok-4.6 (Codex is at its usage limit until 2026-10-03 21:07; this review ran at about 16:00 local time)`.
This is the batch order's own route (BATCH-COMMON §0 ruling (e)), not a silent one. Grok is not
the producer's vendor and is not the implementing session.

**Command:** from an empty folder holding only `diff.patch`, the five changed files, two read-only
scripts (`surface_triage.py`, `codespace_admission.py`) and the contract —
`grok -m grok-4.6 --tools read_file,list_dir,grep -p "<the review prompt>"`; exit 0.
**Served model:** `grok-4.6`, read from the session's `usage.json` `primaryModelId` (7 model calls).
**Output contract (R59 item 1):** the answer had to open by quoting the first line of `diff.patch`; it
did (`diff --git a/.github/workflows/conductor.yml …`), so the read is proven.

## Findings

**No P1 findings.** The reviewer checked Done-contract items 1–6 for four classes: a weakened
assertion, a mask that still leaks, a broken advisory posture of the `ship-gate` job, a vacuous new test.

| Item | The reviewer's reading |
|---|---|
| D1 | the regenerated count is the only change; the `findings == []` assert is not in the diff |
| D2 | `_origin_reachable` / `_gh_healthy` patch the two names `run_admission` looks up at call time; the `== 1` then `== 0` asserts are unchanged |
| D9 | `shutil.which("bash")` is the same resolver the skipif and the sibling test use; the three asserts are unchanged; no platform skip |
| D10 | the in-process mask hits both lookups in `resolve_gh` (PATH and `ProgramFiles`) plus the Windows cwd search; `resolve_gh() is None` fails if either still finds a `gh` |
| J1 | `continue-on-error: true` kept; `fetch-depth: 0` and the seed step added before the gate; the new pin fails on a missing depth, a missing seed, or a wrong order |

## Disputed remark

The reviewer called the D10 comment "a wrong account of the old `dict(os.environ).pop` miss". The lane
measured the facts the comment states, on this box, before writing it: `dict(os.environ)` keys are upper-case
on Windows (`['PROGRAMFILES']`), and a child launched with `ProgramFiles` removed, or set to an empty
directory, still reads `C:\Program Files` (also through `cmd /c echo %ProgramFiles%`). The reviewer ran
nothing. Disposition: **kept**; the comment was widened to state both facts.

## Consumer

This record is the review the contract names (`LANE-FOUNDATION-foundation-2-cheap-fixes.md`, Done-contract
item 7), written to the name the audit grammar admits (`docs/audits/<date>-codex-<slug>.md`).
`docs/audits/README.md` is left stale for the integrator (`[#590]`).
