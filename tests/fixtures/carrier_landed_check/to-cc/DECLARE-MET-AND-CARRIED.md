carried-by: docs/decisions/ADR-900-fixture.md (merged via worktree-lane-fixture, confirmed 2026-09-26)
lands-via: docs/decisions/ADR-900-fixture.md, once the lane merges it

## Fixture

The negative control: the same landing home as `DECLARE-MET-BUT-OPEN.md`, but this file's
`carried-by:` has already been discharged. It carries no `OPEN` value at all, so
`gen_handoff.carriage_verdicts` reads it as `CARRIAGE_RESOLVES` -- out of this organ's
population -- and it must never appear in `carrier_landed_check`'s findings.
