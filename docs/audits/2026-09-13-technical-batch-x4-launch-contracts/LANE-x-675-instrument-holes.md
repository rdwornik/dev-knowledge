# LANE lane-x-675-instrument-holes — Close the three verified [#675] false-pass holes as rows and fixes, RED-first each -- actions_verdict.py:206 returning PASS when job details cannot be read, seat_refusals.py:303 blind to root-level tracked files in the collision extractor, merge_receipt.py:449 counting receipts with missing or failed steps into the median

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort high --permission-mode bypassPermissions --worktree lane-x-675-instrument-holes "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-x-675-instrument-holes.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-x-675-instrument-holes.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-x-675-instrument-holes` — the name that produces `worktree-lane-x-675-instrument-holes` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #675 · lane-x-675-instrument-holes]`.
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
manual fallback and adds a skip-if-`worktree-lane-x-675-instrument-holes`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-x-675-instrument-holes` -> branch `worktree-lane-x-675-instrument-holes` -> contract `LANE-x-675-instrument-holes.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **THREE rows filed, one per hole**, each with `Done when:` in the **literal colon form** and
   the filing commit carrying a flush-left `kill-candidates:` line. `[#675]` itself **stays
   OPEN** - the operator ruled NO-GO on closing it (ratification item 3); these three are its
   children, not its closure.
2. **`scripts/actions_verdict.py:206` must not return PASS when job details cannot be read.**
   RED-first: a test feeding absent/unreadable/malformed job details and asserting the verdict is
   **not** PASS. An instrument that cannot read its input reports UNKNOWN or fails; **a false
   PASS on a verdict organ is strictly worse than no organ**, because a real gate consumes it.
3. **`scripts/seat_refusals.py:303`'s collision extractor must see root-level tracked files.**
   RED-first: a root-level tracked file that today escapes the extractor and therefore never
   collides. A refusal blind to a whole directory level does not refuse less loudly - it refuses
   wrongly, and silently.
4. **`scripts/merge_receipt.py:449` must exclude receipts with missing or failed steps from the
   median.** RED-first: a receipt set whose median is skewed today by an incomplete receipt. A
   receipt that never finished has no duration to contribute, and folding it in reports a number
   that is not a measurement of anything.
5. **Each fix is RED-first and each lands in its own commit** - the failing test first, in the
   same commit or the one before, never after. A fix that arrives with a test written to match it
   proves nothing about the bug it claims to close.
6. **Resolve all three `file:line` locators before acting on them.** They were read at census
   time and this tree has moved since; a line number is a claim until opened.
7. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; targeted tests green.

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

1. Resolve the three locators; record what each line actually is in THIS tree, and whether the
   described defect is still present at it. If a locator has drifted, fix the locator and say so
   - do not fix a different line that looks similar. **COMMIT** (the record)
2. File the three rows. **COMMIT**
3. `actions_verdict.py` - RED test proving the false PASS, then the fix. **COMMIT**
4. `seat_refusals.py` - RED test proving the root-level blindness, then the fix. **COMMIT**
5. `merge_receipt.py` - RED test proving the skewed median, then the fix. **COMMIT**
6. Final: targeted tests green, `git stash list` empty, end-of-lane artifact naming, per hole,
   the RED witness and the commit that greened it. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.

## Model - CORRECTED AT FREEZE, and the operator may reverse it

**The operator ordered `opusplan` for this lane. It is frozen and dispatched at `opus`.**

`opusplan` is a SPLIT tier that routes Opus to **plan mode**. Every dispatch constant puts a lane
on `--permission-mode bypassPermissions`, which never enters plan mode; with no plan phase there
is no Opus phase, and the tier collapses to its implement half - Sonnet. Nothing warns: the flag
is accepted, and the resolved line reads `--model opusplan` while the session runs Sonnet.

**Re-measured at THIS freeze on the installed CLI (2.1.270), not inherited.**
`claude --print --model opusplan --permission-mode bypassPermissions` produced a session
transcript whose every assistant message records `claude-sonnet-5`. The prior reading -
`docs/audits/2026-09-13-technical-batch-x3-manifest.md` section 6 finding 7, measured on 2.1.224
across 84 assistant messages of a real lane - therefore still holds on the current CLI.

Firing at `opusplan` would deliver Sonnet, a tier the operator did not name either, so there is
no faithful-literal option and **both** choices deviate. `opus` is the one matching intent: the
operator's own gloss for the tier is "Opus plans", and Ch8's routing matrix routes **gate and
organ code** - exactly this lane - to `opus`. This paragraph is the disclosure, not an
authorisation: deviation-with-disclosure does not authorise itself, the operator may reverse it,
and re-firing at another tier is one command.

## Why these three are one lane and not three rows in someone else's

All three are **false PASSes in instruments this repo's own seats read to decide things** - a
CI verdict, a seat refusal, a merge-cost median. They share a failure shape: the organ cannot
obtain its input, and reports success rather than ignorance. The census verified all three; the
operator declined to close `[#675]` on them precisely so they would become rows with witnesses
rather than a closure note.

**A note on `merge_receipt.py` and `actions_verdict.py`:** both are wired to
`.claude/commands/lane-integrate.md` and read as orphans to today's census, which does not count
a command file as a wiring surface. **That question is being filed separately through the
decision engine and is NOT this lane's to answer** - do not add a hook to either module to make
an orphan count fall. A pre-commit trigger is wrong on the merits for both (a stopwatch has
nothing to gate; a merge SHA does not exist at commit time).

## Batch context - X wave 4 (appended at freeze, part of the frozen contract)

**The GO.** `to-browser/RATIFICATION-2026-09-13.md`, the operator's words of 2026-09-13,
recorded the same turn. That file is this lane's authority and the scope bound: the GO covers
these four lanes and no lane outside them fires on it.

**Concurrency 4, no backfill.** All four lanes of this wave fire together. **No lane may wait on
the operator mid-run (AX27-1)** - a lane that would need him is mis-scoped, not brave. Everything
outside V-2 classes (a)/(b)/(c) is decided per contract defaults and REPORTED in the end packet.

**Hazards measured in wave 3 and carried here so they are not rediscovered at cost**
(`docs/audits/2026-09-13-technical-batch-x3-manifest.md` section 6):

- **`graph-rebuild` is NOT concurrency-safe, and this batch runs four concurrent lanes by
  design.** A commit can fail inside `graph_store.py::_swap_into_place` when a sibling lane
  commits at the same moment; the same rebuild run standalone a minute later succeeds. **Retry
  the commit. Do not "repair" the store, and do not read the traceback as a defect in your own
  diff** - its worst property is that it surfaces in an unrelated lane's commit.
- **`uv run --locked` on EVERY test invocation.** A bare `pytest` inside a worktree inherits
  `VIRTUAL_ENV` from the primary tree, imports the PRIMARY checkout's source, and reports green
  about code this lane did not touch - silently (STANDING_RULINGS D4; ADR-106 for the pin).
- **`git stash list` EMPTY at STOP.** `refs/stash` lives in the COMMON git directory, not the
  worktree's private ref space: a stash pushed here survives `git worktree remove`, the branch
  delete and every teardown step, and is findable only by someone who thinks to look.
- **Targeted tests only.** The full suite runs ONCE, at integration (`[#528]`). Run the tests
  covering this lane's diff - `uv run --locked python scripts/impacted_tests.py select --changed <paths>`
  names them.
- **A gate that blocks leaves files STAGED.** Fix the cause and re-commit; do not reach for
  `--no-verify`. Where a bypass is genuinely sanctioned it is ONE named hook, declared in the
  commit body.
