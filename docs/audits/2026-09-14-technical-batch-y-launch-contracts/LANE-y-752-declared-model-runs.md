# LANE lane-y-752-declared-model-runs — Resolve a contract's declared model into flags the background launcher actually honours, verify the ran-model off the lane's own transcript, and refuse a receipt whose ran-model differs from its ordered-model

| Model | Mode | Effort |
|---|---|---|
| opus | execute | xhigh |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
claude --bg --model opus --effort xhigh --permission-mode bypassPermissions --worktree lane-y-752-declared-model-runs "Read and execute the frozen contract at $env:CLAUDE_PROMPTS_DIR\LANE-y-752-declared-model-runs.md"
```

**The operator does NOT type the line above.** He types
`dispatch LANE-y-752-declared-model-runs.md` **from the target repo root** — the ruled verb for a local
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
and `--worktree lane-y-752-declared-model-runs` — the name that produces `worktree-lane-y-752-declared-model-runs` and with it
the ADR-110 pairing and the merge exemption. Board label `[.dev-knowledge · #752 · lane-y-752-declared-model-runs]`.
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
manual fallback and adds a skip-if-`worktree-lane-y-752-declared-model-runs`-exists guard the verb path does
not have; that guard's job is done earlier and more broadly at STEP 0 by
`seat_refusals lane-ceiling --check-worktrees`, which reads the live worktree
list before the first worktree exists.

## Worktree pairing

slug `lane-y-752-declared-model-runs` -> branch `worktree-lane-y-752-declared-model-runs` -> contract `LANE-y-752-declared-model-runs.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. The dispatcher resolves a contract's declared mode into flags the background launcher actually honours, and `opusplan` is never emitted onto a `--bg` line -- the witnessed no-op is `lane-x-689`, which ordered opusplan and ran sonnet-5, making every routing decision in that window advisory.
2. The ran-model is read off the lane's OWN transcript, and a receipt whose ran-model differs from its ordered-model is REFUSED. RED-first: ordered-not-equal-ran fails before the check that enforces it exists.
3. DECLARED FOOTPRINT — `scripts/dispatch_surface.py` and `scripts/routing_agreement.py` immediately, and `scripts/merge_receipt.py` LAST, for the ordered-not-equal-ran refusal. This lane is SECOND on `scripts/merge_receipt.py`: `[#750]` owns it and is rewriting its completeness predicate, so this lane does not open that file until `[#750]` has LANDED on `main` and verifies it before its first write there.
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

1. RED-first: a receipt whose ran-model differs from its ordered-model is refused, and a `--bg` line carrying `opusplan` is refused. **COMMIT**
2. Implement mode-to-flag resolution for the background launcher and the ran-model read off the lane transcript. **COMMIT**
3. File or amend row `[#752]`. **COMMIT**

**Declared footprint:** `scripts/dispatch_surface.py` · `scripts/routing_agreement.py` · and, LAST, `scripts/merge_receipt.py` for the ordered-not-equal-ran refusal.

**SEQUENCING, NOT OPTIONAL — this lane is SECOND on `scripts/merge_receipt.py`.** `[#750]` owns that file for batch Y and is rewriting its completeness predicate; this lane does not open it until `[#750]`'s branch has LANDED on `main`, and verifies that before its own first write there. Steps 1 and 2 touch the dispatcher surface only and may proceed immediately. Recorded because step-0 `file-collision` could NOT see this collision — both contracts originally declared no repo path and the check reported them invisible, so the PASS it returned was vacuous on exactly this pair.
4. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
