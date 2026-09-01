# LANE lane-f-6-agy-admission — run the agy route against the SDA-1 analysis pack and rule its analysis-role admission, or refuse it on evidence

| Model | Mode | Effort |
|---|---|---|
| sonnet | execute | high |

**No-consumer:** a frozen lane contract is consumed by its DISPATCH and by the batch manifest that enumerates its slug, never by a governance-surface citation — and its filename carries no `YYYY-MM-DD` prefix, so neither `consumer_at_landing` token regex could resolve a citation even if one existed. Declared per that check's own escape.

## Dispatch

**Shape:** `local` — a background lane on the operator's machine, own worktree, commit-and-STOP.

```
Dispatch-Lane lane-f-6-agy-admission LANE-f-6-agy-admission.md -Effort high
```

The operator runs the line above verbatim, **from the target repo root** — the
helper is cwd-bound, and dispatching from the wrong repo lands the worktree in
it. Dispatch constants ride the line without being re-decided:
`--permission-mode bypassPermissions`, `--bg`, and the board label
`[.dev-knowledge · lane-f-6-agy-admission · lane-f-6-agy-admission]`. Model defaults to `opus` — the `.dev-knowledge`
default per the Ch8 routing matrix — and this lane dispatches at `sonnet`.
Effort is a closed enum: {low | medium | high | xhigh | max}; a value outside it is refused
at the surface with the enum named, rather than guessed. The helper refuses
outright when `worktree-lane-f-6-agy-admission` already exists, so re-running the line is a no-op
rather than a collision.

## Worktree pairing

slug `lane-f-6-agy-admission` -> branch `worktree-lane-f-6-agy-admission` -> contract `LANE-f-6-agy-admission.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). The `worktree-` prefix is applied exactly ONCE — the flag takes the bare lane
name.

## Write-scope (frozen)

- `tasks/627-agy-route-is-inert-no-row-authorizes-analysis-admission.md`
- `docs/audits/2026-09-01-technical-agy-admission-verdict.md`

## Done-contract (immutable)

1. **The agy route is RUN against the SDA-1 analysis pack and a verdict is recorded** — admit
   it to the analysis role, or refuse it, on measurement. `[#627]`'s finding is that the route is
   INERT: the token policy promises what nothing gates, and no row authorizes the admission.
2. **The verdict is an artifact, not a gate.** This lane rules; it does not wire an organ. If the
   verdict is ADMIT, what it produces is the evidence an admission act would cite — the act
   itself is a later, separately-ruled change.
3. **A refusal is a first-class outcome** and is recorded with the same care as an admission. An
   evaluation that can only say yes is not an evaluation.
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

1. `/preflight` `[#627]` and locate the SDA-1 analysis pack before running anything.
   **COMMIT**
2. Run the route against the pack. Record what it did, verbatim, including any soft-denial —
   `agy --print` is known to soft-deny filesystem tools. **COMMIT**
3. Write the verdict artifact and update `[#627]` to point at it. **COMMIT**
3. Final: `pytest` green, one end-of-lane artifact (what changed · proposed diffs · open items), **COMMIT, then STOP.**

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
