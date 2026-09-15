# LANE lane-z-10-aj-m04-first-pass -- First pass over the AJ M04 course material on local disk: a SHIPPED / OWNED / UNOWNED matrix, with every UNOWNED becoming a row

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` -- a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-z-10-aj-m04-first-pass "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-z-10-aj-m04-first-pass.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-z-10-aj-m04-first-pass.md` **from the target repo root** -- the ruled verb for a local
lane (PLAYBOOK Ch8's dispatch table, the sole literal-command site). The verb
reads this `## Dispatch` block and runs it **verbatim**, substituting exactly
one literal -- `$env:CLAUDE_PROMPTS_DIR` -- which is how a frozen contract
names its own location without hard-coding an absolute path. That spelling is
load-bearing: it is the only token the reader replaces, and any other
placeholder is passed through untouched into a real session's prompt.
The repo root still matters: the worktree
is created relative to the current repo, so dispatching from the wrong one
lands the lane in it.

The line carries every dispatch constant rather than defaulting it:
`--permission-mode bypassPermissions` (a `--bg` lane has nobody to answer a
permission prompt, so a default would stall it silently), `--bg`,
and `--worktree lane-z-10-aj-m04-first-pass` -- the name that produces `worktree-lane-z-10-aj-m04-first-pass` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · lane-z-10-aj-m04-first-pass · lane-z-10-aj-m04-first-pass]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `opus` whatever any
surface default (`opus`, the `.dev-knowledge` default per the Ch8
routing matrix) happens to be. A line that omitted it would silently re-decide
the most expensive constant on it. Effort is a closed enum:
{low | medium | high | xhigh | max}; a value outside it is refused with the enum named,
rather than guessed.

**The `claude` head token is required, not stylistic** (`[#675]` clause 1 /
AX25-2). The verb refuses any other program -- *"this script never runs an
arbitrary command from a contract file"* -- so a contract's `## Dispatch` block
is not a place to name a helper. Until 2026-09-12 this generator emitted the
deprecated `Dispatch-Lane` alias here and **every contract it produced was
refused by the verb meant to launch it**. That alias still resolves as the
manual fallback and adds a skip-if-`worktree-lane-z-10-aj-m04-first-pass`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-z-10-aj-m04-first-pass` -> branch `worktree-lane-z-10-aj-m04-first-pass` -> contract `LANE-z-10-aj-m04-first-pass.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE -- the flag takes the bare lane
name.

## Done-contract (immutable)

1. A matrix: every item SHIPPED with its commit, OWNED with its row id, or UNOWNED. The three states are exhaustive and every item lands in exactly one.
2. Every UNOWNED item becomes a filed BACKLOG row in this lane -- the matrix is not complete while an UNOWNED item has no row.
3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## Decision budget

**V-2 -- this lane escalates on three classes only.** Everything else is decided per
contract defaults and reported in the end packet rather than asked
(`protocols/STANDING_RULINGS.md` "The decision budget"):

- **(a)** curated-baseline touches
- **(b)** genuine rule-vs-ruling conflicts
- **(c)** fork classes with no standing ruling

A lane that discovers a refuted premise PAUSEs with the fact (Q10):
deviation-with-disclosure is not a license -- the disclosure discharges the reporting
duty, it does not authorise the deviation.

## Steps

1. File or amend this lane's own BACKLOG row FIRST. **COMMIT**
2. Locate the M04 material on local disk and record its path in the end-of-lane artifact. It is NOT in the repo -- that is precisely why this lane is LOCAL. Use `agy` as reader. **COMMIT**
3. Build the SHIPPED / OWNED / UNOWNED matrix, resolving each claim to a commit or a row id BEFORE recording it -- an unresolved locator is a claim, not evidence. **COMMIT**
4. File a row for every UNOWNED item. **COMMIT, then STOP.**
5. Final: targeted tests for THIS lane's diff (`uv run --locked pytest`), one end-of-lane artifact (what changed - proposed diffs - open items), `git stash list` EMPTY, **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch -- commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry -- that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration -- the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
