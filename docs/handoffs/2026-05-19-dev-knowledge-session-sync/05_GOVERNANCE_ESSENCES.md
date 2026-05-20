# Governance Essences — ADRs cited in this handoff

<!-- scope: meta -->

Operational essences (2-3 sentences each) for ADRs explicitly cited in
`07_ACTION_PLAN.md` directives or hard constraints. Not full ADR text.
The new chat reads full ADRs in-repo when needed.

---

## ADR-51 — Architecture Documentation Convention

Every M/L-tier repo MUST have an `ARCHITECTURE.md` at root with a canonical
structural-context section ("codemap") covering modules, dependency edges,
and layer assignments. Size-tiered policy: M/L receive a graphical codemap,
S receive a text-only module overview. The codemap is intended to be
**auto-generated** with a CI freshness check; until the generator ships,
authors hand-maintain the codemap in the interim package-tree-with-layer-
annotation format documented inline in `templates/ARCHITECTURE-template.md`.
The convention is load-bearing on the generator existing — the codemap
generator + CI check are the open implementation item this handoff targets.

Full ADR: `docs/decisions/ADR-51-architecture-doc-convention.md`

---

## ADR-54 — Codex Reviewer Config as Global Standard

The Codex reviewer configuration is a **global** standard at
`~/.codex/AGENTS.md`, with the canonical source tracked at
`codex/AGENTS.md` in `.dev-knowledge` and deployed to the user-home
location. The global config carries the generic reviewer role (review
checklist, output format, do-not-modify rules) plus an explicit instruction
to **read each repo's `ARCHITECTURE.md` for structural context** before
reviewing. ADR-54 is scoped to tool configuration (Codex), distinct from
ADR-53 which governs the agent-instruction contract (Claude Code via
CLAUDE.md). Per-repo `AGENTS.md` files remain available for genuinely
repo-specific reviewer overrides but are not required.

Full ADR: `docs/decisions/ADR-54-codex-reviewer-global-standard.md`

**Why this matters for the next session:** ADR-54's "Codex reads each
repo's `ARCHITECTURE.md`" instruction is the load-bearing assumption that
makes the codemap generator + freshness check valuable. The new chat
treats ADR-54 as a given input and does NOT re-litigate it.
