# LANE lane-y-755-docs-cut-finish — Delete protocols/ESSENTIALS.md rather than merely de-registering it so [#628] closes on the file being absent, and continue ARCHITECTURE.md toward its 15 KB target through [#667]'s render-from-source with bytes reported before and after

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-y-755-docs-cut-finish "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-y-755-docs-cut-finish.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-y-755-docs-cut-finish.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-y-755-docs-cut-finish` — the name that produces `worktree-lane-y-755-docs-cut-finish` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #755 · lane-y-755-docs-cut-finish]`.
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
manual fallback and adds a skip-if-`worktree-lane-y-755-docs-cut-finish`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-y-755-docs-cut-finish` -> branch `worktree-lane-y-755-docs-cut-finish` -> contract `LANE-y-755-docs-cut-finish.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. `protocols/ESSENTIALS.md` is ABSENT from the tree -- deleted, not merely de-registered -- so `[#628]` closes on the file's absence rather than on its de-registration. It was 16,461 B and tracked at freeze, already retired from five registries.
2. `ARCHITECTURE.md` continues toward its <= 15 KB target through `[#667]`'s render-from-source, with bytes reported BEFORE and AFTER (100,800 B at freeze, already down 22% from 129,213 B).
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

1. Delete `protocols/ESSENTIALS.md` and follow every surface the deletion breaks until each is green. **COMMIT**
2. Continue `ARCHITECTURE.md` toward <= 15 KB via `[#667]` render-from-source, recording bytes before and after. **COMMIT**
3. Confirm `[#628]` closes on the file's ABSENCE; file or amend row `[#755]`. **COMMIT**
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
