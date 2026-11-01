---
intake-id: 121
status: SEED
origin: "ADR-124 carrier rows owed through intake (R96 Carriage; GO-E3.1 id grant, to-cc/GO-E3.1.md: ADR-124's carrier rows go through intake and hold no reservation), filed by lane e31-decide, 2026-11-01"
consumed-by:
---

# SEED -- ADR-124 carrier: static types are checked in CI by the pyright pin already in the repo

## Problem / motivation

ADR-124 D1 adopts pyright in CI at `typeCheckingMode = "standard"` reusing the 1.1.410 pin already in `package.json` (ADR-89): one pin, not two. `package.json` carries the pin for the reverse-dependency oracle only and `pyproject.toml` has no `[tool.pyright]` block, so no CI step type-checks anything. The carrier row is owed through intake (R96 Carriage; `scripts/decision_coverage.py:325`).

## Scenarios (+1 view)

- As the operator I read ADR-124 and expect the tool it names to be the thing that refuses the violation, not a sentence in the ADR.
- As a lane I add code that breaks the rule and the check refuses it before the commit or in CI, naming the rule.

## Functional requirements

- **Must:** D1 (pyright in CI, one pin), D2 step 3 (counter and expiry), D4 (a ratchet over the counted baseline).
- **Should:** every adoption lands through its own lane with a counter and an expiry (ADR-124 D2).
- **Could:** the configuration travels to consumers through the shared block (ADR-124 D3).

## Acceptance criteria (ex-ante)

`[tool.pyright] typeCheckingMode = "standard"` is configured; a CI job runs the pinned pyright; the error count is recorded and may only fall; no second pin appears.

## Non-goals

No conversion pass over existing code (ADR-124 D4, ADR-108 section B-4 stays prospective). No new tool beyond ADR-124 D1's table. This document records WHAT and WHY; the row that carries it is filed after ratification of the intake (ADR-98, ADR-111).

## Impact sketch (4+1 lite)

- **Logical:** one more declared check in an existing config file.
- **Process:** a check at commit or CI time with a counter and an expiry.
- **Development:** untouched beyond the config and the check.
- **Physical:** untouched.

## Open questions

Whether the check runs in the conductor.yml push run or the nightly (the day/night split of R119 is the operator's). How the node dependency of the pin is satisfied in CI.