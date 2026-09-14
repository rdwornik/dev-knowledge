# LANE lane-y-750-merge-receipts — Make /lane-integrate write a kind=merge receipt per merge with wall, test and ceremony minutes, judged COMPLETE on the suite step's verdict STATE (PASS or PRE-EXISTING) per ruling AY1-1 rather than on its exit code, refuse a merge that lands without one, and fix wall_seconds recording serial rather than wall time

| Model | Mode | Effort |
|---|---|---|
| opus | execute | xhigh |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort xhigh --permission-mode bypassPermissions --worktree lane-y-750-merge-receipts "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-y-750-merge-receipts.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-y-750-merge-receipts.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-y-750-merge-receipts` — the name that produces `worktree-lane-y-750-merge-receipts` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #750 · lane-y-750-merge-receipts]`.
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
manual fallback and adds a skip-if-`worktree-lane-y-750-merge-receipts`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-y-750-merge-receipts` -> branch `worktree-lane-y-750-merge-receipts` -> contract `LANE-y-750-merge-receipts.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. `/lane-integrate` writes a `kind=merge` receipt for EVERY merge, carrying wall, test and ceremony minutes; a merge that lands without one is REFUSED. RED-first: the witness that a receipt-less merge fails exists and is red before the enforcing code does.
2. Completeness is judged on the suite step's recorded verdict STATE, per ruling AY1-1 -- `PASS` or `PRE-EXISTING` is COMPLETE with the state recorded BY NAME on the receipt; `REGRESSED`, or a verdict that cannot be read, is INCOMPLETE and refuses the merge. Forcing the suite step to exit 0 is ruled out BY NAME as `[#744]`'s false pass. Separately, `wall_seconds` records WALL time, not serial time (witness: a step-7 span of 3h01m recorded as 1.776 s).
3. DECLARED FOOTPRINT — `scripts/merge_receipt.py` and `.claude/commands/lane-integrate.md`. This lane is the SOLE OWNER of `scripts/merge_receipt.py` for batch Y; `[#752]` is sequenced behind it on that file and does not open it until this lane's branch has landed.
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

1. RED-first witnesses, failing before any build code: a merge with NO receipt fails; a receipt whose suite step is `REGRESSED` fails; a receipt whose suite step is `PRE-EXISTING` PASSES. **COMMIT**
2. In `scripts/merge_receipt.py`: record the suite step's verdict state by name, re-point `Receipt.incompleteness_reason()` leg 3 at that state instead of the flattened `ok` boolean, and fix `wall_seconds` to record wall time. **COMMIT**
3. Wire the refusal into `/lane-integrate` (`.claude/commands/lane-integrate.md`), then file or amend row `[#750]` in this lane's FIRST commit. **COMMIT**

**Declared footprint:** `scripts/merge_receipt.py` · `.claude/commands/lane-integrate.md`. This lane is the SOLE OWNER of `scripts/merge_receipt.py` for batch Y; `[#752]` is sequenced behind it on that file.
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
