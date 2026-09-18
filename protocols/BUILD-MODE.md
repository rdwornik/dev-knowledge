# BUILD MODE — the contributor's rulebook

> **Declared** 2026-09-18 by the architect seat (`2026-09-17-dev-knowledge-architect`), started on
> the operator's word. **Expiry: 2026-11-18.** **Counter:** the five weekly ratchet numbers in
> `protocols/BUILD-LIST.md`. **Owner:** Rob (scope freeze) · architect seat (design).
>
> A second, smaller rulebook with a written exit condition and an expiry — not a bypass of the
> process. The work queue, its decisions and the weekly numbers live in `protocols/BUILD-LIST.md`.

## Rules

1. ONE flat build list, one file in the repo. No ids, no ADRs, no intakes. Done / not done.
2. Git discipline UNCHANGED: branch per unit, commit-and-STOP, integrator merges, tests paired
   against baseline.
3. Handback UNCHANGED: the ten fields to the transport at close.
4. Evidence UNCHANGED: every claim carries the command that produced it; WITNESSED / RELAY /
   UNSOURCED.
5. ONE writer on the primary checkout.
6. Decisions are ONE LINE in the build list, dated. No decision files.
7. NO new mechanism without a counter and an expiry — BUILD MODE itself included.
8. Refusals ONLY at git boundaries (pre-commit, pre-push, CI). Inside the agent loop, nothing but
   path protection. A PreToolUse hook hung a session for twelve hours; a pre-commit hook cannot.
9. Model stated explicitly per session. Opus for the architect seat only.
10. The exit condition is written on day one and BUILD MODE ends automatically when it is met.

## Exit condition — all five measured

- the distiller produces a contract from (kind, subject) with ZERO lines written by the browser;
- the inflow brake is armed and carries a counter;
- merge of a green lane is a MECHANISM, not a decision;
- the handback contract lives in the lane template;
- ONE real item from a consumer repo has gone through the loop end to end.

## Expiry

**2026-11-18.** If BUILD MODE has not exited by then it is reviewed, not silently extended.

## The ratchet on BUILD MODE itself

Five numbers measured weekly by the organs B2 wires — mechanism count, documentation bytes, organ
count, uncalled-organ count, open-row count. If ANY rises week over week, BUILD MODE FAILED THAT
WEEK and the next batch is deletion only. Without this, BUILD MODE becomes the thirty-fifth
mechanism, exactly like every bypass before it.

Week zero, and the command behind each number, is recorded in `protocols/BUILD-LIST.md`.

## The build list — row shape

One row per subject, these fields and no others:
`subject` · `prior-art` · `delta` · `removes` · `size` · `done`

- **`prior-art`** — what already exists for this purpose, where, in what form (code / prose /
  configuration / disabled). EMPTY IS ONLY VALID WITH EVIDENCE that the inventory found nothing.
- **`delta`** — exactly one verb from the CLOSED list:
  ARM (switch on what exists) · WIRE (connect what exists to a caller) ·
  REWRITE (prose -> mechanism, same purpose) · MOVE (relocate, same content) ·
  DELETE (remove, with proof of zero inbound edges) · BUILD (genuinely new).
  BUILD IS THE EXCEPTION AND REQUIRES `prior-art` TO PROVE ABSENCE. A lane that picks BUILD without
  that proof is REFUSED AT INTEGRATION.
- **`removes`** — what disappears when this lands. A REBUILD THAT REMOVES NOTHING IS SUSPECT BY
  DEFINITION.

## Batch gates

- B1 -> B2: the build list exists with `prior-art`, `delta` and `removes` filled for every row, and
  week zero's five numbers are recorded.
- B2 -> B3: net growth in mechanisms and documentation bytes is NEGATIVE against week zero.
- B3 -> B4: every REWRITE row has a non-empty `removes`.
- B4 -> exit: the five exit conditions, measured.

Net growth is checked AT INTEGRATION, at the git boundary — never inside the agent loop.

## Scope freeze

Anything new goes to the END of the build list and waits for the exit.
