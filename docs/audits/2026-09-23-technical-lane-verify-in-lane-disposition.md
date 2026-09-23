# Disposition ledger — lane-verify-in-lane's own two artifacts

**Date:** 2026-09-23
**Lane:** `lane-verify-in-lane` · **Branch:** `worktree-lane-verify-in-lane`

`funnel_coverage` requires every `docs/audits/*.md` artifact to carry exactly one disposition
(ACTIONED / FILED / REJECTED / SUPERSEDED, or PENDING with a question) recorded in a ledger table
elsewhere in the corpus (`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`, the ruling
that mechanism enforces). This lane's two artifacts are FILED under the row that owns them —
recorded here rather than by editing either committed artifact in place (both are already landed,
and `CLAUDE.md` §5 rule 3 holds audits immutable) or by editing the shared
`ecosystem/disposition-register.yaml` register (outside this lane's file ownership, `Files you own`
per `LANE-W4B-4-verify-in-lane.md`). This record is itself a `docs/audits/*.md` artifact and
dispositions itself, self-referentially, the same way
`docs/audits/2026-09-23-technical-lane-handback-organ-disposition.md`'s last row does.

## Disposition ledger

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-22-technical-lane-verify-in-lane-merge-queue-measurement.md | FILED | `[#960]` -- this lane's own row, open, cites this record in its `refs` clause |
| 2026-09-23-codex-lane-verify-in-lane-960-terra.md | FILED | `[#960]` -- this lane's own row, open, cites this record in its `refs` clause |
| 2026-09-23-technical-lane-verify-in-lane-disposition.md | FILED | `[#960]` -- this record itself; self-referential per the precedent above |
