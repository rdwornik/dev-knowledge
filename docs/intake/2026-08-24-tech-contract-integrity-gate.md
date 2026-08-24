---
intake-id: 46
status: READY
origin: integrator, 2026-08-24 batch close; twelve contract errors observed in one window, all one class
---

# A contract states facts it has not verified — and twelve of them were wrong in one window

## Problem / motivation

A lane or integrator contract is a hand-written artifact that states facts about the repo, and
those facts are **not checked against the repo before anyone acts on them**. In this single
batch window, the integrator contract's stated premises were wrong at least twelve times. A
representative sample, each measured rather than argued:

- *"`JOURNAL.md` — six branches touch it, and two collide."* **Eight** branches touch it, and the
  real collision was **six branches all claiming `2026-08-23 (k)`** plus a second C2 entry —
  four times the predicted surface.
- *"L5's mood rewording moves it down by 5."* **Measured net ZERO.** L5's seven `protocols/`
  files contribute no token change at all; the entire +4 was L7's.
- *"`ALL_CHECKS` goes 43 → 44"* — correct — but the pin roster shipped by the lane that owned
  the change **omitted a fifth live pin** (`tests/test_doc_code_edge.py:713`). The contract
  caught that one; nothing structural did.
- *"`[#532]/A9` is closed while 20 WARNs cite it."* **Six** entries cite it; **18** cite the open
  `#241`.

Every one of these is the same defect: **the contract asserted a measured value instead of
naming the command that measures it.** Where the contract instead said *"measure it, set it, and
show your arithmetic"* — as it did for the silent-rule count — the executor got it right,
because there was nothing to inherit.

The corrective already exists as doctrine and is not enforced: `CLAUDE.md` §4 **M2** — *"Never
restate a count or roster in prose — cite the surface that computes it"* — and **M1** — *"Resolve
a locator before you act on it."* M1 records that this is *"the most-recorded executor failure in
the 2026-08-21 governance-drift audit"*, and that the audit's own replacement locator was itself
off by one. The rules are right; nothing applies them to contracts.

## Scenarios (+1 view)

- An integrator reads "two collide", plans two re-letters, and meets eight. Recoverable here
  only because the collisions FAIL a gate; a non-gated wrong premise would have shipped.
- A lane's own registration roster omits a pin. The lane is not lying — it enumerated what it
  found — but the executor who trusts the roster REDs the suite.
- A contract cites `file.md:123`. Three merges later that line is something else, and the
  executor edits the wrong thing having "followed the contract".

## Functional requirements

- **Must:** a contract names the **command that establishes a fact**, never the fact — for every
  count, roster, and collision claim.
- **Must:** a `file:line` / SHA / `[#id]` locator in a contract is resolvable at the moment it is
  acted on, or the executor is told to resolve it first.
- **Should:** contract generation validates emitted paths exist.
- **Could:** a delivery gate — a contract cannot be handed to a seat until its locators resolve.

## Acceptance criteria (ex-ante)

1. A contract containing a bare measured count is refused, or the count is annotated with the
   command that produces it.
2. Every locator in a generated contract resolves at emit time; a test proves an unresolvable
   locator is refused.
3. `/preflight` (which exists, is read-only, and is **wired into no gate**) is either wired in
   or explicitly ruled advisory-forever with the reason recorded.

## Non-goals

- Preventing a contract from being *wrong about a judgement*. This is only about facts a command
  could have checked.
- Rewriting the contracts already executed. The eleven batch-1 contracts are grandfathered as
  records of what was actually dispatched.

## Impact sketch (4+1 lite)

- **Logical:** a contract becomes a set of instructions plus verifiable references, not a
  snapshot that rots between authoring and execution.
- **Process:** costs the author a command per claim; saves the executor a wrong action.
- **Development:** extends `gen_lane_contract` (which today checks SHAPE only, by its own
  admission) and/or wires `/preflight`.
- **Physical:** `scripts/gen_lane_contract.py`, `.claude/commands/preflight.md`.

## Open questions

- **Fork: a delivery gate (contract refused until locators resolve), emit-time path validation
  (generator refuses to write an unresolvable locator), or the doctrine rule alone (a contract
  names the command, never the fact).** They are complementary, not exclusive; the cheapest
  single act is the third, and it is the only one that also covers hand-written contracts —
  which is what every contract in this batch was.
- Can a gate distinguish a *measured* count from an incidental number in prose? If not, the rule
  may have to be a review discipline with a nudge rather than a block.
- Does this bind the architect's own contracts, which are authored outside the repo and arrive
  via `~/Downloads`? Every error above came from one of those.

## Status

READY — filed by the integrator at the 2026-08-24 batch close. Fork named, no row banked.
