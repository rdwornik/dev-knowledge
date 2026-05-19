# ADR-54: Codex Reviewer Config as Global Standard

- **Status:** Accepted
- **Date:** 2026-05-19
- **Amends:** —
- **Related:** ADR-53 (CLAUDE.md as single instruction file — distinct concern), ADR-31 (authority model baseline)
- **Decommission:** none
- **Source:** Rob's decision, 2026-05-19. Prompted by identifying that the generic Codex reviewer config lived only in `corp-monorepo/AGENTS.md` while Codex's layering model routes cross-project config to `~/.codex/AGENTS.md`.

## Context

The generic Codex reviewer config (role, review checklist, output format) resided only in `corp-monorepo/AGENTS.md`. The other ecosystem repos (`ai-council`, `.dev-knowledge`) had no Codex reviewer config at all. This was incoherent: the config is cross-project in nature, and Codex's own model explicitly layers a global `~/.codex/AGENTS.md` with optional per-repo `AGENTS.md` overrides.

Two problems followed from the per-repo-only placement:
1. **Duplication surface.** Any repo that wants Codex review must copy the generic config, creating drift.
2. **Incomplete coverage.** Repos without a per-repo `AGENTS.md` had no reviewer behavior defined.

The `corp-monorepo/AGENTS.md` also contained a repo-specific "Architecture Context" section that duplicated structural content available via `ARCHITECTURE.md`. However, Codex does not auto-load `ARCHITECTURE.md` — it reads `CLAUDE.md` via `project_doc_fallback_filenames = ["CLAUDE.md"]` in `~/.codex/config.toml`, and `CLAUDE.md` only points to `ARCHITECTURE.md`. Without an explicit instruction, structural context was inaccessible to Codex.

**Scope distinction from ADR-53:** ADR-53 retired `AGENTS.md` as the *agent-instruction contract* (the file used to instruct Claude Code, Cursor, Aider, etc.). This ADR governs `AGENTS.md` as Codex's *tool configuration* — a distinct concern. Both ADRs coexist without conflict.

## Decision

1. **The Codex reviewer config (role, review checklist, output format) is a global standard.** It belongs in `~/.codex/AGENTS.md`, not per-repo.

2. **The canonical source is `codex/AGENTS.md` in `.dev-knowledge`.** Updates to the global reviewer config are made here and deployed to `~/.codex/AGENTS.md` by copying. `.dev-knowledge` owns the global standard.

3. **The global config instructs Codex to read the repo's `ARCHITECTURE.md` if present** before reviewing. This explicit instruction routes Codex to structural context (dependency rules, module boundaries, invariants) that `project_doc_fallback_filenames` alone does not provide.

4. **Per-repo `AGENTS.md` files carry only repo-specific review rules.** They do not repeat global reviewer config content. A per-repo file adds checks specific to that repo's architecture, tooling, or invariants.

5. **`corp-monorepo/AGENTS.md` is outside ADR-53's scope** (Codex tool config, not an agent-instruction contract). Its generic reviewer content is superseded by the global config. Its repo-specific "Architecture Context" is superseded by Decision 3 — Codex now reads `ARCHITECTURE.md` directly rather than relying on inline duplication. Retirement of `corp-monorepo/AGENTS.md` is a follow-up chunk in that repo.

## Rationale

- Codex's own layering model (`~/.codex/AGENTS.md` → per-repo `AGENTS.md`) is designed for exactly this split: global invariants at the user level, repo-specific additions at the repo level.
- A single canonical source eliminates duplication and ensures all repos benefit from the same baseline reviewer behavior without per-repo maintenance.
- The explicit `ARCHITECTURE.md` read instruction is necessary because `project_doc_fallback_filenames` only auto-loads `CLAUDE.md`; structural context requires an active instruction to Codex.
- Tracking the canonical source in `.dev-knowledge` aligns with its role as the binding source of cross-repo prescriptions (ADR-31).

## Consequences

- `~/.codex/AGENTS.md` now exists and contains the global reviewer config (deployed 2026-05-19).
- **Subsequent chunk (corp-monorepo):** remove `corp-monorepo/AGENTS.md` or reduce it to repo-specific additions only.
- Any future repo-specific Codex review rules belong in that repo's own `AGENTS.md` as additions to the global baseline.
- Updates to the global reviewer config must be made in `codex/AGENTS.md` here and redeployed to `~/.codex/AGENTS.md`.

## Alternatives considered

- **Keep generic config per-repo, copy to each new repo** — rejected: perpetuates duplication and ensures drift over time; the global file model already exists for this purpose.
- **Inline architecture context in global config** — rejected: cross-repo structural summaries cannot be maintained in one file; the per-repo `ARCHITECTURE.md` + explicit read instruction is the correct model.
- **Do nothing; leave corp-monorepo/AGENTS.md as the de facto standard** — rejected: other repos have no Codex config, and the config's placement in one child repo is not discoverable or maintainable as the ecosystem grows.
