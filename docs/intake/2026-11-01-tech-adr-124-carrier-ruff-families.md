---
intake-id: 119
status: SEED
origin: "ADR-124 carrier rows owed through intake (R96 Carriage; GO-E3.1 id grant, to-cc/GO-E3.1.md: ADR-124's carrier rows go through intake and hold no reservation), filed by lane e31-decide, 2026-11-01"
consumed-by:
---

# SEED -- ADR-124 carrier: the ruff rule families and the complexity bound are enforced, not just declared

## Problem / motivation

ADR-124 D1-D4 (Accepted 2026-10-11, R96) name 15 ruff rule families (B, SIM, C90, PL, RET, PERF, FURB, PTH, N, UP, ARG, ERA, TRY, FBT, RUF) and `max-complexity = 10`. `pyproject.toml` `[tool.ruff.lint] extend-select` carries 7 single rules of three of those families and no `[tool.ruff.lint.mccabe]` block, so the decision is visible in the ADR and absent from the toolchain. The carrier row is owed through intake (R96 Carriage; `scripts/decision_coverage.py:325`) and has not been filed.

## Scenarios (+1 view)

- As the operator I read ADR-124 and expect the tool it names to be the thing that refuses the violation, not a sentence in the ADR.
- As a lane I add code that breaks the rule and the check refuses it before the commit or in CI, naming the rule.

## Functional requirements

- **Must:** D2 step 1 (ruff `extend-select` + C90, no new dependency, violations counted before and after), D3 (one shared configuration in `templates/ruff-config-block.toml`, gated by `fleet_parity`) and D4 (a ratchet: a new violation is refused, the counted baseline only shrinks).
- **Should:** every adoption lands through its own lane with a counter and an expiry (ADR-124 D2).
- **Could:** the configuration travels to consumers through the shared block (ADR-124 D3).

## Acceptance criteria (ex-ante)

the families of D1 are selected in `pyproject.toml`; the count of violations is recorded before and after; a new violation fails the check while the baseline may only fall; the shared config block carries the same set and `fleet_parity` is green.

## Non-goals

No conversion pass over existing code (ADR-124 D4, ADR-108 section B-4 stays prospective). No new tool beyond ADR-124 D1's table. This document records WHAT and WHY; the row that carries it is filed after ratification of the intake (ADR-98, ADR-111).

## Impact sketch (4+1 lite)

- **Logical:** one more declared check in an existing config file.
- **Process:** a check at commit or CI time with a counter and an expiry.
- **Development:** untouched beyond the config and the check.
- **Physical:** untouched.

## Open questions

Which of the 15 families enter first (the order inside D2 step 1 is not fixed by the ADR). Whether `lane-python-standard-1`/`-2` audits already hold the hub baseline (docs/audits/2026-09-25-codex-lane-python-standard-1.md, 2026-09-29-codex-codex-lane-python-standard-2.md) so the count is read, not re-measured.