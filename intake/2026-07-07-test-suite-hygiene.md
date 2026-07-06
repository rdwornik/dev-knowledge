---
intake-id: 3
status: SEED
origin: operator concern, captured 2026-07-07 (Arc-2 epic prompt)
consumed-by:
---

# Test-suite hygiene — theatricality review + impacted-test selection

## Problem / motivation

The test suite / ship-gate runs long, and the collected-test count keeps growing.
Neither growth axis has been examined for whether it's earning its keep: some
fraction of the corpus may be padding the collected count without asserting anything
real, and `/ship` runs the whole corpus regardless of how small the change is. A
complicating wrinkle: the suite recently got **faster** for reasons nobody has
verified — before touching anything, that has to be understood, or any before/after
cleanup number is meaningless.

## Scenarios (+1 view)

- As the operator, I run `/ship` on a one-doc change and wait only for the tests that
  could plausibly break as a result — not the entire corpus.
- As the operator, I read a theatricality report that names specific padded tests,
  each with the evidence that it asserts nothing real (not a vibe-based flag).

## Functional requirements

- **Must:** a theatricality review of the pytest corpus — find tests that assert
  nothing real and exist only to pad the collected count.
- **Must:** impacted-test selection, so `/ship` runs the tests affected by the
  change rather than the full corpus every time.
- **Must (precondition — do this first):** the suite got faster recently for an
  unknown reason. Verify *why* before assuming anything about the current baseline —
  any theatricality or selection work built on an unexplained baseline is built on
  sand.

## Acceptance criteria (ex-ante)

- Ship-gate wall-time delta and collected-count delta after cleanup are both
  measured against a **recorded baseline** (recorded before cleanup starts, not
  reconstructed after).
- The "why did it get faster" question is answered with evidence — not a guess —
  before any cleanup work lands.

## Non-goals

- Not built in Arc 2 / #268 — this is a SEED for the technical architect's triage,
  not a request to build now.
- No test deletion without operator review (core invariant — "never delete code or
  files without asking" applies to tests same as anything else).
- No coverage reduction disguised as cleanup — a theatricality finding must show the
  test asserts nothing real, not merely that it's slow or old.

## Impact sketch (4+1 lite)

- **Logical:** none.
- **Process:** ship cadence — how long an operator waits per `/ship` invocation.
- **Development:** the test corpus itself + the ship-gate that runs it.
- **Physical:** none.

## Open questions

- What made the suite faster recently? Verify before assuming anything about the
  baseline (the Must-precondition above).
- What selection mechanism fits — pytest markers, path-mapping, or a git-diff-based
  approach? Left to the technical architect's call.

## Status

SEED — dropped by the operator during the Arc-2 epic prompt; not yet picked up by a
functional-architect conversation. See `intake/README.md` §5 for the full lifecycle.
