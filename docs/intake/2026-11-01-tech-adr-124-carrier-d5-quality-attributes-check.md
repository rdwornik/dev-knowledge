---
intake-id: 122
status: SEED
origin: "ADR-124 carrier rows owed through intake (R96 Carriage; GO-E3.1 id grant, to-cc/GO-E3.1.md: ADR-124's carrier rows go through intake and hold no reservation), filed by lane e31-decide, 2026-11-01"
consumed-by:
---

# SEED -- ADR-124 carrier: the ADR Quality attributes section (D5) is checked on every landed ADR, not only on /decide drafts

## Problem / motivation

ADR-124 D5 makes `## Quality attributes` a REQUIRED section of every ADR, enforced like `## Flip-condition` (FAIL above a new grandfather mark, WARN at or below). Today the section is checked only for /decide drafts, by `scripts/decide_checks.py` (`check_adr_sections`); `scripts/validate_adr_status.py` `REQUIRED_SECTIONS` does not list it, so an ADR landed by hand carries no check. `scripts/decision_coverage.py:325` records this as the part of ADR-124 not built. The carrier row is owed through intake (R96 Carriage).

## Scenarios (+1 view)

- As the operator I read ADR-124 and expect the tool it names to be the thing that refuses the violation, not a sentence in the ADR.
- As a lane I add code that breaks the rule and the check refuses it before the commit or in CI, naming the rule.

## Functional requirements

- **Must:** D5 (Quality attributes: Quality attribute(s), six-part Scenario with a Response measure, Decision evidence; grandfather mark = ADR-126).
- **Should:** every adoption lands through its own lane with a counter and an expiry (ADR-124 D2).
- **Could:** the configuration travels to consumers through the shared block (ADR-124 D3).

## Acceptance criteria (ex-ante)

`validate_adr_status.py` fails an ADR numbered above the grandfather mark that lacks the section or any of its parts, and warns at or below; the same parts that `decide_checks.py` checks are the ones checked; ADR-134..137 and ADR-133 are read as instances.

## Non-goals

No conversion pass over existing code (ADR-124 D4, ADR-108 section B-4 stays prospective). No new tool beyond ADR-124 D1's table. This document records WHAT and WHY; the row that carries it is filed after ratification of the intake (ADR-98, ADR-111).

## Impact sketch (4+1 lite)

- **Logical:** one more declared check in an existing config file.
- **Process:** a check at commit or CI time with a counter and an expiry.
- **Development:** untouched beyond the config and the check.
- **Physical:** untouched.

## Open questions

Whether ADR-133 and ADR-134..137, landed 2026-11-01 above the mark, all pass today (decide_checks reads ADR-134..137 as 0 defects). Whether the part check is shared with decide_checks rather than copied.