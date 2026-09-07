---
intake-id: 78
status: DRAFT
origin: browser architect seat, deliberate read of the AJ catalogue, 2026-09-07 — `to-cc/DECLARE-F-2-2026-09-07.md` §B row C-A; catalogue rows A-08 / A-09 in `docs/audits/2026-09-06-technical-research-aj-thesis-catalogue-and-deployment-model.md:255-256`
consumed-by:
---

# A lane is sent to a blank page when mature siblings exist — name them in the contract

## Problem / motivation

The catalogue's A-08 states the greenfield inversion as a principle: an agent is *better* on a
mature codebase than on a blank page, so seed it deliberately with reference implementations.
A-09 records the same lesson operationally — run the agent from a directory that already holds
sibling implementations.

We already do this at one grain and not at the other. Between repos the inversion is a running
mechanism: `deploy/carrier_floor.py` plus the manifest carriers seed a child from the matured hub.
Between *lanes* it is absent. A frozen lane contract states a footprint, a done-contract and a
tier; it does not state *which existing file in this tree already solves the adjacent problem
well*. So a lane writing a new validator invents a shape, and the reviewer discovers at tally time
that a mature sibling three files away had already settled the same question.

Measured at filing time (2026-09-07): the token `reference-implementations:` appears nowhere in
`scripts/`, `templates/` or `.claude/`; `scripts/gen_lane_contract.py` exists and emits contracts
without such a field; `lane-contract-check` (`.pre-commit-config.yaml:282`) is a shape gate whose
own comment records its honest limit — *"it checks SHAPE, never whether the contract's footprint
claims are true"*.

Left unaddressed, every code lane re-pays the orientation cost the hub has already paid, and the
inversion stays a fleet-level mechanism that never reaches the grain where most work happens.

## Scenarios (+1 view)

- As the dispatcher, I emit a code lane's contract with `gen_lane_contract.py`. The generator
  refuses to finish until the contract names at least one reference implementation, so the
  question *"what does a good one of these already look like here?"* is answered before the lane
  boots rather than at review.
- As a lane, I open my frozen contract at step 0 and read the named siblings **before my first
  write**. My new hook module comes out shaped like the hooks already in the roster, and the
  reviewer's tally has nothing to say about shape.
- As the reviewer, I read a tally that says the lane diverged from its named reference. That is a
  finding with a citable baseline, not an aesthetic objection.
- As the operator, I look at a code lane whose contract carries an empty
  `reference-implementations:` field and see the commit **refused** at `lane-contract-check` —
  the same way a malformed dispatch line is refused today.
- As a docs-only lane, I carry no reference implementations and am not refused, because the
  requirement is scoped to code lanes.

## Functional requirements

- **Must:** the lane-contract template and `scripts/gen_lane_contract.py` gain a
  `reference-implementations:` field — a list of repo-relative paths, each an existing tracked
  file the lane should read before writing.
- **Must:** `lane-contract-check` refuses a **code** lane whose `reference-implementations:` field
  is missing or empty. Tier is already in the contract and already agreed against the routing row,
  so the code/docs discrimination reuses that value rather than inventing a second one.
- **Must:** each listed path is resolved — a reference that does not exist in the tree is a
  refusal, not a WARN. This is the repo's standing "resolve a locator before you act on it" rule
  applied to the contract that *issues* the locators.
- **Should:** the lane-boot step surfaces the named files as a read, so the contract's answer is
  consumed rather than merely present.
- **Could:** the generator proposes candidates from the footprint's directory (nearest siblings by
  path) for the author to accept or replace; proposal only, never auto-filled.

## Acceptance criteria (ex-ante)

- **AC-1:** `gen_lane_contract.py emit` for a code-tier lane with no reference implementations
  supplied exits non-zero with a message naming the missing field.
- **AC-2:** A committed code-lane contract carrying `reference-implementations:` with an empty
  value is REFUSED by `lane-contract-check` at pre-commit; the same file with one valid tracked
  path passes.
- **AC-3:** A code-lane contract naming a path that is not tracked in the tree is REFUSED, with
  the unresolved path quoted in the message.
- **AC-4:** A docs-only lane contract with no `reference-implementations:` field passes unchanged
  — proven by re-running the gate over an existing docs-lane contract already in
  `docs/audits/2026-09-06-technical-batch-u-launch-contracts/`.
- **AC-5:** The lane contracts already in the tree are not retroactively refused: the gate fires
  on contracts emitted after the change, and the migration posture for older ones is stated in the
  hook comment.

## Non-goals

- **Not** a judgment of whether the lane actually *followed* the reference. The gate checks that
  the question was answered, not that the answer was obeyed — the same honest limit
  `lane-contract-check` already records about footprint claims.
- **Not** a change to the carrier/floor seeding mechanism between repos; that half of the
  inversion already runs and is not in scope here.
- **Not** a new contract genre and not a new branch prefix.
- **Not** an automatic "best sibling" inference engine. Candidate proposal is a *Could*, and even
  then it never fills the field unattended.

## Impact sketch (4+1 lite)

- **Logical:** the lane contract gains one field; "a lane has a baseline it reads first" becomes a
  recorded property rather than tribal practice.
- **Process:** dispatch grows one authoring decision per code lane; lane boot grows one read.
- **Development:** `scripts/gen_lane_contract.py`, the contract template, and the
  `lane-contract-check` entry point in `.pre-commit-config.yaml`, with tests alongside the
  existing lane-contract shape tests.
- **Physical:** untouched — no new file class, no new directory, no runtime.

## Open questions

- Where does the code/docs tier value actually live in the emitted contract, and is it already
  parsed by `lane-contract-check`, or does the gate need to learn it? (Technical-architect
  question; not answered here.)
- Should a reference implementation be pinned to a SHA, or resolved at HEAD? A pin is honest about
  what the lane read; HEAD is cheaper and does not rot into a false claim.
- Does the same field belong on the handoff-bundle contract, or is the lane the only consumer?

## Status

DRAFT — filed 2026-09-07. The operator deferred ratification: DECLARE-F-2 §B files this row as
DRAFT, "ratified at the next sitting". No backlog row and no ADR are owed until then.
