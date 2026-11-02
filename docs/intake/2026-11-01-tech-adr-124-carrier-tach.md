---
intake-id: 120
status: SEED
origin: "ADR-124 carrier rows owed through intake (R96 Carriage; GO-E3.1 id grant, to-cc/GO-E3.1.md: ADR-124's carrier rows go through intake and hold no reservation), filed by lane e31-decide, 2026-11-01"
consumed-by:
---

# SEED -- ADR-124 carrier: import boundaries are a tach contract

## Problem / motivation

ADR-124 D1 names tach 0.35.1 with a `tach.toml` seeded by `tach sync` from the current import graph and tags equal to the ADR-28 layers. No `tach.toml` exists in this tree. Layer boundaries (ADR-28) are stated in prose and checked by no tool. The carrier row is owed through intake (R96 Carriage; `scripts/decision_coverage.py:325`).

## Scenarios (+1 view)

- As the operator I read ADR-124 and expect the tool it names to be the thing that refuses the violation, not a sentence in the ADR.
- As a lane I add code that breaks the rule and the check refuses it before the commit or in CI, naming the rule.

## Functional requirements

- **Must:** D1 (tach as the import-boundary tool), D2 step 2 (one tool per lane, with a counter through `telemetry_emit.py wrap` and an expiry; 0 catches in its window removes it) and D4 (a ratchet).
- **Should:** every adoption lands through its own lane with a counter and an expiry (ADR-124 D2).
- **Could:** the configuration travels to consumers through the shared block (ADR-124 D3).

## Acceptance criteria (ex-ante)

a `tach.toml` exists, seeded from today's graph, tagged with the ADR-28 layers; a boundary violation is refused; the tool enters the commit stage only with its counter and expiry.

## Non-goals

No conversion pass over existing code (ADR-124 D4, ADR-108 section B-4 stays prospective). No new tool beyond ADR-124 D1's table. This document records WHAT and WHY; the row that carries it is filed after ratification of the intake (ADR-98, ADR-111).

## Impact sketch (4+1 lite)

- **Logical:** one more declared check in an existing config file.
- **Process:** a check at commit or CI time with a counter and an expiry.
- **Development:** untouched beyond the config and the check.
- **Physical:** untouched.

## Open questions

Whether the hub (a governance repo with validators) has enough imports for tach to catch anything within its window; the counter answers it, the ADR already says 0 catches removes the tool.