# 05 · Now

<!-- scope: meta -->

> What to do next. The live edge of the work.

## Immediate state

**Clean, nothing half-done.** v4 HANDOFF_PROCESS is stable; ADR-62 + ADR-63 ratify it and the scrum-master review pattern, merged to `main` (`a637f5f`). Working tree clean, baseline green (103 / 9/9 / ruff). Wait for Rob to pick the next item.

## Next candidates (operator picks — nothing is in-flight)

The open queue, by priority (full detail in `BACKLOG.md`):

- **P1** — Adversarial fresh-eyes pass in routine handoff generation (Council scope; pairs with `protocols/AGENT_FRAMEWORK.md` stub). The direct extension of the v4 curse-of-knowledge result.
- **P1** — Sacred-files maintenance enforcement (mechanism design — staleness check / session-end hook).
- **P1** — Council decisions management consolidation (contradiction detection + decision-evolution ownership model).
- **P2** — Extend audit-check enforcement to other governance artifacts (transcripts, ADRs).
- **P2** — Hooks audit *implementation* (the audit is done; the hook additions/consolidation remain).
- **P3** — Relax-vs-gate principle for drifted guards (paired-ADR tension from the ADR-62/63 review). LESSONS or small ADR.
- **P3** — Process refinements deferred from v4.3.1 (7 items batched; mostly Sonnet/medium doc edits).
- **P3** — CLAUDE.md §4 cites a stale known-failing test (one-line fix — that test now passes).

## Watch out for

- **Don't edit ADRs in place** — 62/63 are immutable now (supersede instead).
- **Append-only files** — JOURNAL/LESSONS prepend newest-first.
- **Layer-2 never executes** — validators only.
- **Next quarterly BACKLOG grooming:** 2026-07-01.

---

**Source:** synthesized from `BACKLOG.md` + `JOURNAL.md` at generation (no live interview).
