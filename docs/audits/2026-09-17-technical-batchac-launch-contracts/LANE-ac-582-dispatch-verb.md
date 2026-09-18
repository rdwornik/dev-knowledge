# LANE lane-ac-582-dispatch-verb — CONDITIONAL on L1 item 1a - build the non-Claude launch path and wire ADR-110 manifest refusal into the dispatch verb

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Organs and rows

**`organs:`** -- the organ(s) this lane MUST use. Before writing ANY query or ordering ANY scan, NAME THE ORGAN THAT ALREADY ANSWERS IT. New code ONLY for what no organ answers, and FILE THE GAP AS A ROW when that happens. **A lane that could have used an organ and did not MUST say so in its handback.**

- `file_purpose_graph.py why <path>` (FPG-1) -- file relationships
- the substrate router per `[#582]`, **if it exists** -- establish that before assuming it

**`rows:`** -- the open row(s) this lane's subject already belongs to, resolved against the live index at freeze. A lane whose subject already has a row is RE-SCOPED to that row rather than duplicating it.

- `[#582]` PRIMARY -- substrate router: one gated enum, a capability-keyed table, and the generator that reads it
- `[#741]` -- lane launching is methodology, so the hub owns it (the ownership question this lane must not pre-empt)
- `[#675]` -- carries AX25-2, the generator-to-verb conformance test

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
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-ac-582-dispatch-verb "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-ac-582-dispatch-verb.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-ac-582-dispatch-verb.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-ac-582-dispatch-verb` — the name that produces `worktree-lane-ac-582-dispatch-verb` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #582 · lane-ac-582-dispatch-verb]`.
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
manual fallback and adds a skip-if-`worktree-lane-ac-582-dispatch-verb`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-ac-582-dispatch-verb` -> branch `worktree-lane-ac-582-dispatch-verb` -> contract `LANE-ac-582-dispatch-verb.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **GATE -- READ THIS FIRST. THIS LANE BOOTS ONLY IF L1's item 1a reports the dispatch verb resolves INSIDE THIS REPO.** The dispatcher reads L1's handback and boots this lane or does not; **there is no human decision**. **IF L1 REPORTS ANOTHER REPO, THIS LANE IS NOT BOOTED** -- the build is carried by `[#741]` with L1's report as its input. Do **not** create a worktree in a second repo and do **not** commit there.
2. **(a)** The non-Claude launch path is built. This is the only item in the batch that moves 99.47% Opus.
3. **(b) P5** -- ADR-110's manifest refusal is wired into the verb. Today only `/lane-boot` refuses.
4. **Codex terra review is MANDATORY before merge** for this lane -- not optional, not at the integrator's discretion.
5. **AX25-4 bounds this lane: do not gold-plate the retiring PowerShell path.** Work is bounded to AX25-2's conformance test plus whatever conductor E's runner needs; everything else waits for E.
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

1. **Verify the gate**: confirm from L1's handback that the verb resolves inside this repo. If it does not, STOP immediately and report -- do not proceed to step 2. **COMMIT** (the stop is itself the artifact)
2. Build (a), the non-Claude launch path. **COMMIT**
3. Wire (b), the ADR-110 manifest refusal into the verb. **COMMIT**
4. Request the mandatory Codex terra review; land its findings or record the refusal. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
