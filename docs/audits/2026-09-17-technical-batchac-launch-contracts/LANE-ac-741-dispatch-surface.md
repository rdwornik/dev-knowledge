# LANE lane-ac-741-dispatch-surface — Measure where the dispatch verb lives, whether a launch verb can carry a non-Claude model, and what moving it to the hub would cost in lanes

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Organs and rows

**`organs:`** -- the organ(s) this lane MUST use. Before writing ANY query or ordering ANY scan, NAME THE ORGAN THAT ALREADY ANSWERS IT. New code ONLY for what no organ answers, and FILE THE GAP AS A ROW when that happens. **A lane that could have used an organ and did not MUST say so in its handback.**

- `file_purpose_graph.py why <path>` (FPG-1) -- where a file lives, what it relates to, who triggers it
- `graph_queries.py process-list --render` / `stats` -- the process roster and its counts
- `gen_task_tree` over `tasks/` -- the BACKLOG row index (NEVER a raw grep of BACKLOG.md)
- `ecosystem/organ-index.md` -- the generated organ roster

**`rows:`** -- the open row(s) this lane's subject already belongs to, resolved against the live index at freeze. A lane whose subject already has a row is RE-SCOPED to that row rather than duplicating it.

- `[#741]` PRIMARY -- lane launching is methodology, so the hub owns it; this lane produces its fact-read
- `[#509]` -- `Invoke-Dispatch.ps1` resolves `CLAUDE_PROMPTS_DIR`
- `[#582]` -- the substrate router
- `[#604]` -- admitting win-tooling to the deploy registry

**Library ladder** for anything genuinely new: stdlib > established dependency > proven project > industry pattern; hand-roll only on a MEASURED divergence, recorded so it is not relitigated.

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
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-ac-741-dispatch-surface "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-ac-741-dispatch-surface.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-ac-741-dispatch-surface.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-ac-741-dispatch-surface` — the name that produces `worktree-lane-ac-741-dispatch-surface` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #741 · lane-ac-741-dispatch-surface]`.
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
manual fallback and adds a skip-if-`worktree-lane-ac-741-dispatch-surface`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-ac-741-dispatch-surface` -> branch `worktree-lane-ac-741-dispatch-surface` -> contract `LANE-ac-741-dispatch-surface.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **1a** answered with evidence: the repo and path the dispatch verb PHYSICALLY resolves to, with the command that resolved it quoted.
2. **1b IS RE-SCOPED AND THE RE-SCOPE IS BINDING.** `[#740]` is **CLOSED** (2026-09-16, evidence `f903a24`) -- verified against the live index at this batch's freeze. Do **NOT** re-open it and do NOT "close it on the measurement": there is nothing open to close. Instead measure whether `[#675]` clause 1's generator-to-verb conformance assertion (AX25-2) is GREEN today, and report which of the two explanations holds for the six lanes that ran last window -- they came through the generator, or they did not.
3. **1c** answered UNCONDITIONALLY, whatever 1a returns: can a launch verb carry a NON-CLAUDE model at all? `to-cc/run-lane-copilot.ps1` was hand-written because none existed; say whether that is still true, with the witness.
4. **1d** answered: the verb's contents SPLIT into what is METHODOLOGY (hub-owned, OS-independent) versus what is MACHINE-LOCAL (paths, drive letters, this workstation's specifics -- win-tooling). Itemised, not summarised.
5. **1e** answered: what moving it to the hub would COST, expressed **IN LANES**.
6. The report is committed to `docs/audits/` under the date-slug convention as an **AUDIT-class artifact** -- NOT `logs/`, which is for machine-regenerated digests only -- and is FRAMED AS EVIDENCE FOR `[#741]` `[#509]` `[#582]` `[#604]`, never as a request for a second integrator.
7. **THIS LANE GATES L6.** The handback states, in ONE explicit line, whether the dispatch verb resolves INSIDE this repo. The dispatcher reads that line and boots L6 or does not -- there is no human in the loop, so an ambiguous line is a lane failure.
8. READ-ONLY on the dispatch verb: this lane MEASURES it and does not mutate it (order §6). Docs in English; hyphen-only names; logging rather than print; `pytest` green.

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

1. Resolve 1a with the organs named above BEFORE any raw scan; if an organ could have answered a question you grepped, say so in the handback (§4). **COMMIT**
2. Answer 1b (re-scoped), 1c, 1d, 1e with evidence per item. **COMMIT**
3. Write the audit artifact under `docs/audits/`, framed as evidence for the four rows, with the L6 gate line stated explicitly. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
