# LANE lane-y-754-backlog-to-bar — Bring BACKLOG.md under 72,000 B by running archive_row_body.py on its trigger over the rows above the ceiling, run the lapsed groom, and rule on the two ceilings that measure different corpora

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-y-754-backlog-to-bar "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-y-754-backlog-to-bar.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-y-754-backlog-to-bar.md` **from the target repo root** — the ruled verb for a local
lane (PLAYBOOK Ch8's dispatch table, the sole literal-command site). The verb
reads this `## Dispatch` block and runs it **verbatim**, substituting exactly
one literal — `$env:CLAUDE_PROMPTS_DIR` — which is how a frozen contract
names its own location without hard-coding an absolute path. That spelling is
load-bearing: it is the only token the reader replaces, and any other
placeholder is passed through untouched into a real session's prompt.
The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-y-754-backlog-to-bar` — the name that produces `worktree-lane-y-754-backlog-to-bar` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #754 · lane-y-754-backlog-to-bar]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `opus` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The verb refuses any other program — *"this script never runs an
arbitrary command from a contract file"* — so a contract's `## Dispatch` block
is not a place to name a helper. Until 2026-09-12 this generator emitted the
deprecated `Dispatch-Lane` alias here and **every contract it produced was
refused by the verb meant to launch it**. That alias still resolves as the
manual fallback and adds a skip-if-`worktree-lane-y-754-backlog-to-bar`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-y-754-backlog-to-bar` -> branch `worktree-lane-y-754-backlog-to-bar` -> contract `LANE-y-754-backlog-to-bar.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. CLAUSE 1, BEFORE A SINGLE ROW IS TOUCHED (ruling AY1-3): verify that `archive_row_body.py`'s trigger is LIVE on `main`. Its premise was refuted at freeze -- on 2026-09-13 the graph organ reported zero wiring consumers for `scripts/archive_row_body.py` (only `task-implements` edges) and its trigger commit sat on an unmerged branch. If the trigger is not live, this lane WIRES it as clause 1 rather than assuming it.
2. `BACKLOG.md` is under 72,000 B (90,849 B at freeze) with the over-ceiling row COUNT falling rather than the ceiling rising; the lapsed groom runs (45 days against a 21-day cadence); and the two ceilings are reconciled -- 400 B measured on the view against 1320 chars measured on the reassembled source do not measure the same corpus, so one is retired or re-based and the ruling is recorded.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

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

1. Verify the `archive_row_body.py` trigger is live on `main`; if it is not, wire it -- this is clause 1 and it precedes every other act in this lane (AY1-3). **COMMIT**
2. Run the trigger over the rows above the ceiling and run the lapsed groom, measuring BACKLOG bytes before and after. **COMMIT**
3. Rule on the two ceilings measuring different corpora -- retire or re-base one -- and record the ruling; file or amend row `[#754]`. **COMMIT**
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
