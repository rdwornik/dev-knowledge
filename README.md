# .dev-knowledge

Personal operating system for LLM-augmented dev and presales work.
Not a journal. Not an orchestrator. A reference library + governance
for how I work with Claude (Code + browser) and other LLM tools.

## For whom
<!-- scope: meta -->

- **Primary reader:** Rob, when starting a new browser chat or VS Code session
- **Secondary reader:** Claude (via CLAUDE.md pointer + automatic file reads)
- **Tertiary:** future contributor (hypothetical — no active second contributor)

## Starting a new browser chat
<!-- scope: llm -->

Upload to the new chat:
1. `ESSENTIALS.md` (daily cheat sheet)
2. `HANDOFF_PROCESS.md` (if continuing from another chat)
3. Most recent handoff in `docs/handoffs/` (if any)
4. Project-specific context (CLAUDE.md from target repo if programming)

First message: state objective + 1-2 goals.

## Starting a Claude Code session
<!-- scope: runtime -->

In terminal, inside project repo: `/boot` (loads rules, memory, trends).
`.dev-knowledge` is NOT the working repo — it's reference. Claude Code
reads it only when pointed (e.g. "check .dev-knowledge/PLAYBOOK.md Section X").

## Folder layout
<!-- scope: meta -->

| Folder | Purpose | Read when |
|--------|---------|-----------|
| `(root)` | Core governance files | Daily / session start |
| `docs/decisions/` | ADRs (decisions binding across sessions) | When making similar architectural decision |
| `docs/decisions/transcripts/` | AI Council debate raw outputs | When reviewing how a decision was reached |
| `docs/research/` | Research-mode debates, external research reports | When evaluating new tools / patterns |
| `docs/audits/` | Point-in-time analyses (dated) | Reference; superseded files marked in-file |
| `docs/handoffs/` | Per-session handoff summaries | When resuming work after break |
| `handoff-prompts/` | Live copy-paste templates for generating handoffs | When running a handoff (not archiving) |
| `scripts/` | Validators + automation | Reference; run via pre-commit |
| `templates/` | Reusable boilerplate (e.g. AGENTS.md scaffold) | When bootstrapping similar patterns elsewhere |
| `.claude/` | Claude Code config (skills, commands, rules) | Automatic — Claude Code reads on boot |

## Navigation (where to look)
<!-- scope: meta -->

- **How do I prompt Claude Code?** → `PLAYBOOK.md` (prompt structure + examples)
- **What am I supposed to do when starting?** → `ESSENTIALS.md`
- **What decisions apply?** → `docs/decisions/` (ADR-NN_topic.md)
- **What did I learn recently?** → `LESSONS.md` (append-only, scope-tagged)
- **Where are we in current work?** → `docs/handoffs/` (most recent file)
- **How do I run Council debate?** → `PLAYBOOK.md` Section 5 + Section 5.N (archival)

## Current state (2026-04-26)
<!-- scope: meta -->

- Stream A complete: scope tagging live, validator enforces, hybrid ceiling delta-based
- 31 ADRs active (ADR-01 through ADR-30, plus CLAUDE.md governing this repo)
- 69 lessons in LESSONS.md, scope-tagged inline per ADR-29
- Council #1-#29 archived (transcripts in corp-monorepo and/or docs/decisions/transcripts/, research in docs/research/)
- 19 gaps identified for future streams (see latest audit file)

## Not here (deliberately)
<!-- scope: meta -->

- Client/product/domain knowledge → Obsidian vault
- Claude Code runtime config (skills, hooks, slash commands) → `~/.claude/` (user-level) + `.claude/` in target repo (project-level)
- Actual project code → standalone repos (corp-monorepo, ai-council, etc.)

## Conventions
<!-- scope: meta -->

- **Filenames:** kebab-case for dated (`YYYY-MM-DD-slug.md`), `ADR-NN_topic.md` for ADRs, `DECISION_NN_snake_case.md` for transcripts
- **Scope tags:** every section in tagged files has `<!-- scope: X -->` (dev|llm|hybrid|runtime|meta). Enforced by pre-commit hook.
- **Amendment vs reopen:** minor prescription drift → amend ADR in-place. Intent change → new ADR or Council reopen.
- **Append-only:** LESSONS.md, CHANGELOG.md, TOKEN-LOG.md — never reorder or delete entries.

## How it relates to other repos
<!-- scope: meta -->

- `corp-monorepo` (Scale L): own governance stack (CLAUDE.md, AGENTS.md, JOURNAL.md, docs/HANDOFF.md living doc). Some patterns shared.
- `ai-council` (Scale M): own Python project, outputs flow to target repos per PLAYBOOK S5.N archival protocol.
- This repo is the meta-layer: how I decide, what I learned, how sessions resume.
