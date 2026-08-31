# LANE batch-e-k-11-derived-doc-freshness (HY-1) - doc freshness DERIVED from git for every living doc, and gated. Extends the P5 pattern fleet-wide.

| Model | Mode | Effort |
|---|---|---|
| opus | execute | high |

## Dispatch

**Shape:** `local`

```
Dispatch-Lane lane-k-11-derived-doc-freshness LANE-k-11-derived-doc-freshness.md -Effort high
```

**SUBSTRATE IS `local` BY MEASUREMENT, NOT PREFERENCE.** Batch E's codespace admission probe ran
2026-08-31 and came back RED - `RemoteExitCode=1`, the container's agent returning *"Not logged
in - Please run /login"* in 47 ms
(`docs/audits/2026-08-31-verification-codespace-admission-probe.md`). Z-G3's entry condition is
NOT met, so section 1(C)'s named fallback binds every committing lane in this batch.

## Worktree pairing

slug `lane-k-11-derived-doc-freshness` -> branch `worktree-lane-k-11-derived-doc-freshness` -> contract `LANE-k-11-derived-doc-freshness.md`

## Write-scope (frozen)

- `scripts/canonical_docs.py`
- `scripts/audit.py`
- `tests/test_canonical_docs.py`

**Substrate deviation:** `substrate-lane-write-scope-disjoint` - this lane and DC-1 (`lane-a-1`)
both write `scripts/canonical_docs.py`, and that is DELIBERATE and SEQUENCED rather than
accidental: HY-1 derives the freshness stamp the registry DC-1 is amending will carry. The
merge order is frozen `DC-1 -> HY-1`, DC-1 must be MERGED before this lane starts, and the
integrator verifies that before dispatching it.

## Blocked by

**Tier (A)'s A4 harvest** (`batch-e-a4-doc-freshness-derivation-audit`), which carries the
derivation design and the measured table. **And DC-1 must be MERGED** - both lanes write
`scripts/canonical_docs.py`, and predicate 6 of the `[#591]` validator refuses intersecting
scopes inside one batch. This lane runs AFTER DC-1 lands.

## Done-contract (immutable)

1. **`last_reviewed` is DERIVED from git rather than hand-maintained**, for every living doc,
   and the derivation is GATED. A hand-maintained date lies by construction; that is the whole
   finding A4 exists to measure.
2. **A CONTENT commit is distinguished from a TOUCH.** A whitespace, regeneration or
   index-refresh commit does not invalidate a review. State the rule and apply it consistently -
   a delta computed off `git log -1` alone over-reports and is not the deliverable.
3. **The three classes A4 separates are preserved:** gated-and-stale, gated-and-fresh, and
   **ungated-and-stale**. The third is what funds this lane - it is the part no gate watches.
4. **PLAYBOOK's doctrine table shows the live version and date.**
5. **Docs carrying NO stamp are listed, not skipped.** An absent stamp is not a fresh one.

## Steps

1. Harvest and read A4 first. Do not re-derive what it measured.
2. Implement the derivation RED-first (ADR-108 section B): failing tests before build code.
3. Run the TARGETED tests for this diff. Commit and STOP.

## Decision budget

**V-2 - escalate on three classes only:** (a) curated-baseline touches, (b) genuine
rule-vs-ruling conflicts, (c) fork classes with no standing ruling. Everything else is decided
per contract defaults and reported in the end packet. A refuted premise PAUSEs with the fact
(Q10) - deviation-with-disclosure discharges the reporting duty, it does not authorise the
deviation.

## What NOT to do

- No merges, no pushes to `main` - commit-and-STOP; integration is the integrator's act.
- No JOURNAL entry (`protocols/STANDING_RULINGS.md` P-1), no index regeneration (Q1).
- No row births beyond what the done-contract names - reconcile-before-birth binds this batch.
- No edits outside the declared footprint. Prose in English; hyphen-only names.
