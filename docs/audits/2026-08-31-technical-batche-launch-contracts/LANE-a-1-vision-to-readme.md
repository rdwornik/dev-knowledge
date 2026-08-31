# LANE batch-e-a-1-vision-to-readme — retire VISION.md behind the recreated root README.md, fleet-wide, and package the migration as a deploy carrier. Executes [#614]'s frozen arc.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local` — an on-machine committing lane in its own worktree.

```
Dispatch-Lane lane-a-1-vision-to-readme LANE-a-1-vision-to-readme.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED — `RemoteExitCode=1`, the container's agent returning
*"Not logged in · Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so §1(C)'s named fallback applies to every committing lane in this batch.

## Worktree pairing

slug `lane-a-1-vision-to-readme` -> branch `worktree-lane-a-1-vision-to-readme` -> contract `LANE-a-1-vision-to-readme.md`

## Write-scope (frozen)

- `README.md`
- `VISION.md`
- `scripts/canonical_docs.py`
- `deploy/manifest-v1.4.0.yaml`
- `ecosystem/parity-surfaces.yaml`
- `tests/test_canonical_docs.py`

**`CLAUDE.md` IS DELIBERATELY ABSENT FROM THIS SCOPE — architect ruling CUT-3(b).** The
VISION-line removals at `CLAUDE.md` `:39` (critical paths) and `:68` (living docs) are
**DC-23's** last act, conditioned on this lane being merged. Do not touch `CLAUDE.md` here even
though the VISION retirement is what motivates those two edits: the disjointness is what lets
DC-1 and DC-23 run without a merge conflict, and predicate 6 of the `[#591]` validator now
REFUSES a batch whose declared scopes intersect. Adding `CLAUDE.md` back would RED the freeze.

## Done-contract (immutable)

1. **`README.md` is the MUST front door and `VISION.md` is retired** in the canonical-docs
   registry. ADR-114 already ruled `README.md` a sanctioned Tier-1 file; this executes it.
2. **Every gate-coupled consumer re-pointed** — at minimum the P1a boot probe,
   `scripts/canonical_docs.py`, the hermeticity validators and the ADR-38 baseline check.
   Enumerate them by resolving each locator, never from memory.
3. **`VISION.md` archived BYTE-IDENTICALLY.** Not rewritten, not summarised, not deleted.
4. **The migration is packaged as a deploy carrier**, so the fleet receives it as an organ
   rather than as four hand-edits.
5. **Parity stays GREEN at every step.** No ADR-104 member is left declaring a retired MUST.
6. **The P1a probe runs against the new README BEFORE merge**, and its result is in the packet.

**Deployment order is RULED (CUT-1): `hub -> monorepo -> ai-council -> win-tooling`.** This is the
MIGRATION order. win-tooling being last does NOT roll back its status as the first instantiated
consumer — the floor stays. Do not re-litigate; do not reorder.

## Decision budget

**V-2 — escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported. A refuted premise PAUSEs with the fact (Q10).

## Steps

1. Resolve every consumer locator before editing it (`/preflight`). An unopened locator is a
   claim, not evidence.
2. Amend the registry; re-point consumers; archive VISION byte-identically.
3. Package the deploy carrier.
4. Run the P1a probe against the new README. Run the TARGETED tests for this diff.
5. Commit and STOP.

## What NOT to do

- No merges, no pushes to `main` — commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (P-1), no index regeneration (Q1), no row births.
- **No `CLAUDE.md` edit.** See the write-scope note.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
