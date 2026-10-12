# LANE lane-bw-893-b2w3-carry — the B2-W3 cycle-4 seat leftovers land (R97c)

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | medium |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

**Kind:** `text` — text-only, deletion, or read-only digest — prose, rows, rulings and removals; no executable code changes hands.

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
claude --bg --model sonnet --effort medium --permission-mode bypassPermissions --worktree lane-bw-893-b2w3-carry "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-bw-893-b2w3-carry.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-bw-893-b2w3-carry.md` **from the target repo root** — the hub shim over
`scripts/dispatch.py launch`, which runs the hub's launcher without changing
directory (PLAYBOOK Ch8's dispatch table, the sole literal-command site). From
the hub checkout itself, `uv run --locked python scripts/dispatch.py launch LANE-bw-893-b2w3-carry.md`
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
and `--worktree lane-bw-893-b2w3-carry` — the name that produces `worktree-lane-bw-893-b2w3-carry` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #893 · lane-bw-893-b2w3-carry]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `sonnet` whatever any
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
generator writes is one `dispatch.py` accepts. A lane already holding `worktree-lane-bw-893-b2w3-carry`
is refused earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-bw-893-b2w3-carry` -> branch `worktree-lane-bw-893-b2w3-carry` -> contract `LANE-bw-893-b2w3-carry.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Context

**Batch:** BW (B2-W4 finish), wave F1 · **Manifest:** `docs/audits/2026-10-12-technical-batch-bw-manifest.md`
(its §4 lane rules bind this lane; rules 3, 6 and 7 do not apply — no code) · **Row:** `[#893]` nearest · **Order:** F2, R97(c).

## Inventory (taken by the integrator at freeze, `git diff origin/main` per dirty file, `+` lines only)

| Seat | Lines missing from origin/main | Fate |
|---|---|---|
| `seat-integrator-b2-w3` (`b78c08b6`, dirty `logs/MERGE-RECEIPTS.jsonl`) | 0 | on main; worktree removed by the integrator |
| `seat-integrator-b2-w3-cycle-1` (`a61ca631`, 4 dirty files) | 0 | on main; worktree removed by the integrator |
| `seat-integrator-b2-w3-cycle-2` (`fba1a4d8`) | 3 — the `[#1103]` row close (`status: closed`, manifest entry) | NOT this lane: the close reds `test_every_live_entry_names_a_row_that_is_still_open` while six registry entries name `[#1103]` (JOURNAL 2026-10-11 (a)); it rides lane `lane-bw-1103-registry-repoint` (Wave D) |
| `seat-integrator-b2-w3-cycle-4` (`5eacd135`, tag `archive/b2-w3-close-carry`) | 4 — 3 `logs/LANE-COSTS.jsonl` seat-cost rows, 1 `logs/MERGE-RECEIPTS.jsonl` arc receipt | **this lane** |

## Done-contract (immutable)


1. The four lines of `5eacd135` are on the lane branch, byte-identical, appended at the end of
   their append-only files (`git cherry-pick 5eacd135`, resolving any append conflict by keeping
   BOTH sides in chronological order).
2. `git diff origin/main...HEAD` shows exactly 4 added lines and 0 removed lines.
3. `uv run --locked pytest tests/test_merge_receipt.py tests/test_lane_cost.py -q` green (or the
   nearest tests that read those ledgers — find them with `file_purpose_graph.py why`).

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
