# LANE lane-y-751-cost-in-money — Convert the transcripts' existing token figures into tokens and USD per lane and per model on the lane receipt using provider-registry.yaml's own rates, report cost per batch and per model in fleet_health, and either feed TOKEN-LOG.md from this path or delete it

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-y-751-cost-in-money "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-y-751-cost-in-money.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-y-751-cost-in-money.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-y-751-cost-in-money` — the name that produces `worktree-lane-y-751-cost-in-money` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #751 · lane-y-751-cost-in-money]`.
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
manual fallback and adds a skip-if-`worktree-lane-y-751-cost-in-money`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-y-751-cost-in-money` -> branch `worktree-lane-y-751-cost-in-money` -> contract `LANE-y-751-cost-in-money.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. CLAUSE 1, AND THE ROSTER'S PREMISE IS CORRECTED HERE: the rates DO NOT YET EXIST. Measured at freeze on `main` — `ecosystem/provider-registry.yaml` has top-level keys `providers` / `roles` / `models` and NO machine-readable rate, price or USD field anywhere; its only cost content is prose commentary (a measured `$0.037` test call under "COST REGIME"). This lane therefore AUTHORS a machine-readable rate structure in that file as its first act, rather than reading one that is not there. **This lane is the sole owner of `ecosystem/provider-registry.yaml` for batch Y** (step-0 `file-collision`; see the manifest's serialisation group).
2. The lane receipt carries tokens and USD, per lane AND per model, resolved from that file at run time — never a rate table hard-coded into this lane, and never a literal in the receipt writer.
3. `fleet_health` reports cost per batch and per model. `logs/TOKEN-LOG.md` is either fed by this path or deleted, and which one is a recorded decision rather than an omission -- it is append-only (ADR-29/ADR-39), so feeding it APPENDS and never edits an existing entry.
4. Docs and code in English; hyphen-only names; logging rather than print;
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

1. Author the machine-readable rate structure in `ecosystem/provider-registry.yaml` — it does not exist (Done-when 1). RED-first: a receipt without tokens and USD fails, and the rates must RESOLVE out of that file rather than a literal. **COMMIT**
2. Implement the conversion onto the receipt and the per-batch / per-model report in `fleet_health`. **COMMIT**
3. Rule TOKEN-LOG fed-or-deleted and execute that ruling; file or amend row `[#751]`. **COMMIT**
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
