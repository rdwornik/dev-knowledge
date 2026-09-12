# LANE lane-x-675-merge-cost — take the measured 84-minute merge apart and drive median merge under 30 minutes, reported as a number

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-x-675-merge-cost LANE-x-675-merge-cost.md -Effort high -Model opus
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · #675 · lane-x-675-merge-cost]`. **The model is ON the line, not defaulted** (`[#717]`): it
is rendered from the routing table above, so this lane dispatches at
`opus` whatever the surface's own default (`opus`, the
`.dev-knowledge` default per the Ch8 routing matrix) happens to be. A line that
omitted it would silently re-decide the most expensive constant on it.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-x-675-merge-cost` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-x-675-merge-cost` -> branch `worktree-lane-x-675-merge-cost` -> contract `LANE-x-675-merge-cost.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Done-contract (immutable)

1. **FIRST COMMIT, before any mechanism: `[#675]`'s Done-when REPLACES its stale target with the
   measured baseline.** The current Done-when carries a `12 → under 2` minutes-to-merge target
   from an earlier, smaller measurement; the wave-1 measurement supersedes it. The replacement
   baseline is frozen by the operator (2026-09-12) and is transcribed, not recomputed:

   > **84 min wall = 11.3 targeted tests + 72.7 residual ceremony** (itemised views ~90 and ~63,
   > **nothing measured today**).

   The parenthesis is part of the baseline, not commentary: the two itemised views disagree with
   each other and with the wall figure, and **no measurement was taken on 2026-09-12** — so the
   lane inherits a baseline with a known spread rather than a single trusted number, and says so
   whenever it reports against it. This rides this lane's first commit — it is NOT a separate
   lane (operator ruling, same message).

2. **The target, replacing `12 → under 2`, is six things — all six, not a pick-list** (operator,
   2026-09-12, transcribed):
   1. **per-step minutes recorded into the receipt** — the merge stops being one opaque wall
      number and becomes an itemised one, which is the only way the ~90/~63 disagreement above
      ever resolves;
   2. **full suite and index regeneration on GitHub Actions, with the integrator READING the
      result** — not merely running there. A green run nobody reads is not a gate;
   3. **Codex reviews in parallel** — not serially behind the suite;
   4. **the dispatcher REFUSES to fire two lanes whose contracts touch the same file**, with a
      **RED-first** witness — a refusal, at dispatch, in the `seat_refusals.py` STEP-0 family,
      not a warning afterwards;
   5. **review and triage are handed pre-assembled inputs and are NOT cut** — the saving comes
      from removing assembly, never from removing the judgement step;
   6. **median merge under 30 minutes, MEASURED** — a median over a real run of merges, reported
      as a number, against the baseline in clause 1.

3. Docs and code in English; hyphen-only names; logging rather than print;
   Click for a CLI where one is warranted; `pytest` green.

## The one clause that is a REFUSAL, and where it has to sit

Target 2.4 — *the dispatcher refuses to fire two lanes whose contracts touch the same file* — is
the only target here that is a gate rather than a measurement, and its placement is the whole
mechanism. It belongs in the **STEP 0 refusal family** (`scripts/seat_refusals.py`, alongside
`lane-ceiling`, `carried-by`, `sleeping-poll`, `dryrun-step0`), evaluated **on the frozen
contract set before the first worktree exists**.

Run later — after provisioning, or as an observation in the integrator's first report — it is
decorative: the collision cost the refusal exists to prevent has already been paid, and the
remaining options are all teardowns. This is `lane-ceiling`'s own placement rule, and it is
quoted here because the identical mistake is available.

**Honest limit, stated so the lane does not overclaim:** a contract declares the files it
*intends* to touch. A refusal built on that declaration catches declared collisions only; a lane
that writes outside its declared footprint is a different defect with a different owner. Say so
in the end packet rather than implying the refusal is total.

## Carried rows and clauses (verbatim — AX12-1)

### `AX23-3` clause 1 — verbatim

> **AX23-3 · Wave 2, re-ordered by measured cost:** (1) `[#675]` merge cost — 87 % of an
> 84-minute merge is ceremony, now measured; Done-when carries the split and a target;

### `AX23-5` — verbatim (the metric this lane is measured on)

> **AX23-5 · Recorded:** wave 1 delivered five mechanisms and zero subtraction; the window
> stands at +47 rows filed, 4 closed. The next wave is measured on bytes removed, rows closed
> and merge minutes — not on rows filed.

### `AX24-1` — verbatim (this lane's position in the order)

> **AX24-1 · No new X2 lane until the finished work is banked.** Order: merge x-691 (routing
> Half A) → close the six witnessed rows → the fail-open fix (AX24-2) → `[#675]` merge cost →
> X-DEL second attempt. Everything else in wave 2 waits.

### Row `[#675]` — the Done-when leg clause 1 replaces, verbatim

> and a **text-only diff takes a SINGLE-COMMIT path with its anchor in the same commit**, which
> requires the anchor predicate to admit an entry that names its own commit for that class —
> taking **minutes-to-merge from the measured 12 to under 2**, reported as a number rather than
> asserted

The other three legs of `[#675]`'s Done-when — type-discriminated node access, the RED-first
heterogeneous-list witness, and the size gate refusing worktree provisioning for a
`BACKLOG.md`/`tasks/`-only contract — are **untouched by clause 1 and remain in force**. Only the
minutes-to-merge target is replaced.

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

**Not escalation classes here, decided in advance:** the baseline numbers (frozen, clause 1);
which six targets are in scope (all of them, clause 2); and where the collision refusal sits
(STEP 0, above). **A genuine class (b) IS available and should be taken if it appears:** target
2.2 moves the suite to GitHub Actions, and `[#689]`'s conductor-E row is the organ that would
run it — if this lane finds the two in conflict, that is a rule-vs-ruling escalation, not a
silent merge of the two rows.

## Steps

1. Replace `[#675]`'s minutes-to-merge target per clause 1, leaving its other three legs intact.
   **COMMIT** (first commit; the row edit precedes the mechanisms it governs).
2. Build target 2.1 — per-step minutes into the receipt — and use it to itemise one real merge,
   which is what makes every later number comparable. **COMMIT**
3. Build target 2.4 — the same-file collision refusal — RED-first, in the STEP 0 family.
   **COMMIT**
4. Targets 2.2, 2.3 and 2.5: Actions-hosted suite and index regen with the integrator reading
   the result; Codex reviews in parallel; review and triage handed pre-assembled inputs.
   **COMMIT** each.
5. Final: measure target 2.6 — median merge minutes over the runs available — and report it as
   a number against clause 1's baseline, **naming the spread rather than hiding it**. `pytest`
   green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then
   STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
- **Do not reach the 30-minute median by cutting review or triage.** Target 2.5 exists precisely
  to forbid that trade, and a median hit that way is a false pass on this row.
- **Do not report a median without its spread.** Clause 1's baseline has a known ~90-vs-~63
  disagreement and nothing measured on the day it was frozen; a single confident number
  reported against it repeats the defect this row is about.
