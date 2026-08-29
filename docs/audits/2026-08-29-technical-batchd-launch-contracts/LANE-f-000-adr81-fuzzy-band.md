# LANE lane-f-000-adr81-fuzzy-band — Design the non-binary acceptance shape ADR-81 section 45 defers to its own arc, exercised on two real fuzzy artifacts.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `cloud` — an off-machine lane, repo-bound and receipt-gated, on the `claude/` prefix.

```
Dispatch-CloudV2 LANE-f-000-adr81-fuzzy-band.md -Title 'lane-f-000-adr81-fuzzy-band'
```

The operator runs the line above verbatim. The **whole file is the brief** — it
travels in a JSON body, so one file is one lane and never a multi-lane bundle —
and the dispatch binds Revision `main`. `Dispatch-CloudV2` carries no `-Effort`
parameter, so this lane's tier is on the record in the routing table above
(`opus` / `high`) rather than on the command line. Permission
mode is `bypassPermissions`, as it is for an on-machine lane.
A cloud session clones from `origin`, so every input this contract names is
pushed before dispatch: it cannot see an unpushed branch or a local file.

## Worktree pairing

slug `lane-f-000-adr81-fuzzy-band` -> branch `claude/lane-f-000-adr81-fuzzy-band` -> contract `LANE-f-000-adr81-fuzzy-band.md`

One lane = one contract file = one branch, so an open lane resolves to the
contract that created it and an orphan is attributable at a glance (ADR-110,
fifth per-lane requirement). A cloud lane runs on the `claude/` prefix, not `worktree-`: the branch is created
by the cloud transport, not by a local worktree provisioner.

## Receipt gate

This lane runs off-machine, so it carries a receipt (`protocols/STANDING_RULINGS.md` Q5).
Both fields, checked as a conjunction — either one alone reports a success the other refutes:

- `git-source-resolves-non-empty:` `<the resolved git source, non-empty>`
- `first-assistant-text-echoed:` `<the session's first assistant text, echoed back>`

A dispatch missing either half is treated as not having started, and is
re-dispatched. The lane also branches fresh off `origin/main` and leaves files it
did not author and this contract does not name exactly as found (Q4).

## Write-scope (frozen)

`docs/decisions/**` (one new ADR) · `docs/intake/**`

Design happens on CLOUD; the landing act is CC's from the primary checkout. **Merges LAST** — it
consumes lane-e's census.

## Done-contract (immutable)

1. **A non-binary acceptance shape** for the band ADR-81 §45 explicitly defers: *"decks, prose,
   judgment artifacts where closure cannot be an exact pass/fail"*, deferred there *"to its own
   arc"*. This is that arc; at freeze,
   `grep -rn "fuzzy" tasks/ docs/decisions/` returns no other owner.
2. **Exercised on >=2 REAL fuzzy artifacts from this repo's own corpus** — not invented examples.
   An acceptance shape never run against a real artifact is a proposal, not a shape.
3. The ADR states what it does NOT cover, so the deterministic band ADR-81 already binds is not
   quietly re-litigated.
4. Prose in English; hyphen-only names. **This lane runs NO gate and asserts none** — it is
   read-only by contract, so it carries no test leg and has no gate result to report. A cloud
   image may carry the wrong `uv`; if anything is run at all, invoke `python3` directly and
   **declare that you did**. Never report a gate result you did not observe.

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

1. Read ADR-81 §45 and the two chosen fuzzy artifacts; draft the acceptance shape.
2. Exercise the shape against both artifacts and record where it fails or is ambiguous — negative
   results are first-class here.
3. Print the design in full as the final message; the ADR is landed by the integrator.

Gate note: a cloud image may carry the wrong `uv`; invoke `python3` directly and **declare that
you did**.

## What NOT to do

- No merges, no pushes to `main`, no touching another lane's branch — commit-and-STOP;
  integration is the integrator's act, from the primary checkout.
- No JOURNAL entry — that is the integrator's surface (`protocols/STANDING_RULINGS.md` P-1).
- No index regeneration — the integrator is gate-of-record and regenerates once
  at the merge (Q1); a lane declares its single-hook bypass in the commit body.
- No edits outside this lane's declared footprint.
