# LANE lane-bw-1103-registry-repoint — the six [#1103] known-reds entries are re-tied and [#1103] is closed

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
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-bw-1103-registry-repoint "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-1103-registry-repoint.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-1103-registry-repoint.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-1103-registry-repoint.md`
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
and `--worktree lane-bw-1103-registry-repoint` — the name that produces `worktree-lane-bw-1103-registry-repoint` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #1103 · lane-bw-1103-registry-repoint]`.
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
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-1103-registry-repoint`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-1103-registry-repoint` -> branch `worktree-lane-bw-1103-registry-repoint` -> contract `LANE-bw-1103-registry-repoint.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave D · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md` (its §4 lane rules bind this lane) · **Order:** `to-cc/BATCH-B2-W4-CC-FINISH-2026-10-12.md` F3/F4 + `to-cc/AMEND-BATCH-B2-W4-CC-FINISH-R99-2026-10-12.md` + `to-cc/BATCH-B2-W4-COPILOT-2026-10-11.md` Wave D (Done-when verbatim below) + `to-cc/BATCH-BW-NIGHT-2026-10-13.md` · **Frozen on:** Wave C's integration commit (this file rides `land --slug b2-w4-c`). · **Row:** `[#1103]` owner.

**Order Done-when (verbatim):** D4 `registry-repoint`: the six `[#1103]` entries are re-tied and `[#1103]` is closed.

## Why

`logs/KNOWN-REDS-REGISTRY.json` carries `[#1103]` entries (2 members x all/ubuntu/windows at freeze); `tests/...::test_every_live_entry_names_a_row_that_is_still_open` reds when `[#1103]` closes while entries name it (JOURNAL 2026-10-11 (a)). The `[#1103]` row close itself (3 lines, `status: closed` + manifest entry) sits uncommitted-to-main on seat `seat-integrator-b2-w3-cycle-2` (`fba1a4d8`) and rides THIS lane (lane `b2w3-carry`'s inventory). R98: nothing is re-dated.

## Done-contract (immutable)

1. Each registry entry naming `[#1103]` is re-tied to the open row that actually owns its red (find it; if none exists, the lane does NOT file one — it records `INPUT_REQUIRED` with the exact intake line), with the same expiry (no re-date).
2. `[#1103]` is closed with the cycle-2 lines (byte-identical where they still apply) and BACKLOG regenerated by its generator; RED-first: `test_every_live_entry_names_a_row_that_is_still_open` is red with the close and no re-tie, green with both.
3. `tests/test_known_reds.py` and the backlog/task-tree tests targeted green; `known_reds.py` validation verb exit 0.
4. Docs and code in English; hyphen-only names; logging rather than print; Click for a CLI where one is warranted; targeted `pytest` green; `ruff` clean.
5. **Close-out:** the review record carries the served model id and session id from Codex's own output and the nonce it returned (R59).

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
3. Review with Codex until APPROVE (§4 rule 6); usage test where it applies (§4 rule 7). **COMMIT** fixes.
4. Push the lane branch only, write the LANE REPORT (§4 rules 4, 9), hand back (§4 rule 8), **then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
