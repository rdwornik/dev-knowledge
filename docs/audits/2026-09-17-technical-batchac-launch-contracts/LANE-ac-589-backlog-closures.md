# LANE lane-ac-589-backlog-closures — Execute the 25 witness-backed closures and file the acceptance-test and per-task execution-state carrier rows

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Organs and rows

**`organs:`** -- the organ(s) this lane MUST use. Before writing ANY query or ordering ANY scan, NAME THE ORGAN THAT ALREADY ANSWERS IT. New code ONLY for what no organ answers, and FILE THE GAP AS A ROW when that happens. **A lane that could have used an organ and did not MUST say so in its handback.**

- `gen_task_tree` -- the row index and the `--close-row` verb; NEVER hand-edit `BACKLOG.md`, which is generated
- `decision_coverage.py check` -- decision-to-row coverage
- `graph_queries` orphan census -- a process no wiring surface reaches

**`rows:`** -- the open row(s) this lane's subject already belongs to, resolved against the live index at freeze. A lane whose subject already has a row is RE-SCOPED to that row rather than duplicating it.

- `[#589]` PRIMARY -- the BACKLOG view projection and its 72,000 B bar
- **FILES `[#889]`** -- the acceptance-test row
- **FILES `[#890]`** -- the per-task execution-state carrier row

**Library ladder** for anything genuinely new: stdlib > established dependency > proven project > industry pattern; hand-roll only on a MEASURED divergence, recorded so it is not relitigated.

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
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-ac-589-backlog-closures "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-ac-589-backlog-closures.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-ac-589-backlog-closures.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-ac-589-backlog-closures` — the name that produces `worktree-lane-ac-589-backlog-closures` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #589 · lane-ac-589-backlog-closures]`.
**The model is ON the line, not defaulted** (`[#717]`): it is rendered from the
routing table above, so this lane dispatches at `sonnet` whatever any
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
manual fallback and adds a skip-if-`worktree-lane-ac-589-backlog-closures`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-ac-589-backlog-closures` -> branch `worktree-lane-ac-589-backlog-closures` -> contract `LANE-ac-589-backlog-closures.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The 25 identified closures are executed, **EACH with its witness named**. A closure with no witness is not executed -- it is reported as un-witnessed and left open.
2. **`[#889]` is filed** -- the acceptance-test row. Its Done-when is intake 103 §0.6 **VERBATIM**: *"one lane runs end to end, dispatch to merged, in under one hour, with nothing wedged and no human decision in the middle"* -- PLUS one sentence: **the result names the set of guards armed while the measurement ran.**
3. **`[#890]` is filed** -- the PER-TASK EXECUTION STATE carrier row.
4. **THE TWO IDS ARE ALREADY RESERVED BY PUSH** (`refs/reservations/task-id/889` and `/890`, holder `lane-ac-589-backlog-closures`). **Do NOT run the allocator and do NOT read a local maximum** -- use 889 and 890 as given. Allocating again would burn ids and reading a local maximum is the `[#804]` defect.
5. **BACKLOG bytes AND row count** are reported against the `[#589]` **72,000 B** bar. Report the measured numbers; do not restate a count from prose.
6. Docs and code in English; hyphen-only names; logging rather than print; `pytest` green.

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

1. Enumerate the 25 closures and resolve each one's witness BEFORE closing anything; a closure whose witness does not resolve is dropped from the set and reported. **COMMIT**
2. Execute the witnessed closures via `gen_task_tree`'s close verb, never by hand-editing the generated view. **COMMIT**
3. File `[#889]` and `[#890]` at the reserved ids. **COMMIT**
4. Measure and report BACKLOG bytes and row count against the 72,000 B bar. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
