# Disposition ledger — lane-hooks-rearm's own two artifacts

**Date:** 2026-09-22
**Lane:** `lane-hooks-rearm` · **Branch:** `worktree-lane-hooks-rearm`

`funnel_coverage` requires every `docs/audits/*.md` artifact to carry exactly one disposition
(ACTIONED / FILED / REJECTED / SUPERSEDED, or PENDING with a question) recorded in a ledger table
elsewhere in the corpus (`docs/audits/2026-08-17-technical-audit-disposition-ledger.md`, the ruling
that mechanism enforces). This lane's two artifacts are FILED under the row that owns them —
recorded here rather than by editing either committed artifact in place (both are already landed,
and `CLAUDE.md` §5 rule 3 holds audits immutable) or by editing the shared
`ecosystem/disposition-register.yaml` register (outside this lane's file ownership, `Files you own`
per `LANE-W4B-0-hooks-rearm.md`). This record is itself a `docs/audits/*.md` artifact and
dispositions itself, self-referentially, the same way
`docs/audits/2026-09-05-technical-r5-funnel-disposition-ledger.md`'s last row does.

## Disposition ledger

| File | Disposition | Evidence locator |
|---|---|---|
| 2026-09-22-technical-lane-hooks-rearm-live-measurement.md | FILED | `[#956]` -- this lane's own row, open, cites this record in its `refs` clause |
| 2026-09-22-codex-lane-hooks-rearm.md | FILED | `[#956]` -- this lane's own row, open, cites this record in its `refs` clause |
| 2026-09-22-technical-lane-hooks-rearm-disposition.md | FILED | `[#956]` -- this record itself; self-referential per the precedent above |
