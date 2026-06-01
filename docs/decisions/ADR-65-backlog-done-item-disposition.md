<!-- scope: meta -->

# ADR-65 — BACKLOG done-item disposition: git is the technical record, JOURNAL is the business record

**Status:** Accepted — 2026-06-01, **Path A** (direct ADR refining ADR-64; no Council convene — post-hoc record of an operator-confirmed refinement, not a new architecture choice).
**Refines:** ADR-64 (Decision 1 — done items leave the active file).
**Related:** ADR-47 (done items leave; git history is the record), ADR-49 (git history replaces CHANGELOG), ADR-39 (living-files), CLAUDE.md §5 (`BACKLOG_ARCHIVE.md` stays deleted). Diagnosis: `docs/audits/2026-05-31-backlog-architecture-diagnosis.md`; migration inventory: `docs/audits/2026-06-01-backlog-migration-inventory.md`.

## Context

ADR-64 Decision 1 settled that done items **leave** `BACKLOG.md` (no archive file, no collapsed stubs). Implementing it surfaced a practical question the operator resolved in self-review: **where does a done item's record live, and does "done items leave" impose a new per-item logging burden?** If every closure required a deliberate write somewhere, the convention would just relocate the ceremony ADR-47 tried to remove.

## Decision

1. **Technical record = git.** A done item's full text, history, and closure live in git — recoverable via the tagged removal commit (restores the entry verbatim) plus the closing commit(s) that did the work. **No archive file** (CLAUDE.md §5; ADR-47 "no ceremonial archive").

2. **Business record = the per-session JOURNAL narrative.** *What* was done and *why* already rides the existing per-session JOURNAL ritual (`Did / Result / Changes`). Closing a backlog item therefore adds **no new per-item write** — it is covered by the session entry that performed the work. JOURNAL is not a per-item close-log.

3. **Forward-only indexing.** Git history is immutable. The CONTRIBUTING commit-naming convention (entry-`id`/ADR references) indexes **future** commits so a closure is locatable by id. Past closures are covered by the SHAs already embedded in entries, preserved into this migration's one-time JOURNAL map. **No history is ever rewritten.**

4. **One-time migration bridge.** Because the 41 currently-done entries are being removed in bulk *outside* their original sessions, this migration writes **one** JOURNAL entry mapping each retired item → closing SHA → one-line summary. This is a one-time bridge for the bulk purge, **not** an ongoing discipline.

## Consequences

- The "does done-items-leave create a logging tax?" objection is resolved: **no per-item tax** — git + the existing JOURNAL ritual already carry the record.
- A removed item is recoverable two independent ways: `git revert` of the tagged removal commit (entry text), and its closing commit (the work).
- `BACKLOG_ARCHIVE.md` is not revived; CLAUDE.md §5 stands.
- Retrospective "what was done" = `git log` + JOURNAL. **Revisit signal** (per ADR-64): if `git log` retrospection of done items becomes frequent pain, add a *read-only generated* "recently done" view — never a managed archive file.

## Alternatives considered

- **One-line stubs in-file** (ADR-64 Option-1 disposition) — rejected by ADR-64 Q1-A; stubs still accrete and re-bloat.
- **Revive `BACKLOG_ARCHIVE.md`** (ADR-64 Option-3) — rejected; would amend CLAUDE.md §5 + ADR-47.
- **Per-item JOURNAL / close-log write** — rejected as a new per-event discipline (operator refinement: the record rides the existing per-session ritual, not a new per-item one).

## References

- `docs/decisions/ADR-64-backlog-architecture.md` (the decision this refines)
- `docs/decisions/ADR-47-cross-repo-backlog-organization.md`; `docs/decisions/ADR-49-consolidate-past-recording-files.md`
- `CLAUDE.md` §5 (deleted-files invariant)
- `docs/audits/2026-06-01-backlog-migration-inventory.md` (the verified done-set + SHA map basis)
