<!-- scope: meta -->

# Child-repo relocation PROPOSAL (ADR-64 Q3-A) — no moves

> **Proposal only. Nothing was moved or edited in any other repo (ADR-41).** Branch
> `docs/backlog-migration-adr64-2026-06-01`, Step 7. Implements the *triage* half of ADR-64
> Decision 3; the *moves* are execution in the target repos (separate sessions). These items
> currently live in `BACKLOG.md` `## Coordination` → "Pending relocation," each with a
> `repo:`/`Relocate:` field and the id assigned in Step 6.

## Triage rule applied

- **Relocate** — the item's primary *work executes in a child repo*. It moves to that repo's own `BACKLOG.md`; the pointer then leaves `.dev-knowledge`.
- **Keep as Coordination pointer** — genuine cross-repo *governance/coordination* whose authority sits in `.dev-knowledge` (disseminator/auditor function). Stays here as a pointer, never a duplicated task. (ids 45 Phase-2 rollout, 46 scrum-master rollout, 47 undiscovered-repos — kept; not in this proposal.)

## Relocation mechanics (proposed; pins ADR-64 §"Open implementation questions" #1)

1. **Move, don't copy.** A child-repo session adds the item to `<repo>/BACKLOG.md` (with its own local id); a follow-on `.dev-knowledge` session then removes the pointer here. The two commits reference each other by message (`relocated from .dev-knowledge backlog id N` / `closes coordination id N`).
2. **Split-brain avoidance.** While in flight, the item is in exactly one *active* place at a time — it leaves `.dev-knowledge` only once it lands in the child repo. No simultaneous dual-ownership.
3. **Backlink.** The child entry's `Added:` cites the originating `.dev-knowledge` context (audit/ADR) so provenance survives the move.
4. **What stays.** If, on inspection, an item turns out to carry a genuine `.dev-knowledge` governance obligation (not just execution), keep a one-line Coordination *pointer* here and move only the execution part.

## Proposal table

| id | Item | Target repo | Verdict |
|---|---|---|---|
| 48 | Apply tier-deprecation | corp-monorepo | relocate |
| 49 | Apply tier-deprecation | ai-council | relocate |
| 50 | Execute ai-council universalization plan | ai-council | relocate (subsumes 49/57 scope) |
| 51 | Handoff folder-format adoption | corp-monorepo | relocate (after A4 legacy-format decision) |
| 52 | P1-2 path-traversal branch unmerged | corp-monorepo | relocate (operator merges branch → main) |
| 53 | Root hygiene application | corp-monorepo | relocate |
| 54 | Root hygiene application | ai-council | relocate |
| 55 | README disposition decision | corp-monorepo | relocate (decision in-repo; ai-council already DELETE) |
| 56 | Hyphen migration + ADR-38 (subitems 1,3) | corp-monorepo | relocate |
| 57 | Hyphen migration + ADR-38 | ai-council | relocate (largely subsumed by 50) |
| 58 | Prevent auto-debate of stray Council files | ai-council | relocate |
| 59 | ADR-59 visual-pattern retrofits (4×) | each child repo | relocate per-repo (corp-monorepo blocked on its ruff-strictness decision) |
| 60 | dev-tooling install + run.py → scripts/ | corp-sca-time-automation | relocate |
| 61 | LESSONS scope-tag backfill | ai-council | relocate |
| 62 | UPPERCASE TYPE legacy-archive rename | corp-monorepo, corp-sca | relocate (opportunistic) |
| 63 | docs/HANDOFF.md flat-file deprecation | corp-monorepo, ai-council | relocate (tied to 51) |
| 64 | Per-repo deeper cleanup (post-retrofit) | each child repo | relocate per-repo |
| 65 | Cross-repo low-severity cleanups (child subset) | corp-monorepo, corp-ops, corp-sca, ai-council | relocate / split per owner |

**18 items proposed for relocation.** Multi-target items (59, 62, 63, 64, 65) split into per-repo entries when they land. As these execute, `## Coordination` drains from 21 → ~3 (the kept governance pointers 45-47), bringing it under the ≤10 target.

## Constraints honored

- **No file in any other repo was read, edited, or moved** (ADR-41).
- Nothing removed from `.dev-knowledge` `BACKLOG.md` in this step — the pointers stay until their target-repo sessions execute the move.
- The triage verdicts are a recommendation for the operator; per-item re-triage at move-time is expected (mechanics rule #4).
