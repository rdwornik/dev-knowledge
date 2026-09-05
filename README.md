---
version: 1.0
owner: rob
last_reviewed: 2026-09-01
status: active
---

# .dev-knowledge
<!-- scope: meta -->

## Vision

`.dev-knowledge` is a universal LLM-driven development guide and
methodology framework. Full statement — doctrine vs. artifact host-binding,
the continuous-improvement principle, strategic emphasis, scope, values,
relationships and lifecycle: `docs/archive/governance.md`.

## References

- `CLAUDE.md` — the session contract for Claude Code in this repo
- `AGENTS.md` — the portable instruction layer every provider reads (ADR-115)
- `ARCHITECTURE.md` — the structural map; read before structural changes
- `docs/archive/VISION.md` — superseded by this file (ADR-114); relocated here at the hub ([#614] lane-e-5, 2026-09-01), retained and still tracked
- `docs/archive/governance.md` — full Vision, Strategic emphasis, Scope, Values, Relationships and Lifecycle; relocated from this file by lane `lane-h0-readme` ([#634], 2026-09-05)
- `protocols/ESSENTIALS.md` — operating values, daily cheat sheet
- `protocols/PLAYBOOK.md` — full process reference
- `JOURNAL.md` — session-by-session activity history (and notable-change record; replaces the retired CHANGELOG.md per ADR-49)
- `BACKLOG.md` — cross-session pending items (per ADR-41)
- `ecosystem/north-star.md` — **the arc set in dependency order: what this repo is working towards and what blocks what.** GENERATED from `tasks/` (`scripts/gen_north_star.py --write`); the arc names and their order are declared, every count and member row is derived, so it cannot drift from the backlog the way a hand-written roadmap does
- `CONTRIBUTING.md` — branch/commit/validator conventions
- `docs/decisions/` — architectural decisions (ADRs only; the `transcripts/` landing zone was deleted 2026-07-22)
- ADR-88 — File-oriented dependency management (markdown as a design pattern): repo files are the dependency unit; coherence across the declared edge-graph is held by mechanism — a conformance harness — not by memory.
