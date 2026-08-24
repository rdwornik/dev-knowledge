---
intake-id: 44
status: READY
origin: integrator, 2026-08-24 batch close; measured directly against ecosystem/disposition-register.yaml
---

# The disposition register's `ref` and `match` fields have no schema, and both are drifting

## Problem / motivation

`ecosystem/disposition-register.yaml` suppresses known-benign ship-gate WARNs. Two of its three
load-bearing fields are used inconsistently, and the register's own header already rules how one
of them should work — the rule is simply not enforced.

**Measured 2026-08-24 against the live file (30 entries):**

**(a) `ref` points at a backlog ROW rather than at the ruling that makes the WARN benign.**
- **24 of 30 entries** carry a `ref` naming a backlog row: **18** name `#241`, **6** name
  `[#532]/A9`.
- **`[#532]` is CLOSED.** Six live suppressions therefore rest on a row that no longer exists as
  an open commitment, which is the orphan class ruling **P-2**
  (`protocols/STANDING_RULINGS.md:1811`, *"Anti-orphan ratification"*) exists to close.
- **`#241` is OPEN**, so those 18 are not orphaned today — but they will orphan silently the day
  it closes, with no organ to notice.
- A row is a unit of *work*; a ruling is what makes a WARN *benign*. Closing the work does not
  make the WARN un-benign, so keying on the row conflates two different lifetimes.

**(b) `match` keys on a MEASURED VALUE rather than on identity, and the register's own header
forbids exactly this.** The header rules: *"KEY ON THE SPECIFIC BENIGN SIGNATURE (e.g. the
commit sha), NOT a bare id, so a DIFFERENT future drift on the same id re-surfaces and blocks
(precision-over-recall)."* Six entries instead embed a character count:

```
backlog-row-length BACKLOG#546 (2227 chars     backlog-row-length BACKLOG#533 (4210 chars
backlog-row-length BACKLOG#547 (2099 chars     backlog-row-length BACKLOG#529 (2001 chars
backlog-row-length BACKLOG#552 (3576 chars     backlog-row-length BACKLOG#530 (1871 chars
```

A char count is not a signature — it is a *measurement of the thing being suppressed*. Edit the
row by one character and the disposition silently stops matching; the WARN returns and reads as
new drift. The failure is invisible: the register's ADR-75 decoration surfaces a stale entry,
but a *near-miss* entry looks identical to a working one until the WARN reappears.

**Discrepancy recorded rather than smoothed over:** the batch contract stated *"`[#532]/A9` is
closed while 20 WARNs cite it, so P-2 is violated twenty times over"* and *"6 of 30 … 3 already
dead, against 0 of 24"*. The direct measurement above gives **6** entries citing `[#532]/A9`,
not 20, and **18** citing the open `#241`. The 24 figure survives, but as *entries keyed on a
row rather than a ruling*, which is a different claim. The defect class is real and arguably
broader than stated; the specific count in the contract is not reproducible.

## Scenarios (+1 view)

- Someone trims `BACKLOG#546` by two characters for clarity. Its disposition stops matching, a
  WARN returns, and the next window triages it as new drift.
- `#241` closes. Eighteen suppressions orphan in one commit. Nothing fires.
- A reviewer asks *why* a WARN is benign and follows `ref` to a closed row whose text describes
  work, not a judgement.

## Functional requirements

- **Must:** `ref` names the artifact that establishes benignity — a ruling, ADR, or dated
  decision record — not (or not only) a work row.
- **Must:** `match` keys on identity. For the row-length class: `backlog-row-length BACKLOG#<id>`.
- **Should:** an organ notices a `ref` naming a closed/absent row, as P-2 requires.
- **Could:** a schema module for the register, as `ecosystem/schema/provider_registry.py` is for
  the provider registry — the precedent shipped this same batch by lane L1.

## Acceptance criteria (ex-ante)

1. No live entry's `match` embeds a measured value; a mutation test proves a one-character edit
   to a suppressed row does not break its disposition.
2. Every `ref` resolves to a live artifact, or the entry is surfaced.
3. The register's header rule is machine-asserted rather than prose-only.

## Non-goals

- Re-deciding whether any specific WARN is benign.
- Removing the `#241` dispositions while `#241` is open.

## Impact sketch (4+1 lite)

- **Logical:** separates "the work" from "the judgement", which is the actual bug.
- **Process:** ship-gate triage stops re-litigating WARNs that were already dispositioned.
- **Development:** a schema + a check; the provider-registry pair is the shape to copy.
- **Physical:** `ecosystem/disposition-register.yaml`, plus a schema module and a gate.

## Open questions

- **Fork: a `ref`-liveness check inside `audit.py`, or a declared schema module with a
  pre-commit gate** (the `check_provider_registry.py` shape). The first is cheaper; the second
  catches field-shape drift the first cannot see.
- Should `ref` become two fields — `ruling:` (why benign) and `row:` (who owns the cleanup)?
  That would make both lifetimes explicit instead of overloading one key.
- Does P-2 bind the disposition register at all, or only ratified intakes? It is being cited
  here by analogy, and the analogy has not been ruled.

## Status

READY — filed by the integrator at the 2026-08-24 batch close. Fork named, no row banked.
