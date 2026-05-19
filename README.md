# .dev-knowledge

Universal LLM-driven development guide and methodology framework for
Rob's ecosystem. Knowledge guardian, methodology author, auditor —
absorbs lessons from individual projects, universalizes them into
patterns, disseminates patterns back as enforceable conventions, and
verifies child-repo conformance. Not a journal, not an orchestrator,
not application code: a reference library + cross-repo governance
layer. Full mission and scope in `VISION.md`; structural model in
`ARCHITECTURE.md`.

## For whom
<!-- scope: meta -->

- **Primary reader:** Rob, when starting a new browser chat or VS Code session
- **Secondary reader:** Claude (via CLAUDE.md pointer + automatic file reads)
- **Tertiary:** future contributor (hypothetical — no active second contributor)

## Starting a new browser chat
<!-- scope: llm -->

Upload to the new chat:
1. `protocols/ESSENTIALS.md` (daily cheat sheet)
2. `protocols/HANDOFF_PROCESS.md` (if continuing from another chat)
3. Most recent handoff in `docs/handoffs/` (if any)
4. Project-specific context (CLAUDE.md from target repo if programming)

Before chartering session goals: review `BACKLOG.md` for pending items.
First message: state objective + 1-2 goals.

## Starting a Claude Code session
<!-- scope: runtime -->

In terminal, inside project repo: `/boot` (loads rules, memory, trends).
`.dev-knowledge` is NOT the working repo — it's reference. Claude Code
reads it only when pointed (e.g. "check .dev-knowledge/protocols/PLAYBOOK.md Section X").

## Folder layout
<!-- scope: meta -->

| Folder | Purpose | Read when |
|--------|---------|-----------|
| `(root)` | Canonical files: VISION, ARCHITECTURE, README, CLAUDE, BACKLOG, CHANGELOG, JOURNAL, LESSONS, CONTRIBUTING | Daily / session start |
| `protocols/` | Operational protocols: ESSENTIALS, PLAYBOOK, HANDOFF_PROCESS, SESSION_SETUP, ENVIRONMENT | Process reference |
| `logs/` | Append-only logs: TOKEN-LOG | Token tracking (threshold-triggered) |
| `config/` | Repo config: requirements-dev.txt | Tooling reference |
| `docs/decisions/` | ADRs (decisions binding across sessions) | When making similar architectural decision |
| `docs/decisions/transcripts/` | AI Council debate raw outputs | When reviewing how a decision was reached |
| `docs/research/` | Research-mode debates, external research reports | When evaluating new tools / patterns |
| `docs/audits/` | Point-in-time analyses (dated) | Reference; superseded files marked in-file |
| `docs/handoffs/` | Per-session handoff summaries (folders for new format, .md files for legacy) | When resuming work after break |
| `scripts/` | Validators + automation | Reference; run via pre-commit |
| `templates/` | Reusable boilerplate (e.g. CLAUDE.md scaffold) | When bootstrapping similar patterns elsewhere |
| `.claude/` | Claude Code config (skills, commands, rules) | Automatic — Claude Code reads on boot |

## Navigation (where to look)
<!-- scope: meta -->

- **How do I prompt Claude Code?** → `protocols/PLAYBOOK.md` (prompt structure + examples)
- **What am I supposed to do when starting?** → `protocols/ESSENTIALS.md`
- **What prescriptive architectural decisions apply?** → `docs/decisions/` (ADR-NN-topic.md, binding across all sessions)
- **What did I learn recently?** → `LESSONS.md` (append-only, scope-tagged)
- **Where are stream-level strategic/process decisions and session status?** → `docs/handoffs/` (most recent for active stream; dated files/folders are persistent stream archive — covers session plans, cluster ordering, execution sequencing decisions that aren't ADR-worthy individually but bind stream coordination)
- **How do I run Council debate?** → `protocols/PLAYBOOK.md` Section 5 + "Council Debate Archival Protocol" subsection

## Current state (2026-04-28)
<!-- scope: meta -->

- Stream A complete: scope tagging live, validator enforces, hybrid ceiling delta-based
- Stream C session 1 complete: ADR-30 (default branch = main), ADR-31 (authority model), ADR-32 (handoff format), PLAYBOOK Repo conventions skeleton; HANDOFF_PROCESS.md v2.0 lands the operational counterpart of ADR-32
- VISION.md + ARCHITECTURE.md established 2026-04-28: universal-brain mission and structural model
- ADRs in `docs/decisions/` + corp-monorepo
- See LESSONS.md (scope-tagged inline per ADR-29)
- Council debates archived (transcripts in corp-monorepo and/or docs/decisions/transcripts/, research in docs/research/)
- Gaps identified for future streams: see latest audit file

## Not here (deliberately)
<!-- scope: meta -->

- Client/product/domain knowledge → Obsidian vault
- Claude Code runtime config (skills, hooks, slash commands) → `~/.claude/` (user-level) + `.claude/` in target repo (project-level)
- Actual project code → standalone repos (corp-monorepo, ai-council, etc.)

## Conventions
<!-- scope: meta -->

- **Filenames:** kebab-case for dated (`YYYY-MM-DD-slug.md`), `ADR-NN-topic.md` for ADRs (per ADR-34), `DECISION_NN_snake_case.md` for legacy transcripts (grandfathered)
- **Scope tags:** every section in tagged files has `<!-- scope: X -->` (dev|llm|hybrid|runtime|meta). Enforced by pre-commit hook.
- **Amendment vs reopen:** minor prescription drift → amend ADR in-place. Intent change → new ADR or Council reopen.
- **Append-only:** LESSONS.md, CHANGELOG.md, TOKEN-LOG.md — never reorder or delete entries.

## How it relates to other repos
<!-- scope: meta -->

- `corp-monorepo` (Scale L): own governance stack (CLAUDE.md, JOURNAL.md, docs/HANDOFF.md living doc). Some patterns shared.
- `ai-council` (Scale M): own Python project, outputs flow to target repos per PLAYBOOK S5.N archival protocol. Functions as a tool used by `.dev-knowledge` to generate architectural decisions; debate transcripts return to `.dev-knowledge/docs/decisions/transcripts/` per Council output convention.
- This repo is the meta-layer and universal brain: how I decide, what I learned, how sessions resume — see `VISION.md` for full mission framing.
- **Workspace coordination** (outside any single repo): `Dev/.settings/repos.toml` (repo discovery manifest for cross-repo audit) + `Dev/.settings/HUB.md` (multi-repo coordination index). Created 2026-04-27 per Topic 1 authority model + Research Meta-Repo pattern synthesis.
