# LANE lane-ac-863-notification — Restore the Notification hook with a counter and add an expiry field beside every individually-disabled hook

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

## Organs and rows

**`organs:`** -- the organ(s) this lane MUST use. Before writing ANY query or ordering ANY scan, NAME THE ORGAN THAT ALREADY ANSWERS IT. New code ONLY for what no organ answers, and FILE THE GAP AS A ROW when that happens. **A lane that could have used an organ and did not MUST say so in its handback.**

- `ecosystem/organ-index.md` -- the generated organ roster
- `decision_coverage.py check` -- the `[#886]` linkage
- `fleet_parity.py` -- the parity surfaces the hook set is declared against

**`rows:`** -- the open row(s) this lane's subject already belongs to, resolved against the live index at freeze. A lane whose subject already has a row is RE-SCOPED to that row rather than duplicating it.

- `[#863]` PRIMARY -- owns re-arming the disabled hooks
- `[#886]` -- an emergency change records its temporary debt as DATA with an owner and an expiry; **this row owns the record shape, so this lane adds a FIELD to it and does not invent a rival record**
- `[#888]` -- the repo has no DEGRADED state; the per-hook list is a comment-key register, not a gate-read record

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
claude --bg --model sonnet --effort high --permission-mode bypassPermissions --worktree lane-ac-863-notification "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-ac-863-notification.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-ac-863-notification.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-ac-863-notification` — the name that produces `worktree-lane-ac-863-notification` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #863 · lane-ac-863-notification]`.
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
manual fallback and adds a skip-if-`worktree-lane-ac-863-notification`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-ac-863-notification` -> branch `worktree-lane-ac-863-notification` -> contract `LANE-ac-863-notification.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The **Notification** hook is restored **WITH A COUNTER** recording what it caught, what it cost, and over what window. A restored hook with no counter is NOT done -- §15: every restored mechanism ships with a counter.
2. An **`expiry`** field is added beside every individually-disabled hook's existing `rate` / `owner` / `reenable_when` in `.claude/settings.json`: the `[#886]`-class debt as DATA. **A FIELD ON THE EXISTING RECORD, NOT A NEW RECORD TYPE** -- the no-new-organ rule holds (§15) and `[#886]` owns the record shape.
3. Further hooks are restored **ONLY per family** and **ONLY where B0's measurement clears that family**. A family with no measurement is NOT restored tonight; the handback NAMES each family left alone and why.
4. A gate with no catch in its window is **REMOVED, not tuned** (§15). If a restored hook's counter shows zero catches, say so rather than adjusting its threshold.
5. Docs and code in English; hyphen-only names; logging rather than print; `pytest` green.

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

1. Read the live hook register in `.claude/settings.json` and the `[#886]` record shape BEFORE editing; confirm which families carry a measurement. **COMMIT**
2. Restore Notification with its counter. **COMMIT**
3. Add the `expiry` field to every individually-disabled hook entry. **COMMIT**
4. End-of-lane artifact: what changed, which families were left alone and why, each counter's window. **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
