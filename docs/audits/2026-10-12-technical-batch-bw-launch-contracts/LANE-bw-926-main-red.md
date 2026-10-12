# LANE lane-bw-926-main-red — main's two unregistered reds are fixed at their cause: the Windows test_gen_handoff probes regression and the journal_day_letters 2026-10-11 (d) collision

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

**Kind:** `code` — changes executable code — `scripts/`, `tests/`, hooks, schema, generators.

The kind is DECLARED, not inferred, and it is what the routing default keys on
(`[#885]` clause 2). A text-only, deletion or read-only-digest lane never starts on
Opus; a review lane is not dispatched from a lane contract at all, because
`ecosystem/routing-table.yaml` is the authority for which CLI runs that role; a code lane
plans on Opus and implements on Sonnet **as two sessions with a file between them**,
never as one session changing tier mid-flight. The prompt cache is keyed PER MODEL,
so a mid-session switch re-writes the whole context: at this repo's measured mean of
232,875 tokens per call, one switch costs USD 1.46 into Opus or USD 0.58 into Sonnet
against USD 0.0812 saved per turn moved — about 25 consecutive cheap turns to repay
one round trip. Anything shaped like plan-then-execute is TWO SESSIONS.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-bw-926-main-red "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-926-main-red.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-926-main-red.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-926-main-red.md`
is the same act typed in full. The launcher reads this `## Dispatch`
block for its fields — model, effort, worktree, permission mode — and builds the
session's own argv; it never runs the block. The `$env:CLAUDE_PROMPTS_DIR`
token is how a frozen contract names its own location without hard-coding an
absolute path. The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-bw-926-main-red` — the name that produces `worktree-lane-bw-926-main-red` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #926 · lane-bw-926-main-red]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `opus` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The launcher admits a `claude`, `codex` or `copilot` head and refuses
any other program, so a contract's `## Dispatch` block is not a place to name a
helper. Until 2026-09-12 this generator emitted a different head here and
**every contract it produced was refused by the reader meant to launch it**;
`tests/test_dispatch_conformance.py` is the standing witness that the fence this
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-926-main-red`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-926-main-red` -> branch `worktree-lane-bw-926-main-red` -> contract `LANE-bw-926-main-red.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave F1 · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md`
(its §4 lane rules bind this lane) · **Rows:** `[#926]` owner (journal leg), nearest for the
gen_handoff leg · **Order:** `to-cc/BATCH-BW-NIGHT-2026-10-13.md` R2 (row F1-MR, added before
F0's land).

## Why

`main` (`c1b65e6d`) carries two reds that no registry entry covers, and both block a handoff cut:

- **Windows:** `tests/test_gen_handoff.py::test_filled_rerender_regenerates_probes_md_so_a_tamper_cannot_survive`
  fails with `PreflightError: [FAIL] ship_gate: 2 hard-fail finding(s) in the handoff organ set
  (handoff_probes)` (reproduced on the operator's Windows box 2026-10-13, 427 s). It guards the
  handoff, so it must be green before any cut.
- **commit-gate:** `audit.check_journal_day_letters` FAILs on `2026-10-11 (d)` — five 2026-10-11
  entries are all lettered (d), and their headings share 63 leading characters, more than
  `[#926]`'s `_JOURNAL_POINTER_CHARS = 60` correction pointer, so a correction-by-addition cannot
  name the collided blocks unambiguously.

## Done-contract (immutable)

1. **gen_handoff leg:** the Windows test above passes for a real reason found at its cause
   (RED-first if the fix is in code; never by registering it as a known red, never by skipping it
   on Windows). The cause is named in the LANE REPORT.
2. **journal leg:** RED first, then fix the CHECK or the CORRECTION MECHANISM so that the
   2026-10-11 (d) collision is resolvable by an append-only correction, with tests pinning that
   (i) the correction clears it and (ii) a new, uncorrected duplicate still FAILs. Any scope change
   is temporary by construction (dated, expiring), per `[#926]`'s precondition. No history rewrite;
   no edit of a past JOURNAL entry beyond what `[#926]` allows. A correction entry, if one is
   needed, is the integrator's JOURNAL act — the lane supplies its exact text in the handback.
3. `uv run --locked python -c "import sys;sys.path.insert(0,'scripts');import audit;from pathlib import Path;print(audit.check_journal_day_letters(Path('.')))"`
   prints no `fail` on the integration commit once the correction is applied.
4. **Done when** both are green in the wave's CI on Windows and Ubuntu (the integrator reads it at `land`).
5. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; targeted `pytest` green.
6. **Close-out:** the review record carries the served model id from the tool's
   own log and the nonce or content hash the reviewer returned (R59).

## Decision budget

**V-2 — this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license — the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. Boot: confirm the worktree path and branch, seed check (manifest §4 rule 1). **COMMIT** nothing yet.
2. Work the Done-contract above in order, RED-first where code changes (§4 rules 2-3). **COMMIT** per step.
3. Review with Codex until APPROVE (§4 rule 6). **COMMIT** fixes.
4. Push the lane branch only, write the LANE REPORT (§4 rules 4, 9), hand back (§4 rule 8), **then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
