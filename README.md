---
version: 1.1
owner: rob
last_reviewed: 2026-09-06
status: active
---

# .dev-knowledge
<!-- scope: meta -->

## Vision

`.dev-knowledge` is a universal LLM-driven development guide and
methodology framework. Full statement — doctrine vs. artifact host-binding,
the continuous-improvement principle, strategic emphasis, scope, values,
relationships and lifecycle: `docs/archive/governance.md`.

**What it is, concretely.** Markdown governance files plus hub-local validators, generators
and gates. It prescribes the conventions every `Dev/` child repo follows, and agents — Claude
Code, Codex, Cursor — read it as context.

**What it is not.** A code project, or an execution engine: nothing here drives a child repo's
state. Validators, generators and gates are in scope; orchestration scripts are not. The layer
model that makes that a checkable invariant is `ARCHITECTURE.md` **Purpose** and **Layer
Boundaries & Invariants** — read it there rather than restated here.

## Quickstart

The environment is **declared, not discovered** — `pyproject.toml` + `uv.lock` +
`.python-version`, with `uv` itself pinned exactly. Every command goes through
`uv run --locked`; a bare `python` or `pytest` resolves nothing on a clean checkout, so one in
a doc is a defect rather than a shorthand.

```bash
uv sync --locked                                   # build the declared environment
uv run --locked pytest -x --tb=short               # the suite
uv run --locked ruff check --fix                   # lint (also a pre-commit gate)
uv run --locked python scripts/audit.py health     # self-conformance gate
```

Arm the commit gates once per clone. They are not advisory — a FAIL blocks, and the fix is the
cause, not `--no-verify`:

```bash
uv run --locked pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

**To land a change:** branch, then merge with `--no-ff`; never commit directly to `main`. Branch
prefixes are a closed enum, commit types follow Conventional Commits, and a commit that opens or
closes a backlog row carries its own required line. This section starts you; `AGENTS.md`
(portable, every provider) and `CONTRIBUTING.md` (full) govern you.

## Map

**Start here, in this order**

- `CLAUDE.md` — the session contract for Claude Code in this repo
- `AGENTS.md` — the portable instruction layer every provider reads (ADR-115)
- `ARCHITECTURE.md` — the structural map; read before structural changes
- `CONTRIBUTING.md` — branch/commit/validator conventions

**Process and doctrine**

- `protocols/PLAYBOOK.md` — full process reference; consulted on demand, never a boot-time read
- `protocols/ESSENTIALS.md` — operating values, daily cheat sheet; **superseded, pending `[#628]`** — not a boot read
- `docs/decisions/` — architectural decisions (ADRs only; the `transcripts/` landing zone was deleted 2026-07-22)
- ADR-88 — File-oriented dependency management (markdown as a design pattern): repo files are the dependency unit; coherence across the declared edge-graph is held by mechanism — a conformance harness — not by memory.

**State — what happened, what is pending, what is next**

- `JOURNAL.md` — session-by-session activity history (and notable-change record; replaces the retired CHANGELOG.md per ADR-49)
- `BACKLOG.md` — cross-session pending items (per ADR-41); a generated VIEW — edit `tasks/`, then regenerate
- `LESSONS.md` — append-only empirical patterns; read before structural changes
- `ecosystem/north-star.md` — **the arc set in dependency order: what this repo is working towards and what blocks what.** GENERATED from `tasks/` (`scripts/gen_north_star.py --write`); the arc names and their order are declared, every count and member row is derived, so it cannot drift from the backlog the way a hand-written roadmap does

**Superseded, retained, still tracked**

- `docs/archive/governance.md` — full Vision, Strategic emphasis, Scope, Values, Relationships and Lifecycle; relocated from this file by lane `lane-h0-readme` ([#634], 2026-09-05)
- `docs/archive/VISION.md` — superseded by this file (ADR-114); relocated here at the hub ([#614] lane-e-5, 2026-09-01), retained and still tracked
