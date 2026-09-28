# ADR-NNN (Proposed): a synthetic decision, for the /decide gate's own tests

- **Status:** Proposed

## Decision

Do the thing.

## Quality attributes

- **Quality attribute(s):** Testability (primary), Modifiability.
- **Scenario (six parts):**
  - *Source:* a lane's diff.
  - *Stimulus:* introduces a regression.
  - *Environment:* CI, both OSes.
  - *Artifact:* the integration sha.
  - *Response:* the regression is refused.
  - *Response measure:* 100% of seeded regressions caught.
- **Decision evidence:** the matrix and the evaluator responses above.

## Flip-condition

Reverse this decision if the measured cost doubles.

## Alternatives considered

A1 (today), A2 (withdrawn).
